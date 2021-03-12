from discord import Message

from ..util.middleware import BaseMiddleware


class Acl(BaseMiddleware):
    async def setup_chat(self, message: Message, data: dict) -> None:
        user_id = message.author.id

        data['user'] = _user

    async def on_pre_process_message(self, message: Message, data: dict):
        await self.setup_chat(message, data)
