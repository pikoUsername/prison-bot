from discord.ext.commands import HelpCommand, BucketType, Cooldown
from discord.ext.commands.core import Command
from iternal.discord.util.paginator import Pages, BotHelpPageSource

class HelpMenu(Pages):
    __slots__ = ()

    def __init__(self, source):
        super().__init__(source)

class CustomHelp(HelpCommand):
    __slots__ = ()

    def __init__(self):
        super().__init__(command_attrs={'cooldown': Cooldown(1, 3.0, BucketType.member),'help': 'Показывает эту плашку'})

    async def get_command_signature(self, cmd: Command):
        text = f"{cmd.qualified_name}\n{cmd.description}"
        return text

    async def send_bot_help(self, mapping):
        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True)
        all_commands = {}
        for command in entries:
            if not command.cog:
                continue
            try:
                all_commands[command.cog].append(command)
            except:
                all_commands[command.cog] = [command]
        menu = HelpMenu(BotHelpPageSource(self, all_commands))
        await self.context.release()
        await menu.start(self.context)

