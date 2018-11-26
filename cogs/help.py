import json

import discord
from discord.ext import commands

from constants import Strings
from library import crc


class Help:
    def __init__(self, bot):
        self.bot = bot
        self.current_crc = ''  # Current hash of help.json
        self.help_list = {}  # Dictionary of all commands and their usage
        self.command_list = []  # List of available commands

    @commands.command()
    async def help(self, ctx, args: str = '', public=''):
        embed = discord.Embed(colour=0x4ba139)  # Create empty embed

        new_crc = crc('help.json')  # CRC of help.json
        if self.current_crc != new_crc:  # If help.json has been changed
            self.current_crc = new_crc  # Set hash to the new changes
            with open('help.json') as f:  # Open help.json
                self.help_list = json.load(f)  # Load the JSON data
            for key, value in self.help_list['categories'].items():
                for key2, value2 in value['commands'].items():
                    self.command_list.append(key2.replace(' ', '').lower())

        if args == '' or args == 'public':
            title = f':{self.help_list["warning"]["icon"]}: __**Note**__'
            content = self.help_list["warning"]["description"] + '\n\n_'
            embed.add_field(name=title, value=content)  # add Warning help information to embed
            for key, value in self.help_list['categories'].items():
                title = f':{value["icon"]}: __**{key} Commands**__'
                content = '\n\n'.join([f'`{value2["usage"]}` - {value2["short"]}' for key2, value2 in value['commands'].items()]) + '\n\n_'
                embed.add_field(name=title, value=content)

        else:
            if args in self.command_list:
                for key, value in self.help_list['categories'].items():
                    for key2, value2 in value['commands'].items():
                        if args == key2.replace(' ', '').lower():
                            content = f'`{value2["usage"]}` - {value2["description"]}'  # `usage` - description
                            if value2['examples']:  # If there are examples for the command
                                content += '\n\n' + '*' + 'Examples:' + '* ' + '\n' + '\n'.join(['`' + value3 + '`' for key3, value3 in value2['examples'].items()])  # *Examples:* `example1`, `example2`, `example3`

                            if value2['aliases']:  # If there are aliases for the command
                                content += '\n\n' + '*' + 'Aliases:' + '* ' + ', '.join(['`' + value3 + '`' for key3, value3 in value2['aliases'].items()])  # *Aliases:* `alias1`, `alias2`, `alias3`
                            embed.add_field(name=key2, value=content)

        if args == 'public' or public == 'public':
            await ctx.send(embed=embed)
        else:
            try:
                await ctx.author.send(embed=embed)
                if ctx.message.guild is None:  # If the user is calling command from PM
                    pass
                else:  # If the user is calling command from a channel
                    embed = discord.Embed(title='Help', description=Strings.pm_successful, colour=0x4ba139)  # Create embed
                    await ctx.send(embed=embed)
            except discord.errors.Forbidden:  # If cannot send PM to user
                embed = discord.Embed(title='Help', description=Strings.pm_unsuccessful, colour=0xff5252)  # Create embed
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
