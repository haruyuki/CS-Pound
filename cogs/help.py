import discord
import hashlib
import json
from discord.ext import commands

current_hash = ''  # Current hash of help.json
help_list = {}
command_list = []

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, args: str = ''):
        global current_hash, help_list, command_list
        embed = discord.Embed(colour=0x4ba139)  # Create empty embed
        message = ''

        new_hash = hashlib.md5(open('help.json').read().encode()).hexdigest()  # MD5 hash of help.json
        if current_hash != new_hash:  # If help.json has been changed
            current_hash = new_hash  # Set hash to the new changes
            with open('help.json') as f:  # Open help.json
                help_list = json.load(f)  # Load the JSON data
            for key, value in help_list['categories'].items():
                for key2, value2 in value['commands'].items():
                    command_list.append(key2.replace(' ', '').lower())

        if args == '':
            title = f':{help_list["warning"]["icon"]}: __**Note**__'
            content = help_list["warning"]["description"] + '\n\n_'
            embed.add_field(name=title, value=content)  # add Warning help information to embed
            for key, value in help_list['categories'].items():
                title = f':{value["icon"]}: __**{key} Commands**__'
                content = '\n\n'.join([f'`{value2["usage"]}` - {value2["short"]}' for key2, value2 in value['commands'].items()]) + '\n\n_'
                embed.add_field(name=title, value=content)
        else:
            if args in command_list:
                for key, value in help_list['categories'].items():
                    for key2, value2 in value['commands'].items():
                        if args == key2.replace(' ', '').lower():
                            content = f'`{value2["usage"]}` - {value2["description"]}'  # `usage` - description
                            if value2['examples']:  # If there are examples for the command
                                content += '\n' + '*' + 'Examples:' + '* ' + ', '.join(['`' + value3 + '`' for key3, value3 in value2['examples'].items()])  # *Examples:* `example1`, `example2`, `example3`

                            if value2['aliases']:  # If there are aliases for the command
                                content += '\n' + '*' + 'Aliases:' + '* ' + ', '.join(['`' + value3 + '`' for key3, value3 in value2['aliases'].items()])  # *Aliases:* `alias1`, `alias2`, `alias3`
                            embed.add_field(name=key2, value=content)

        try:
            await ctx.author.send(embed=embed)
            if ctx.message.guild is None:  # If the user is calling command from PM
                pass
            else:  # If the user is calling command from a channel
                embed = discord.Embed(title='Help', description='A PM has been sent to you!', colour=0x4ba139)  # Create embed
                await ctx.send(embed=embed)
        except discord.errors.Forbidden:  # If cannot send PM to user
            embed = discord.Embed(title='Help', description='A PM couldn\'t be sent to you, it may be that you have \'Allow direct messages from server members\' disabled in your privacy settings.', colour=0xff5252)  # Create embed
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
