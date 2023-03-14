from datetime import datetime, date

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.sqlite.functions import Random
from nonebot import get_driver, require


require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler


_is_special: bool = False
_special_tips: str | None = None
driver = get_driver()


class Tips(Model):
    tips = fields.CharField(max_length=255)

    class Meta:
        table = "checkin_tips"


class SpecicalTips(Model):
    # 格式: 月-日 eg:3-1,12-25
    special_date = fields.CharField(max_length=5, pk=True)
    tips = fields.CharField(max_length=255)

    class Meta:
        table = "special_checkin_tips"


@driver.on_bot_connect
async def check_special():
    global _is_special, _special_tips
    cur_date = datetime.now().date()
    res = await SpecicalTips.get_or_none(
        special_date=f"{cur_date.month}-{cur_date.day}"
    )
    if res is None:
        _is_special = False
        _special_tips = None
    else:
        _is_special = True
        _special_tips = res.tips


scheduler.add_job(check_special, "cron", hour=0, minute=0)


async def is_special() -> bool:
    global _is_special
    return _is_special


async def get_tips() -> str:
    global _is_special, _special_tips
    if _is_special:
        assert _special_tips
        return _special_tips
    return (await Tips.annotate(order=Random()).order_by("order").first()).tips