import os
from pathlib import Path

import nonebot
from nonebot import get_driver

from .config import Config
from src.providers.pathutil import data_path


driver = get_driver()
config = Config.parse_obj(driver.config)


@driver.on_bot_connect
async def init():
    if not os.path.exists(str(data_path("random_pictures"))):
        os.makedirs(str(data_path("random_pictures")))


def picture_folder_path(name: str) -> Path:
    return data_path("random_pictures").joinpath(name)


_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").resolve())
)