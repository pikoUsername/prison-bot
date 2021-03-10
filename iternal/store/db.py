import datetime
from typing import Any

from gino import Gino, GinoEngine
from loguru import logger

from iternal.discord.util import Bot
from data import config


db = Gino()


class BaseModel(db.Model):
    __abstract__ = True


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), default=datetime.datetime.now)
    update_at = db.Column(
        db.DateTime(True),
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
    )


async def on_startup(bot: Bot):
    pool: GinoEngine = await db.set_bind(config.create_dsn())
    bot['db_pool'] = pool
    await db.gino.create_all()


async def on_shutdown(_: Any):
    await db.pop_bind().close()


def setup(bot):
    logger.info("Setuping Database.")
    bot.on_startup(on_startup)
    bot.on_shutdown(on_shutdown)
