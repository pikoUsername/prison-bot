from typing import Optional

from discord import Guild, Message

from sqlalchemy import CheckConstraint
from sqlalchemy.sql import expression

from pkg.middlewares.utils import current_message
from .db import db, TimedBaseModel

__all__ = "Prison",


def _check_lang(lang: str):
    if lang in ('ru', 'en'):
        return True
    return


class Prison(TimedBaseModel):
    """
    Represents Guild object, as prison
    """
    __tablename__ = "prison"

    gid = db.Column(db.BigInteger, index=True)
    officer_id = db.Column(db.BigInteger)
    name = db.Column(db.String(125))
    description = db.Column(db.String(2048))
    prison_id = db.Column(db.Integer, CheckConstraint('prison_id < 100'))
    language = db.Column(db.String(10), default="ru")

    # строгого, общего
    # or an english
    # hard, general
    mode = db.Column(db.String())

    lock_down = db.Column(db.Boolean(), server_default=expression.false())

    @staticmethod
    async def get_prison(gid: int):
        # not using cache, bc this meth uses not so much
        sql = "SELECT p.* FROM prison AS p WHERE gid = $1 LIMIT 1;"
        async with db.acquire() as conn:
            prison = await conn.first(sql, gid)
        return prison

    @staticmethod
    async def create_from_guild(guild: Optional[Guild] = None):
        if not guild:
            _mes: Message = current_message.get()
            if _mes is None:
                raise TypeError("No current_message context get.")
            _guild = _mes.guild
        else:
            _guild = guild

        _prison = await Prison.get_prison(_guild.id)
        if _prison is not None:
            return _prison

        new_prison = Prison()
        new_prison.gid = _guild.id
        new_prison.description = _guild.description
        new_prison.name = _guild.name

        return new_prison

    @staticmethod
    async def change_lang(lang: str, gid: int):
        if _check_lang(lang):
            langs = 'ru', 'en'
            raise TypeError(f"Not available language, language must be in {langs}")

        sql = f'UPDATE {Prison.__tablename__} SET language = $1 WHERE gid = $2;'
        await Prison.request(sql, lang, gid, execute=True)
