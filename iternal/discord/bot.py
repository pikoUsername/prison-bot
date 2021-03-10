from .util import Bot, CustomHelp
from . import cogs

from ..store import db


class PrisonRpBot(Bot):
    __slots__ = "config",

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.help_command = CustomHelp()

    async def start(self, *args, **kwargs):
        token = self.config['bot']['TOKEN']

        db.setup(self)
        cogs.setup(self)

        await super().start(token, *args, **kwargs)
