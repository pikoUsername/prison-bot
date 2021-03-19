from loguru import logger

from .rp import Prison
from .other import Events
from .fun import Coin
from .admin import Debugger

__all__ = "setup"

def setup(bot):
    logger.info("setuping Cogs")

    bot.add_cog(Prison(bot))
    bot.add_cog(Events(bot))
    bot.add_cog(Coin(bot))
    bot.add_cog(Debugger(bot))
