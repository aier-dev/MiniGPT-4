#!/usr/bin/env python

from config import chat
from minigpt4.conversation.conversation import CONV_VISION
from PIL import Image

IMGLI = []
STATE = CONV_VISION.copy()


def qa(msg):
    print('\n>', msg)
    chat.ask(msg, STATE)

    # num_beams=3 表示我们在解码阶段保留 3 个最有可能的翻译候选者。
    num_beams = 1

    # temperature 创意程度, 0.8到2之间
    temperature = 1

    max_new_tokens = 3000
    max_length = max_new_tokens * 10

    llm_message = chat.answer(conv=STATE,
                              img_list=IMGLI,
                              num_beams=num_beams,
                              temperature=temperature,
                              max_new_tokens=max_new_tokens,
                              max_length=max_length)[0]

    print('\n<', llm_message, end='\n\n')


def run(fp, li):
    global STATE, IMGLI
    print('\n' + fp + '\n')
    STATE.messages = []
    IMGLI = []
    img = Image.open(fp)
    chat.upload_img(img, STATE, IMGLI)
    for msg in li:
        qa(msg)


if __name__ == '__main__':
    imgli = ['/Users/z/Downloads/11.jpeg', '/Users/z/Downloads/12.jpeg']
    qli = [
        'Create title for the image',
        'Generate a detailed description for the image',
        'Tag the picture, tags are separated by commas',
    ]

    for fp in imgli:
        run(fp, qli)
