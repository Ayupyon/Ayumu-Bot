import asyncio
from io import BytesIO
from datetime import datetime, timedelta

from nonebot import require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

import src.plugins.song_guess.plugins.guess as guess


_players = {}


class Player(object):
    def __init__(self,
                 event: GroupMessageEvent,
                 server_bot: Bot,
                 level: int,
                 answer: str,
                 original: BytesIO,
                 instrumental: BytesIO):
        self._event = event
        self._server_bot = server_bot
        self._level = level
        self._answer = answer
        self._original = original
        self._instrumental = instrumental
        self._job = None

    @property
    def server_bot(self) -> Bot:
        return self._server_bot
    
    @property
    def event(self) -> GroupMessageEvent:
        return self._event
    
    @property
    def answer(self) -> str:
        return self._answer
    
    @property
    def original(self) -> BytesIO:
        return self._original
    
    @property
    def instrumental(self) -> BytesIO:
        return self.instrumental

    def timer_start(self):
        loop = asyncio.get_event_loop()
        self._job = loop.call_later(60, lambda: asyncio.ensure_future(guess.timeout_reaction(self)))

    def timer_stop(self):
        self._job.cancel()


async def add_player(player: Player):
    _players[player.event.user_id] = player
    print(_players)


async def remove_player(player: Player):
    _players.pop(player.event.user_id)


async def get_player(user_id: int) -> Player | None:
    return _players.get(user_id)