from discord.ext import commands as commands
from .utils.consts import COINS as COINS

from iternal.discord.loader import _ as __


class Coin(commands.Cog, name="coin | Монетка"):
    __slots__ = "bot", "sys_random"

    def __init__(self, bot):
        # on windows __import__ faster for 30% than just import
        random = __import__("random")

        self.bot = bot
        self.sys_random = random.SystemRandom()

    @commands.command(name="coin", help="Coin Flip")
    async def coin(self, ctx, excepted):
        assert excepted in COINS, __("Большой и толстый Хер")

        rand_coin = self.sys_random.randint(0x0, 0x1)
        result = COINS[rand_coin]
        if result != excepted:
            return await ctx.reply(__(
                "Посмотрим, что тут у нас, {result}, Ты сдохнешь"
            ).format(result=result))

        await ctx.reply(__(
            "Посмотрим, что у вас выпало, {result} Поздравляю, вас не трахнут"
        ).format(result=result))

    @commands.command(name="bottle", help="you need at sit on bottle")
    async def bottle_flip(self, ctx):
        if self.sys_random.random() > .8:
            return await ctx.reply("Опа, тебе повезло")

        await ctx.reply("Сядешь на бутылку")
