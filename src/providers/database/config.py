from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    db_url: str