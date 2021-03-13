import datetime
from contextlib import suppress

from sqlalchemy import sql
from gino import Gino, GinoEngine, UninitializedError
from loguru import logger

from iternal.discord.util import Bot
from data import config


db = Gino()


class BaseModel(db.Model):
    __abstract__ = 1  # type: bool
    query: sql.Select

    id = db.Column(db.Integer(), db.Sequence("user_id_seq"), index=True, primary_key=True)

    @property
    def bot(self):
        b = Bot.get_current()
        assert b is not None, "No bot from context, make set_current(bot) for this."
        return b


class TimedBaseModel(BaseModel):
    __abstract__ = 1  # type: bool

    created_at = db.Column(db.DateTime(1), default=datetime.datetime.now)
    update_at = db.Column(
        db.DateTime(1),
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
    )


async def on_startup(bot: Bot):
    dsn: str = config.create_dsn()
    pool: GinoEngine = await db.set_bind(dsn)
    bot['pool'] = pool
    await db.gino.create_all()


async def on_shutdown(_: Bot):
    with suppress(UninitializedError):
        logger.info("Closing Postgres Connection")
        await db.pop_bind().close()


def setup(bot: Bot):
    logger.info("Setuping Database.")

    bot.on_startup(on_startup)
    bot.on_shutdown(on_shutdown)
