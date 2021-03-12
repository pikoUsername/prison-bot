from discord.ext import commands


class Prison(commands.Cog, name="prison | Тюрьма", help="Your home | Твой милый дом"):
    __slots__ = "bot",

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="How to Come to jail? Just get fuck up")
    async def start(self, ctx): pass
