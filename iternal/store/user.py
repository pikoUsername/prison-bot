import discord
from sqlalchemy import sql, ForeignKey

from .db import db, TimedBaseModel
from iternal.discord.loader import bot
from pkg.middlewares.utils.other import current_message

__all__ = "User",


class User(TimedBaseModel):
    """
    user model, uses for registers user
    ID of user created in BaseModel, see BaseModel
    """
    __tablename__ = "users"

    # discord id
    uid = db.Column(db.BigInteger(), index=True)

    first_name = db.Column(db.String(125))
    last_name = db.Column(db.String(125))

    money = db.Column(db.Integer(), default=0)
    exp = db.Column(db.Integer(), default=1)
    hp = db.Column(db.Integer(), default=100)

    is_active = db.Column(db.Boolean(), server_default=sql.expression.false())
    prisons = db.ForeignKey('prisons', ondelete="NO ACTION", onupdate="NO ACTION")
    on_location = ForeignKey(
        'globallocation', ondelete='SET NULL', onupdate='NO ACTION'
    )

    respect = db.Column(db.Integer(), default=10)
    in_prison = db.Column(
        db.Boolean(),
        server_default=sql.expression.false()
    )  # ?
    reason = db.Column(db.String(53), default="No")

    @staticmethod
    async def get_user(uid: int, use_cache: bool = False):
        """
        Get user from cache, default uses cache
        create_from_discord caches result of creating
        and if use_cache is True, takes from cache

        * Use for just get, not for update, and etc.

        2* If you are using use_cache, then gets
           User Model object, not a asyncpg.Record

        :param uid:
        :param use_cache:
        :return:
        """
        if use_cache:
            mes = current_message.get(None)
            user = await bot.storage.get_data(guild=mes.guild.id, user=uid)
        else:
            sql = "SELECT u.* FROM users AS u WHERE uid = $1 LIMIT 1;"
            async with db.acquire() as conn:
                user = await conn.first(sql, uid)
        return user

    @staticmethod
    async def to_imprison(user_id: int) -> None:
        sql_exp = "UPDATE users SET in_prison WHERE uid = $1;"
        async with db.acquire() as conn:
            await conn.first(sql_exp, user_id)

    @staticmethod
    async def create_from_discord(
        user: discord.User, guild_id: int = None
    ) -> "User":
        """
        Creates user's table from discord user

        :param user: discord.User class
        :param guild_id: better get to func this attr
        :return:
        """
        # use_cache is False, bc KeyError
        old_user = await User.get_user(user.id, use_cache=False)
        if old_user:
            return old_user

        new_user = User(
            uid=user.id,
            first_name=user.display_name,
        )
        await new_user.create()

        # caches result
        await bot.storage.set_data(
            user=new_user.uid,
            guild=guild_id,
            data={"cache": new_user},
        )
        return new_user
