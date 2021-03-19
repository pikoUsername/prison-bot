from discord import Message
from pkg.middlewares.middleware import BaseMiddleware

from iternal.store.user import User
from iternal.store.prison import Prison


class Acl(BaseMiddleware):
    async def setup_chat(self, message: Message, data: dict) -> None:
        user_id = message.author.id

        _user = await User.get_user(user_id)
        if not _user:
            await User.create_from_discord(message.author, message.guild.id)

        _prison = await Prison.get(message.guild.id)
        if not _prison:
            await Prison.create_from_guild(message.guild)

        data['user'] = _user
        data['prison'] = data['guild'] = None

    async def on_pre_process_message(self, message: Message, data: dict):
        await self.setup_chat(message, data)
