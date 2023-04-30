#!/usr/bin/env python

from config import chat
from minigpt4.conversation.conversation import CONV_VISION
from PIL import Image

img = Image.open('/Users/z/Downloads/11.jpeg')

imgli = []
chat_state = CONV_VISION.copy()
chat.upload_img(img, chat_state, imgli)

msg = 'Create title for the image'

chat.ask(msg, chat_state)
llm_message = chat.answer(conv=chat_state,
                          img_list=img_list,
                          num_beams=num_beams,
                          temperature=temperature,
                          max_new_tokens=3000,
                          max_length=20000)[0]
