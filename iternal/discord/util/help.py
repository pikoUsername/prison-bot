"""
Copy Paste from R.Danny,
who cares? About it, so much
I guess R.Danny licinse not so strict
"""
import discord
from discord.ext import menus
from discord.ext.commands import HelpCommand, BucketType, Cooldown, Command
from iternal.discord.util.paginator import Pages, BotHelpPageSource
from iternal.discord.loader import _

__all__ = "HelpMenu", "CustomHelp"


class HelpMenu(Pages): pass


class GroupHelpPageSource(menus.ListPageSource):
    __slots__ = "group", "prefix", "title", "description"

    def __init__(self, group, commands, *, prefix):
        super().__init__(entries=commands, per_page=6)
        self.group = group
        self.prefix = prefix
        self.title = _('{qualified_name} Комманд').format(self.group.qualified_name)
        self.description = self.group.description

    async def format_page(self, menu, commands):
        embed = discord.Embed(title=self.title, description=self.description, colour=discord.Colour.blurple())

        for command in commands:
            signature = f'{command.qualified_name} {command.signature}'
            embed.add_field(name=signature, value=command.short_doc or 'Мыло на шыло...', inline=False)

        maximum = self.get_max_pages()
        if maximum > 1:
            embed.set_author(name=_(
                'Бутылка {current_page}/{maximum} ({entries}) Всего)')
                    .format(
                        current_page=menu.current_page + 1,
                        maximum=maximum,
                        entries=len(self.entries)
                    )
            )

        embed.set_footer(text=_('Юзай "{prefix}help <Действие>" for more info on a command.').format(prefix=self.prefix))
        return embed


class CustomHelp(HelpCommand):
    __slots__ = ()

    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': Cooldown(1, 3.0, BucketType.member),
            'help': 'Показывает эту плашку'}
        )

    def get_command_signature(self, command: Command):
        """
        Take some Attributes from Command

        :param command:
        :return: <string>
        """
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'{command.name} | {aliases}'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        if len(entries) == 0:
            return await self.send_command_help(group)

        source = GroupHelpPageSource(group, entries, prefix=self.clean_prefix)
        self.common_command_formatting(source, group)
        menu = HelpMenu(source)
        await self.context.release()
        await menu.start(self.context)

    def common_command_formatting(self, embed_like, command: Command):
        embed_like.title = self.get_command_signature(command)
        if command.description:
            embed_like.description = f'{command.description}\n\n{command.help}'
        else:
            embed_like.description = command.help or 'Зачем описание...'

    async def send_command_help(self, command: Command):
        # No pagination necessary for a single command.
        embed = discord.Embed(colour=discord.Colour.blurple())
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

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
        await menu.start(self.context)
