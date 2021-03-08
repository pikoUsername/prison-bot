from .util import Bot, CustomHelp
from .cogs import setup

class PrisonRpBot(Bot):
    __slots__ = "config",

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.help_command = CustomHelp()

    async def start(self, *args, **kwargs):
        token = self.config['bot']['TOKEN']
        # cogs setup
        setup(self)
        await super().start(token, *args, **kwargs)
