from tortoise import fields
from tortoise.models import Model


class PictureName(Model):
    name = fields.CharField(max_length=20, pk=True)

    class Meta:
        table = "picture_name"


class PictureAlias(Model):
    alias = fields.CharField(max_length=20, pk=True)
    name = fields.CharField(max_length=20)

    class Meta:
        table = "picture_alias"


async def get_name(name_or_alias: str) -> str | None:
    name = await PictureName.get_or_none(name=name_or_alias)
    if name is not None:
        return name.name
    alias = await PictureAlias.get_or_none(alias=name_or_alias)
    if alias is not None:
        return alias.name
    return None