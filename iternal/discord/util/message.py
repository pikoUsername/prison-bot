from discord import Message
from discord.ext.commands import Command, Context


class DateMessage(Message):
    ctx_data = dict()

    __getitem__ = lambda s, k: s.ctx_data[k]

    def __setitem__(self, key, value):
        self.ctx_data[key] = value

    def __delitem__(self, key):
        del self.ctx_data[key]


class CustomCommand(Command):
    pass
