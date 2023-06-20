from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER

from src.plugins.random_picture.model import PictureName


add_name = on_command("添加名称", priority=5, permission=GROUP_ADMIN | GROUP_OWNER)


@add_name.handle()
async def _(args: Message=CommandArg()):
    name = args.extract_plain_text()
    if len(name) > 20:
        await add_name.send("这个名称太长啦！！", at_sender=True)
        return
    _, create = await PictureName.get_or_create(name=name)
    if create:
        await add_name.send("添加成功~", at_sender=True)
    else:
        await add_name.send("这个名称已经添加过啦~", at_sender=True)