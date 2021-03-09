import random

from discord.ext import commands

COINS = "решка", "орел"

class Coin(commands.Cog, name="coin | Монетка"):
    __slots__ = "bot", "sys_random"

    def __init__(self, bot):
        self.bot = bot
        self.sys_random = random.SystemRandom()

    @commands.command(name="coin")
    async def coin(self, ctx, excepted):
        assert excepted in COINS, "Большой и толстый Хер"

        rand_coin = self.sys_random.randint(0, 1)
        result = COINS[rand_coin]
        if result != excepted:
            return await ctx.reply(f"Посмотрим, что тут у нас, {result} Вы умрете")

        await ctx.reply(f"Посмотрим, что у вас выпало, {result} Поздравляю, вас не трахнут")

    @commands.command(name="bottle")
    async def bottle_flip(self, ctx):
        if self.sys_random.random() > .8:
            return await ctx.reply("Опа, тебе повеззло")

        await ctx.reply("Сядешь на бутылку")
