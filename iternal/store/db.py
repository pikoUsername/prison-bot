import datetime
from typing import TypeVar, List, Union
from contextlib import suppress
import warnings

import asyncpg
from sqlalchemy import sql
import sqlalchemy as sa
from gino import Gino, GinoEngine, UninitializedError
from loguru import logger

# for not raise cuircular imports
from pkg.middlewares import MiddlewareBot as Bot
from data import config


# query result
QR = TypeVar("QR")

db = Gino()


class BaseModel(db.Model):
    __abstract__ = 1  # type: bool
    query: sql.Select

    id = db.Column(db.Integer(), unique=True, index=True, primary_key=True)

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

    @staticmethod
    async def request(
        query: str,
        *params,
        fetch: bool = 0,
        execute: bool = 0,
        model=None,
        **kwargs,
    ) -> Union[QR, List[QR]]:
        self = BaseModel
        result = await self._request(query, params, fetch, execute, **kwargs)

        if model is not None and not execute:
            return model(*result)

        return result

    @staticmethod
    async def _request(query, params, fetch, execute, **kwargs):
        """
        request to database, and etc.
        """
        if execute and fetch:
            warnings.warn("Fetch and execute, is True, "
                          "and it s have not got any efficient.")

        if not execute and not fetch:
            warnings.warn("Fetch and execute is False, it s does not have any effect")

        async with db.bind.acquire() as conn:
            conn: asyncpg.Connection
            async with conn.transaction():
                result = None
                if fetch:
                    result = await conn.fetchrow(query, *params, **kwargs)
                if execute:
                    await conn.execute(query, *params, **kwargs)
                return result


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
