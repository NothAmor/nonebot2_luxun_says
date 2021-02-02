import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import textwrap
import random
import os

from nonebot import on_command
from nonebot.adapters.cqhttp import Message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.log import logger

import nonebot

luxun = on_command("luxun", aliases=set(["鲁迅说"]), rule=None)

@luxun.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["content"] = args

@luxun.got("content", prompt="你让鲁迅说点啥?")
async def handle_event(bot: Bot, event: Event, state: T_State):
    filename = str(event.get_user_id()) + str(random.randint(0, 10000)) + ".jpg"
    content = state["content"]

    at_ = f"[CQ:at,qq={event.get_user_id()}]"

    if len(content) >= 25:
        await luxun.finish(Message(at_ + " 太长了, 鲁迅说不完!"))
    else:
        await process_pic(content, filename)
        cqimg = f"[CQ:image,file=file:////root/qqBot/NothAmor-Bot/nothamor_bot/plugins/luxun_says/says_img/{filename}]"
        
        await luxun.finish(Message(cqimg))


async def process_pic(content, filename):
    text = content
    para = textwrap.wrap(text, width=15)
    MAX_W, MAX_H = 480, 280

    bk_img = cv2.imread("/root/qqBot/NothAmor-Bot/nothamor_bot/plugins/luxun_says/luxun.jpg")
    font_path = "msyh.ttf"
    font = ImageFont.truetype(font_path, 37)
    font2 = ImageFont.truetype(font_path, 30)

    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)

    current_h, pad = 300, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad

    draw.text((320, 400),  "——鲁迅", font = font2, fill = (255, 255, 255))
    
    bk_img = np.array(img_pil)
    cv2.imwrite("/root/qqBot/NothAmor-Bot/nothamor_bot/plugins/luxun_says/says_img/" + filename, bk_img)
