import discord

from .db import db, TimedBaseModel


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
    async def get_user(uid: int):
        sql = "SELECT u.* FROM users AS u WHERE uid = $1;"
        async with db.acquire() as conn:
            user = await conn.first(sql, uid)
        return user

    @staticmethod
    async def create_from_discord(user: discord.User) -> "User":
        old_user = await User.get_user(user.id)
        if old_user:
            return old_user

        new_user = User(
            uid=user.id,
            first_name=user.display_name,
        )
        await new_user.create()
        return new_user
