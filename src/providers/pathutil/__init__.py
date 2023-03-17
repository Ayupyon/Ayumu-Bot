import os
from pathlib import Path
from functools import cache

from nonebot import get_driver


ayumu_home = Path(os.getcwd())
driver = get_driver()


@driver.on_startup
async def init_home_path():
    if not os.path.exists(str(resource_path())):
        os.makedirs(str(resource_path()))
    if not os.path.exists(str(data_path())):
        os.makedirs(str(data_path()))


@cache
def resource_path(path: Path | str="") -> Path:
    assert ayumu_home, "home path isn't initialized"
    return ayumu_home.joinpath("resources", path)


@cache
def data_path(path: Path | str="") -> Path:
    assert ayumu_home, "home path isn't initialized"
    return ayumu_home.joinpath("data", path)