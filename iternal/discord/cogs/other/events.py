from discord.ext.commands import errors
from discord import Embed, Message
from discord.ext import commands

from iternal.discord.loader import _


class Events(commands.Cog, name="events | Евенты"):
    __slots__ = "bot", "command_activated"

    def __init__(self, bot):
        self.bot = bot
        self.command_activated = 0

    async def send_to_owner(
        self,
        *args, **kwargs
    ):
        owner = await self.bot.fetch_user(self.bot.owner_id)
        return await owner.send(*args, **kwargs)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        args_errors = (
            errors.BadUnionArgument,
            errors.MissingRequiredArgument,
            errors.BadArgument,
            errors.TooManyArguments
        )

        ignore_errors = (
            errors.RoleNotFound,
            errors.CommandNotFound,
            errors.CommandOnCooldown,
            errors.ChannelNotFound
        )

        if isinstance(error, ignore_errors):
            return
        elif isinstance(error, args_errors):
            await ctx.send(_("``Argument Error``, Проебался, что то пропустил в аргментах"))
        elif isinstance(error, commands.NotOwner):
            await ctx.reply(embed=Embed(
                title=_("Доступ запрещен"),
                description=_("{command}, Только Для Оффицеров"
                              ).format(command=ctx.command)
            ))
        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, AssertionError):
                await ctx.reply(error)
            else:
                await ctx.reply(_("Ну что же, у нас проблемки. {error}").format(error=error))
        else:
            await ctx.reply(f"Как ты это Сделал это? {error}\n")
            text = _(
                "У нас проблема, в тюрьме: {g_name}, и эта проблема: {error}"
            ).format(g_name=ctx.guild.name, error=error)
            await self.send_to_owner(text)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_command_complete(self, *_):
        # and too this
        self.command_activated += 1
