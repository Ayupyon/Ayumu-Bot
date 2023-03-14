import os
from random import sample

from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

from src.plugins.random_picture import picture_folder_path
from src.plugins.random_picture.model import get_name


async def pick_picture_rule(event: MessageEvent, state: T_State):
    text = event.get_plaintext()
    if len(text) > 20:
        return False
    name = await get_name(text)
    if name is not None:
        state["name"] = name
        return True
    return False


pick_picture = on_message(rule=pick_picture_rule, priority=5)


@pick_picture.handle()
async def _(state: T_State):
    name = state["name"]
    folder = picture_folder_path(name)
    if not os.path.exists(str(folder)):
        pick_picture.send("小步梦还没有这个名称对应的图片，快去添加几张吧！", at_sender=True)
        return
    picture_list = os.listdir(str(folder))
    picture_name: str = sample(picture_list, 1)[0]
    message = MessageSegment.image(folder.joinpath(picture_name))
    await pick_picture.send(message, at_sender=True)