from datetime import datetime, date, timedelta

from tortoise import fields
from tortoise.models import Model


def prev_day() -> date:
    return datetime.now().date() - timedelta(days=1)


class User(Model):
    id = fields.BigIntField(pk=True)
    star = fields.IntField(default=0)
    checkin_days = fields.IntField(default=0)
    last_checkin = fields.DateField(default=prev_day)
    checkin_token = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "users"

    def __str__(self):
        return {
            "id": self.id,
            "star": self.star,
            "checkin_days": self.checkin_days,
            "last_checkin": self.last_checkin,
            "checkin_token": self.checkin_token,
        }.__str__()