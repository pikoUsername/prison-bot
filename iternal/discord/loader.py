from pathlib import Path

from data import config
from pkg.userstorage.memory import MemoryStorage

from ._bot import PrisonRpBot
from .middlewares.i18n import I18nMiddleware

__all__ = "bot", 'i18n', 'proj_root', 'prefix', '_'

# entry point for application is cli/manage.py or cli/__main__.py
proj_root = Path(__name__).parent.parent.parent

i18n = I18nMiddleware('bot', proj_root / "locales", default='ru')

_ = i18n.gettext

prefix = config['bot']['prefix']
bot = PrisonRpBot(config,
                  storage=MemoryStorage(),
                  command_prefix=prefix)
