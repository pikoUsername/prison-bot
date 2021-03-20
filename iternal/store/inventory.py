from sqlalchemy import sql

from .db import db, BaseModel, TimedBaseModel
from .user import User

__all__ = "Inventory", "Item", "GlobalItem", "Effect"


class Inventory(BaseModel):
    __tablename__ = "inventories"

    user_id = db.ForeignKey('users', ondelete="CASCADE", onupdate="NO ACTION")
    limit = db.Column(db.Integer(), default=20)

    @staticmethod
    async def get_user(inventory: "Inventory"):
        result = await User.query.where(
            User.uid == inventory.user_id
        ).gino.first()
        return result


class Item(TimedBaseModel):
    __tablename__ = "items"

    inventory_id = db.Column(db.Integer, db.ForeignKey("inventories.id"), null=False)
    equipped = db.Column(db.Boolean(), server_default=sql.false())
    item_parent = db.ForeignKey("globalitems", ondelete="CASCADE", onupdate="NO ACTION")


class GlobalItem(TimedBaseModel):
    __tablename__ = "globalitems"

    title = db.Column(db.String(125))
    description = db.Column(db.String(125))
    type = db.Column(db.String(20))
    effect_id = db.Column(db.Integer, db.ForeignKey("effects.id"))


class Effect(TimedBaseModel):
    __tablename__ = "effects"

    title = db.Column(db.String(125))
    # no minus effects
    hp = db.Column(db.Integer, default=0)
    # and other ...
