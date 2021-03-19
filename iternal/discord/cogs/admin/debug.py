from discord.ext import commands


class Debugger(commands.Cog, name='pantry | Кладовка'):
    __slots__ = "bot",

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show_logs", help="shows last logs")
    @commands.is_owner()
    async def show_logs(self, ctx, file: str = None):
        if not file:
            return
        await self.bot.send_message(ctx.channel.id, "No text")

    @commands.group(name="i18n")
    @commands.is_owner()
    async def i18n(_, ctx):
        await ctx.send("No text...")
