from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

from nonebot import on_type
from nonebot.adapters.onebot.v11 import (
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    MessageSegment,
)


# 发送欢迎信息
member_welcome = on_type(GroupIncreaseNoticeEvent, priority=1)
# 退群信息通知
member_leave = on_type(GroupDecreaseNoticeEvent, priority=1)


@member_welcome.handle()
async def _(event: GroupIncreaseNoticeEvent):
    message = (MessageSegment.at(event.get_user_id()) +
               "欢迎新大佬，这里是小步梦~")
    await member_welcome.finish(message)


@member_leave.handle()
async def _(event: GroupDecreaseNoticeEvent):
    await member_leave.finish(f"呜呜呜，有人离开了（{event.get_user_id()}）")