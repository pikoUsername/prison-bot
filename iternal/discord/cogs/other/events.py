from discord.ext.commands import errors
from discord.ext import commands

class Events(commands.Cog, name="events | Евенты"):
    __slots__ = "bot", "command_activated"

    def __init__(self, bot):
        self.bot = bot
        self.command_activated = 0x0
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     # for optimization
    #     args_errors = (
    #         errors.BadUnionArgument,
    #         errors.MissingRequiredArgument,
    #         errors.BadArgument,
    #         errors.TooManyArguments
    #     )
    #
    #     ignore_errors = (
    #         errors.RoleNotFound,
    #         errors.CommandNotFound,
    #         errors.CommandOnCooldown,
    #         errors.ChannelNotFound
    #     )
    #     if isinstance(error, ignore_errors):
    #         pass
    #     elif isinstance(error, args_errors):
    #         await ctx.send("``Argument Error``, Проебался, что то пропустил в аргментах")
    #     elif isinstance(error, commands.NotOwner):
    #         await ctx.reply(embed=Embed(title="Доступ запрещен",description=f"{ctx.command}, Только Для Оффицеров"))
    #     elif isinstance(error, commands.CommandInvokeError):
    #         if isinstance(error.original, AssertionError):
    #             await ctx.reply(error)
    #         else:
    #             await ctx.reply(f"Ну что же, у нас проблемки. {error}")
    #             owner = await self.bot.fetch_user(self.bot.owner_id)
    #             text = "У нас проблема, в тюрьме: {g_id}, и эта проблема: {error}".format(g_id=ctx.guild.id, error=error)
    #             await owner.send(text)
    #     else:
    #         await ctx.reply(f"Как ты это Сделал это? {error}\n")
    #         owner = await self.bot.fetch_user(self.bot.owner_id)
    #         text = "У нас проблема, в тюрьме: {g_id}, и эта проблема: {error}".format(g_id=ctx.guild.id, error=error)
    #         await owner.send(text)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err: Exception):
        s = "``Argument Error``, Проебался, что то пропустил в аргментах"
        err_dict = {
            errors.CommandInvokeError: None,
            errors.RoleNotFound: s,
            errors.CommandNotFound: s,
            errors.CommandOnCooldown: s,
            errors.ChannelNotFound: s,
        }

        result = err_dict.get(err, None)

        if result is None:
            await ctx.reply(f"Как ты это Сделал это? {err}\n")
            owner = await self.bot.fetch_user(self.bot.owner_id)
            text = "У нас проблема, в тюрьме: {g_id}, и эта проблема: {error}".format(g_id=ctx.guild.id, error=error)
            await owner.send(text)
            return

        if callable(result):
            await result()
            return

        await ctx.send(result)

    @commands.Cog.listener()
    async def on_command_complete(self, *_):
        # and too this
        self.command_activated += 0x1
