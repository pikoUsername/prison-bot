from typing import Optional

from discord import Guild, Message

from sqlalchemy import CheckConstraint
from sqlalchemy.sql import expression

from pkg.middlewares.utils import current_message
from .db import db, TimedBaseModel


class Prison(TimedBaseModel):
    """
    Represents Guild object, as prison
    """
    __tablename__ = "prison"

    gid = db.Column(db.BigInteger(), index=True, null=False)
    officer_id = db.Column(db.BitInteger())
    name = db.Column(db.String(125))
    description = db.Column(db.String(2048))
    prison_id = db.Column(db.Integer, CheckConstraint('prison_id < 100'))
    language = db.Column(db.String(10), default="ru")

    # строгого, общего
    # or an english
    # hard, general
    mode = db.Column(db.String())

    lock_down = db.Column(db.Boolean(), server_default=expression.false)

    @staticmethod
    async def get_prison(gid: int):
        sql = "SELECT u.* FROM users AS u WHERE uid = $1 LIMIT 1;"
        async with db.acquire() as conn:
            prison = await conn.first(sql, gid)
        return prison

    @staticmethod
    async def create_from_guild(guild: Optional[Guild] = None):
        if not guild:
            _mes: Message = current_message.get()
            if _mes is None:
                raise TypeError("No current_message context took.")
            _guild = _mes.guild
        else:
            _guild = guild

        _prison = await Prison.get(_guild.id)
        if _prison is not None:
            return _prison

        new_prison = Prison()
        new_prison.gid = _guild.id
        new_prison.description = _guild.description
        new_prison.name = _guild.name

        return new_prison
