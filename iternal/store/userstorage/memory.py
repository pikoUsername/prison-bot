import typing
import copy

from .base import BaseStorage


class MemoryStorage(BaseStorage):
    __slots__ = "data",

    def __init__(self):
        self.data = {}

    def resolve_address(self, guild, user):
        chat_id, user_id = map(str, self.check_address(guild=guild, user=user))

        if chat_id not in self.data:
            self.data[chat_id] = {}
        if user_id not in self.data[chat_id]:
            self.data[chat_id][user_id] = {'state': None, 'data': {}, 'bucket': {}}

        return chat_id, user_id

    async def get_data(self, *,
                       guild: typing.Union[str, int, None] = None,
                       user: typing.Union[str, int, None] = None,
                       default: typing.Optional[str] = None) -> typing.Dict:
        chat, user = self.resolve_address(guild=guild, user=user)
        return copy.deepcopy(self.data[chat][user]['data'])

    async def update_data(self, *,
                          guild: typing.Union[str, int, None] = None,
                          user: typing.Union[str, int, None] = None,
                          data: typing.Dict = None, **kwargs):
        if data is None:
            data = {}
        chat, user = self.resolve_address(guild=guild, user=user)
        self.data[chat][user]['data'].update(data, **kwargs)

    async def set_data(self, **kwargs):
        for k, v in kwargs.items():
            self.data[k] = v

    async def wait_closed(self): pass

    async def close(self):
        self.data.clear()
