from discord import Message
from pkg.middlewares.middleware import BaseMiddleware

from iternal.store.user import User
from iternal.store.prison import Prison


class Acl(BaseMiddleware):
    async def setup_chat(self, message: Message, data: dict) -> None:
        _user = await User.get_user(message.author.id, False)
        if not _user:
            await User.create_from_discord(message.author, message.guild.id)

        _prison = await Prison.get_prison(message.guild.id)
        if not _prison:
            await Prison.create_from_guild(message.guild)

        data['user'] = _user
        data['prison'] = data['guild'] = _prison

    async def on_post_process_message(self, message: Message, data: dict):
        await self.setup_chat(message, data)
