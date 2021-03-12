from discord import Message

from ..util.middleware import BaseMiddleware


class Acl(BaseMiddleware):
    async def on_pre_process(self, message: Message, data: dict):
        await self.setup_chat(message, data)
