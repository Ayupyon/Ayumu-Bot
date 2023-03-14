import os
from io import BytesIO
from datetime import datetime

import httpx
from PIL import Image
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.helpers import extract_image_urls

from src.plugins.random_picture import picture_folder_path
from src.plugins.random_picture.model import get_name


add_picture = on_command("添加图片", aliases={"add",}, priority=5)


@add_picture.handle()
async def _(args: Message=CommandArg()):
    name_or_alias = args.extract_plain_text()
    name = await get_name(name_or_alias)
    if name is None:
        await add_picture.send("小步梦没有这个名称的信息，请先添加名称或昵称~", at_sender=True)
        return
    urls = extract_image_urls(args)
    await save_pictures(name, urls)
    await add_picture.send("保存成功~", at_sender=True)


async def save_pictures(name: str, urls: list[str]):
    folder_path = picture_folder_path(name)
    if not os.path.exists(str(folder_path)):
        os.makedirs(str(folder_path))
    time = datetime.now()
    picture_name = f"{time.year}_{time.month}_{time.day}_{time.hour}_{time.second}"
    async with httpx.AsyncClient() as client:
        for i, url in enumerate(urls):
            response = await client.get(url)
            image = Image.open(BytesIO(response.content))
            image.save(folder_path.joinpath(f"{picture_name}_{i}.jpeg"), format="jpeg")