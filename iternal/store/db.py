import datetime
import sqlalchemy as sa

from gino import Gino


db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(True), default=datetime.datetime.now)
    update_at = sa.Column(
        sa.DateTime(True),
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
    )
