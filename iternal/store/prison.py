from sqlalchemy import CheckConstraint
from sqlalchemy.sql import expression

from .db import db, TimedBaseModel


class Prison(TimedBaseModel):
    """
    Represents Guild object, as prison
    """
    __tablename__ = "prison"

    gid = db.Column(db.BigInteger(), index=True, null=False)
    name = db.Column(db.String(125))
    description = db.Column(db.String(2048))
    prison_id = db.Column(db.Integer, CheckConstraint('prison_id < 100'))

    # строгого, общий
    # or an english
    # hard, general
    mode = db.Column(db.String())

    lock_down = db.Column(db.Boolean(), server_default=expression.false)
