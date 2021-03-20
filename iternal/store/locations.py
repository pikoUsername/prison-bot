from .db import db, TimedBaseModel


class Location(TimedBaseModel):
    __tablename__ = "locations"


class GlobalLocation(TimedBaseModel):
    __tablename__ = "globallocation"

    title = db.Column(db.String(126), index=True)
    description = db.Column(db.String)
