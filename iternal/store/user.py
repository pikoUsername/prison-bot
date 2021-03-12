from .db import db, TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    uid = db.Column(db.BigInt(), index=True)
    first_name = db.Column(db.String(125))
    last_name = db.Column(db.String(125))
    money = db.Column(db.Integer())
    xp = db.Column(db.Integer())

