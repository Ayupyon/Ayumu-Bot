from nonebot import get_driver
from nonebot import on_command, on_message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Bot,
    Message,
    MessageSegment
)
from nonebot.adapters.onebot.v11.permission import GROUP

from .config import Config
from src.plugins.song_guess.model import Song, SongAlias

global_config = get_driver().config
config = Config.parse_obj(global_config)

set_alias = on_command("设置歌曲别名", priority=5, permission=GROUP)


@set_alias.handle()
async def _(args: Message=CommandArg()):
    song, alias = args.extract_plain_text().split(' ', 2)
    if not await Song.exists(song=song):
        if not await SongAlias.exists(alias=song):
            await set_alias.send("小步梦找不到这首歌哦")
            return
        else:
            song = (await SongAlias.get(alias=song)).song
    song_alias, create = await SongAlias.get_or_create(defaults={"song": song}, alias=alias)
    if create:
        await set_alias.send(f"成功为 {song} 添加别名 {alias}!")
    else:
        await set_alias.send(f"该别名已经被设置为 {song_alias.song} 的别名了！")