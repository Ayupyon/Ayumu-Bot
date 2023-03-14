from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message

from src.plugins.random_picture.model import PictureName, PictureAlias


# 添加昵称 格式：添加昵称 名称 昵称
add_alias = on_command("添加昵称", priority=5)


@add_alias.handle()
async def _(args: Message=CommandArg()):
    name, alias = args.extract_plain_text().split(' ', 2)
    if not await PictureName.exists(name=name):
        await add_alias.send("不存在该名称，请先添加名称！！", at_sender=True)
        return
    if len(alias) > 20:
        await add_alias.send("昵称太长啦！！", at_sender=True)
        return
    picture_alias, create = await PictureAlias.get_or_create(defaults={"name": name}, alias=alias)
    if create:
        await add_alias.send(f"成功为 {name} 添加昵称 {alias}~", at_sender=True)
    else:
        await add_alias.send(f"该昵称已经被设置为 {picture_alias.name} 的昵称了！！", at_sender=True)