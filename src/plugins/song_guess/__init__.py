import os
from pathlib import Path

import nonebot
from nonebot import get_driver

from .config import Config
from src.providers.pathutil import data_path

driver = get_driver()
config = Config.parse_obj(driver.config)

_root_dir = data_path("song_guess")
_original_song_dir = _root_dir.joinpath("original")
_instrumental_song_dir = _root_dir.joinpath("instrumental")


@driver.on_bot_connect
async def init():
    if not os.path.exists(str(_root_dir)):
        os.makedirs(str(_root_dir))
    if not os.path.exists(str(_original_song_dir)):
        os.makedirs(str(_original_song_dir))
    if not os.path.exists(str(_instrumental_song_dir)):
        os.makedirs(str(_instrumental_song_dir))


def get_song_path(song_name: str) -> tuple[Path, Path]:
    return (_original_song_dir.joinpath(song_name), _instrumental_song_dir.joinpath(song_name))


_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").resolve())
)