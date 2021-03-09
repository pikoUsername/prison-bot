import sqlalchemy as sa

from gino import Gino


db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime(True))
