from nonebot import on_command
from nonebot.params import Depends, CommandArg
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent, 
    MessageSegment, 
    Message
)
from nonebot.adapters.onebot.v11.permission import GROUP

from src.providers.database.model import User


# 修改签到口令
modify_token = on_command("设置签到口令", priority=5, permission=GROUP)


@modify_token.handle()
async def _(event: GroupMessageEvent, arg: Message=CommandArg()):
    user_id = event.get_user_id()
    user, _ = await User.get_or_create(id=user_id)
    token = arg.extract_plain_text()
    message = MessageSegment.at(user.id)
    if len(token) > 15:
        message += " 口令太长啦~请换一个短一点的"
        await modify_token.send(message)
    else:
        try:
            user.checkin_token = token
            await user.save()
            message += f"设置成功！当前口令为：{token}"
            await modify_token.send(message)
        except:
            await modify_token.send("出现了问题,请稍后重试或联系bot管理员解决")
        