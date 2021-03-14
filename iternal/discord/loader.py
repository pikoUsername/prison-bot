from data import config
from pkg.userstorage.memory import MemoryStorage

from ._bot import PrisonRpBot

__all__ = "bot",

prefix = config['bot']['prefix']
bot = PrisonRpBot(config,
                  storage=MemoryStorage(),
                  command_prefix=prefix)
