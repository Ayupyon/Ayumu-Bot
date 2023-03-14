from datetime import datetime
from io import BytesIO

from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    MessageSegment,
    Bot,
)
from nonebot.adapters.onebot.v11.permission import GROUP

from src.plugins.daily_checkin.model import is_special, get_tips
from src.providers.database.model import User
from src.providers.playwright.pic_render import render


async def checkin_rule(event: GroupMessageEvent, state: T_State) -> bool:
    text = event.get_plaintext()
    user_id = event.get_user_id()
    # 默认口令
    if text == "小步梦签到":
        user, _ = await User.get_or_create(id=user_id)
        state["user"] = user
        return True
    # 自定义口令
    user = await User.get_or_none(id=user_id)
    if user is not None and text == user.checkin_token:
        state["user"] = user
        return True
    return False


# 签到功能
checkin = on_message(rule=checkin_rule, priority=5, permission=GROUP)
    

async def get_star_delta(checkin_days: int) -> int:
    res = 200
    if checkin_days <= 20:
        res = 50
    elif checkin_days <= 50:
        res = 100
    elif checkin_days <= 100:
        res = 150
    if await is_special():
        res += 500
    return res


@checkin.handle()
async def _(bot: Bot, state: T_State):
    user: User = state["user"]
    cur_date = datetime.now().date()
    if user.last_checkin == cur_date:
        img = await get_img(bot, user, 0, "您今天已经签到过了，这里显示您的当前状态")
        message = MessageSegment.image(img)
        await checkin.send(message, at_sender=True)
    else:
        if (cur_date - user.last_checkin).days == 1:
            user.checkin_days += 1
        else:
            user.checkin_days = 1
        user.last_checkin = cur_date
        star_delta = await get_star_delta(user.checkin_days)
        user.star += star_delta
        img = await get_img(bot, user, star_delta, await get_tips())
        message = MessageSegment.image(img)
        await checkin.send(message, at_sender=True)
        await user.save()


async def get_img(bot: Bot, user: User, delta: int, tips: str) -> BytesIO:
    return await render(
        "check_in_template.html",
        user_id=user.id,
        user_name=(await bot.get_stranger_info(user_id=user.id))["nickname"],
        token=(user.checkin_token if user.checkin_token is not None else "暂未设置口令"),
        star=user.star,
        star_delta=f"{delta:+}" if delta != 0 else "",
        checkin_days=user.checkin_days,
        tips=tips
    )