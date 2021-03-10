import datetime
from contextlib import suppress
from typing import Any

from gino import Gino, GinoEngine, UninitializedError
from loguru import logger

from iternal.discord.util import Bot
from data import config


db = Gino()


class BaseModel(db.Model):
    __abstract__ = 1


class TimedBaseModel(BaseModel):
    __abstract__ = 1

    created_at = db.Column(db.DateTime(1), default=datetime.datetime.now)
    update_at = db.Column(
        db.DateTime(1),
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
    )


async def on_startup(bot: Bot):
    dsn: str = config.create_dsn()
    pool: GinoEngine = await db.set_bind(dsn)
    await db.gino.create_all()


async def on_shutdown(_: Any):
    with suppress(UninitializedError):
        logger.info("Closing Postgres Connection")
        await db.pop_bind().close()


def setup(bot):
    logger.info("Setuping Database.")

    bot.on_startup(on_startup)
    bot.on_shutdown(on_shutdown)
