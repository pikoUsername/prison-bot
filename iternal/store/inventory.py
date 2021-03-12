from .db import db, BaseModel, TimedBaseModel


class Inventory(BaseModel):
    __tablename__ = "inventories"

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))


class Item(TimedBaseModel):
    __tablename__ = "items"

    inventories = db.ForeignKey("inventories")
    equipped = None


class GlobalItem(TimedBaseModel):
    __tablename__ = "globalitems"

    title = db.Column(db.String(125))
    description = db.Column(db.String(125))
    type = db.Column(db.String(20))
    damage = db.Column
