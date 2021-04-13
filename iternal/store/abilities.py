"""
Abilities work like gta:sa
"""
from .db import db, BaseModel


class Ability(BaseModel):
    __tablename__ = "abilities"

    name = db.Column(db.String(125))
    description = db.Column(db.String)
    # types:
    # 1 << 2 is power
    # 1 << 3 is hp
    # 1 << 4 is speed, of craft and etc.
    # 1 << 5->20 is reserved special abilities, for example
    type = db.Column(db.Integer)
    xp = db.Column(db.Integer)


class UserAbility(BaseModel):
    __tablename__ = "user_abilities"

    parent_id = db.Integer(db.ForeignKey('alilities.id', ondelete="CASCADE", onupdate='NO ACTION'))
