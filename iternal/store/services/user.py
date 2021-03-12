from gino import GinoEngine

from ..db import db


class UserModelApi:
    """
    Wrapper for contact with user model
    """
    @staticmethod
    def prepare_sql(query: str):
        if not query.endswith(";"):
            query += ";"
        return query

    @staticmethod
    async def get_user(uid: int):
        sql = UserModelApi.prepare_sql("SELECT u.* FROM users AS u WHERE uid = $1;")
        async with db.acquire() as conn:
            conn: GinoEngine
            user = await conn.first(sql, uid)
        return user
