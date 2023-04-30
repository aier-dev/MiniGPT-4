import random

import numpy as np
import torch
import torch.backends.cudnn as cudnn
import gradio as gr

from minigpt4.common.dist_utils import get_rank
from minigpt4.conversation.conversation import CONV_VISION

# imports modules for registration
from minigpt4.datasets.builders import *
from minigpt4.models import *
from minigpt4.processors import *
from minigpt4.runners import *
from minigpt4.tasks import *

from config import chat


def setup_seeds(config):
    seed = config.run_cfg.seed + get_rank()

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    cudnn.benchmark = False
    cudnn.deterministic = True


# ========================================
#             Gradio Setting
# ========================================


def gradio_reset(chat_state, img_list):
    if chat_state is not None:
        chat_state.messages = []
    if img_list is not None:
        img_list = []
    return None, gr.update(value=None, interactive=True), gr.update(
        placeholder='Please upload your image first',
        interactive=False), gr.update(value="Upload & Start Chat",
                                      interactive=True), chat_state, img_list


def upload_img(gr_img, text_input, chat_state):
    if gr_img is None:
        return None, None, gr.update(interactive=True), chat_state, None
    chat_state = CONV_VISION.copy()
    img_list = []
    chat.upload_img(gr_img, chat_state, img_list)
    return gr.update(interactive=False), gr.update(interactive=True,
                                                   placeholder='Type and press Enter'), gr.update(
                                                       value="Start Chatting",
                                                       interactive=False), chat_state, img_list


def gradio_ask(user_message, chatbot, chat_state):
    if len(user_message) == 0:
        return gr.update(interactive=True,
                         placeholder='Input should not be empty!'), chatbot, chat_state
    print('\nask', user_message, '\nchat_state', chat_state)
    chat.ask(user_message, chat_state)
    chatbot = chatbot + [[user_message, None]]
    return '', chatbot, chat_state


def gradio_answer(chatbot, chat_state, img_list, num_beams, temperature):
    print('\nanswer', chat_state, '\nimg_list', img_list, '\nnum_beams', num_beams, '\ntemperature',
          temperature)
    llm_message = chat.answer(conv=chat_state,
                              img_list=img_list,
                              num_beams=num_beams,
                              temperature=temperature,
                              max_new_tokens=3000,
                              max_length=20000)[0]
    print('\nllm_message', llm_message)
    chatbot[-1][1] = llm_message
    return chatbot, chat_state, img_list


title = """<h1 align="center">Demo of MiniGPT-4</h1>"""
description = """<h3>This is the demo of MiniGPT-4. Upload your images and start chatting!</h3>"""
article = """<p><a href='https://minigpt-4.github.io'><img src='https://img.shields.io/badge/Project-Page-Green'></a></p><p><a href='https://github.com/Vision-CAIR/MiniGPT-4'><img src='https://img.shields.io/badge/Github-Code-blue'></a></p><p><a href='https://raw.githubusercontent.com/Vision-CAIR/MiniGPT-4/main/MiniGPT_4.pdf'><img src='https://img.shields.io/badge/Paper-PDF-red'></a></p>
"""

#TODO show examples below

with gr.Blocks() as demo:
    gr.Markdown(title)
    gr.Markdown(description)
    gr.Markdown(article)

    with gr.Row():
        with gr.Column(scale=0.5):
            image = gr.Image(type="pil")
            upload_button = gr.Button(value="Upload & Start Chat",
                                      interactive=True,
                                      variant="primary")
            clear = gr.Button("Restart")

            num_beams = gr.Slider(
                minimum=1,
                maximum=10,
                value=1,
                step=1,
                interactive=True,
                label="beam search numbers)",
            )

            temperature = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=1.0,
                step=0.1,
                interactive=True,
                label="Temperature",
            )

        with gr.Column():
            chat_state = gr.State()
            print('\ngr.Column chat_state', chat_state)
            img_list = gr.State()
            chatbot = gr.Chatbot(label='MiniGPT-4')
            text_input = gr.Textbox(label='User',
                                    placeholder='Please upload your image first',
                                    interactive=False)

    upload_button.click(upload_img, [image, text_input, chat_state],
                        [image, text_input, upload_button, chat_state, img_list])

    text_input.submit(gradio_ask,
                      [text_input, chatbot, chat_state], [text_input, chatbot, chat_state]).then(
                          gradio_answer, [chatbot, chat_state, img_list, num_beams, temperature],
                          [chatbot, chat_state, img_list])
    clear.click(gradio_reset, [chat_state, img_list],
                [chatbot, image, text_input, upload_button, chat_state, img_list],
                queue=False)

demo.launch(share=True, enable_queue=True)
