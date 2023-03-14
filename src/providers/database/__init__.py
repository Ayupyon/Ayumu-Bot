from tortoise import Tortoise
from nonebot import get_driver

from .config import Config


driver = get_driver()
db_config = Config.parse_obj(driver.config)

tortoise_config = {
    "connections": {
        "bot": db_config.db_url,
    },
    "apps": {
        "bot": {
            "models": [
                "src.providers.database.model",
                "src.plugins.daily_checkin.model",
                "src.plugins.random_picture.model",
            ],
            "default_connection": "bot"
        }
    },
    "timezone": "UTC+8",
}


async def init_db():
    await Tortoise.generate_schemas()
    from src.providers.database.model import User
    from src.plugins.daily_checkin.model import Tips, SpecicalTips
    from src.plugins.random_picture.model import PictureName
    import json

    user = await User.get(id=1501923345)
    user.checkin_days = 75
    await user.save()


@driver.on_startup
async def init_tortoise():
    await Tortoise.init(config=tortoise_config)
    # await init_db()


@driver.on_shutdown
async def close_tortoise():
    await Tortoise.close_connections()