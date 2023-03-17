from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.sqlite.functions import Random


class Song(Model):
    song = fields.CharField(max_length=50, pk=True)

    class Meta:
        table = "songs"


class SongAlias(Model):
    song = fields.CharField(max_length=50)
    alias = fields.CharField(max_length=50, pk=True)

    class Meta:
        table = "song_aliases"


async def get_random_song() -> str:
    return (await Song.annotate(order=Random()).order_by("order").first()).song


async def check_answer(player_answer: str, correct_answer: str) -> bool:
    if player_answer == correct_answer:
        return True
    alias = await SongAlias.get_or_none(alias=player_answer)
    if alias is not None and alias.song == correct_answer:
        return True
    return False


async def get_alias_list(name: str) -> list[str]:
    res = await SongAlias.filter(song=name)
    return [song_alias.alias for song_alias in res]