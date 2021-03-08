import random

from discord import Embed
from discord.ext import commands

COINS = "решка", "орел"


class Coin(commands.Cog, name="coin | Монетка"):
    __slots__ = "bot", "sys_random"

    def __init__(self, bot):
        self.bot = bot
        self.sys_random = random.SystemRandom()

    @commands.command(name="coin")
    async def coin(self, ctx: commands.Context, excepted):
        assert excepted in COINS, "Ваше ожидание, не правильные"

        rand_coin = self.sys_random.randint(0, 1)
        result = COINS[rand_coin]

        if result != excepted:
            text = f"Посмотрим, что тут у нас, {result} Вы умрете"
            await ctx.reply(text)
            return

        text = f"Посмотрим, что у вас выпало, {result} Поздравляю, вас не трахнут"
        await ctx.reply(text)

    @commands.command(name="bottle")
    async def bottle_flip(self, ctx: commands.Context):
        chance = .8

        if self.sys_random.random() > chance:
            text = "Опа, тебе повеззло"
            return await ctx.reply(text)

        text = "Сядешь на бутылку"
        await ctx.reply(text)
