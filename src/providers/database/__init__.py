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
                "src.plugins.song_guess.model",
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
    from src.plugins.song_guess.model import Song, SongAlias
    import json, asyncio

    # async def add_alias(song: str, alias: str):
    #     await SongAlias.create(song=song, alias=alias)

    # with open("data.json", "r") as file:
    #     res = json.load(file)
    #     for entry in res:
    #         name, aliases = entry
    #         await Song.create(song=name)
    #         tasks = [add_alias(name, alias) for alias in aliases]
    #         await asyncio.gather(*tasks)
    # song = await Song.get(song="めっちゃGoing")
    # await song.delete()
    # s = await SongAlias.filter(song="めっちゃGoing")
    # for e in s:
    #     e.song = "めっちゃGoing!!"
    #     await e.save()


@driver.on_startup
async def init_tortoise():
    await Tortoise.init(config=tortoise_config)
    await init_db()


@driver.on_shutdown
async def close_tortoise():
    await Tortoise.close_connections()