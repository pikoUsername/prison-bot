from .rp import Prison
from .other import Events
from .fun import Coin
from .admin import Debugger


def setup(bot):
    bot.add_cog(Prison(bot))
    bot.add_cog(Events(bot))
    bot.add_cog(Coin(bot))
    bot.add_cog(Debugger(bot))
