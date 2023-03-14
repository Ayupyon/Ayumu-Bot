from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message

from src.plugins.random_picture.model import PictureName, PictureAlias


# 查看名称对应的昵称列表 格式: 昵称列表 名称
alias_list = on_command("昵称列表", priority=5)


@alias_list.handle()
async def _(args: Message=CommandArg()):
    name = args.extract_plain_text()
    if not PictureName.exists(name=name):
        await alias_list.send("不存在该名称，请先添加名称！！", at_sender=True)
        return
    res = await PictureAlias.filter(name=name)
    if len(res) == 0:
        await alias_list.send("该名称还没有对应的昵称，去添加一个吧！", at_sender=True)
    else:
        message = f"{name}的昵称有：" + "，".join([picture_alias.alias for picture_alias in res])
        await alias_list.send(message, at_sender=True)
