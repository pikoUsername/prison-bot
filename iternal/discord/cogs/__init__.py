from loguru import logger as logger

from .rp import Prison as Prison
from .other import Events as Events
from .fun import Coin as Coin
from .admin import Debugger, Owner

__all__ = "setup"


def setup(bot):
    logger.info("setuping Cogs")

    bot.add_cog(Prison(bot))
    bot.add_cog(Events(bot))
    bot.add_cog(Coin(bot))
    bot.add_cog(Debugger(bot))
    bot.add_cog(Owner(bot))
