from discord import Message

from ..util.middleware import BaseMiddleware

from iternal.store.user import User


class Acl(BaseMiddleware):
    async def setup_chat(self, message: Message, data: dict) -> None:
        user_id = message.author.id

        _user = await User.get_user(user_id)
        if not _user:
            await User.create_from_discord(message.author, message.guild.id)
            _user = await User.get_user(user_id)

        data['user'] = _user

    async def on_pre_process_message(self, message: Message, data: dict):
        await self.setup_chat(message, data)
