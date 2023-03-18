from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

from src.providers.pathutil import resource_path


help = on_command("使用帮助", priority=5, block=True)


@help.handle()
async def _():
    await help.send(MessageSegment.image(resource_path("help.png")))