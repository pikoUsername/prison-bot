import asyncio
import discord
from contextlib import suppress
from discord.ext import menus

class BotHelpPageSource(menus.ListPageSource):
    __slots__ = "commands", "help_command", "prefix"

    def __init__(self, help_command, commands):
        super().__init__(entries=sorted(commands.keys(), key=lambda c: c.qualified_name), per_page=6)
        self.commands = commands
        self.help_command = help_command
        self.prefix = help_command.clean_prefix

    def format_commands(_, cog, commands):
        short_doc = cog.description.split('\n', 1)[0] + '\n' if cog.description else 'Хуй те, а не помощь\n'
        current_count = len(short_doc)
        ending_note = '+%d нет'
        ending_length = len(ending_note)
        page = []
        for command in commands:
            value = f'``{command.name}``'
            count = len(value) + 1 # The space
            if count + current_count < 800:
                current_count += count
                page.append(value)
            else:
                if current_count + ending_length + 1 > 800:
                    page.pop()
                break
        [cmds_len, page_len] = len(commands), len(page)
        if page_len == cmds_len:
            return short_doc + ' '.join(page)
        hidden = cmds_len - page_len
        return short_doc + ' '.join(page) + '\n' + (ending_note % hidden)

    async def format_page(self, menu, cogs):
        prefix = menu.ctx.prefix
        description = (f'"{prefix}help <command>" ну что же, документация действий вот здесь, если захочешь найдешь.' 
                      f'Поиспользуй это "{prefix}help category" для того что бы не запутатся.')
        embed = discord.Embed(title='Категории',description="\n".join(description),colour=discord.Colour.blurple())
        for cog in cogs:
            commands = self.commands.get(cog)
            if commands:
                value = self.format_commands(cog, commands)
                embed.add_field(name=cog.qualified_name, value=value, inline=True)
        maximum = self.get_max_pages()
        embed.set_footer(text=f'Page {menu.current_page + 1}/{maximum}')
        return embed

class Pages(menus.MenuPages):
    def __init__(self, source):
        super().__init__(source=source, check_embeds=True)
    async def finalize(self, timed_out):
        with suppress(discord.HTTPException):
            if timed_out:
                await self.message.clear_reactions()
            else:
                await self.message.delete()

    @menus.button('\N{INFORMATION SOURCE}\ufe0f', position=menus.Last(3))
    async def show_help(self, _):
        """shows this message"""
        embed = discord.Embed(title='Помощь от Батиной книги');messages = []
        for emoji, button in self.buttons.items():
            messages.append(f'{emoji}: {button.action.__doc__}')
        embed.add_field(name='Для чего это кнопкочка?', value='\n'.join(messages), inline=False)
        embed.set_footer(text=f'Ты на странице - {self.current_page + 1}.')
        await self.message.edit(content=None, embed=embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_page(self.current_page)
        self.bot.loop.create_task(go_back_to_current_page())

    @menus.button('\N{INPUT SYMBOL FOR NUMBERS}', position=menus.Last(1.5))
    async def numbered_page(self, payload):
        """lets you type a page number to go to"""
        channel = self.message.channel
        author_id = payload.user_id
        to_delete = [await channel.send('Полистай побольше, может найдешь что то годное')]
        def message_check(m):
            # check out, for author_id and channel, and content is it digit()
            return (m.author.id == author_id and channel == m.channel and m.content.isdigit())
        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except asyncio.TimeoutError:
            to_delete.append(await channel.send('Ты проебался, ты проебал страницу.'))
            await asyncio.sleep(5)
        else:
            page = int(msg.content)
            to_delete.append(msg)
            await self.show_checked_page(page - 1)
        with suppress(Exception):
            await channel.delete_messages(to_delete)
