import discord

from .db import db, TimedBaseModel
from iternal.discord.loader import bot

__all__ = "User",


class User(TimedBaseModel):
    __tablename__ = "users"

    # discord id
    uid = db.Column(db.BigInt(), index=True)
    first_name = db.Column(db.String(125))
    last_name = db.Column(db.String(125))
    money = db.Column(db.Integer(), default=0)
    exp = db.Column(db.Integer(), default=1)
    hp = db.Column(db.Integer(), default=100)

    @staticmethod
    async def get_user(uid: int, use_cache: bool = True):
        sql = "SELECT u.* FROM users AS u WHERE uid = $1;"

        if use_cache:
            user = await bot.storage.get_data(guild=None, user=uid)

        else:
            async with db.acquire() as conn:
                user = await conn.first(sql, uid)
        return user

    @staticmethod
    async def create_from_discord(user: discord.User, guild_id: int = None) -> "User":
        """
        Creates user's table from discord user

        :param user: discord.User class
        :param guild_id: better get to func this attr
        :return:
        """
        old_user = await User.get_user(user.id)
        if old_user:
            return old_user

        new_user = User(
            uid=user.id,
            first_name=user.display_name,
        )
        await new_user.create()
        await User.bot().storage.set_data(
            user=new_user.uid,
            guild=guild_id,
            data={"cache": new_user},
        )
        return new_user
