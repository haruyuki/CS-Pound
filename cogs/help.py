import discord
import hashlib
import json
from discord.ext import commands

help_hash = ''  # Current hash of help.json
help_list = {}

# -------------------- HELP TEXT --------------------
warning_help = '''\
CS Pound website (Where you also get the invite link)
http://tailstar.us

-'''  # Title help

chickensmoothie_help2 = '''\
`,archive <query>` - Search the ChickenSmoothie archives (Under Development)

`,fair <link>` - Determine whether a trade is fair (Under Development)

`,image <link>` - Displays pet image only

`,oekaki <link>` - Displays Oekaki drawing

`,pet <link>` - Displays pet information

`,time` - Tells you how long until the pound opens

`,trade <link>` - Displays trade information (Under Development)

_'''

chickensmoothie_help = '''\
`,image <link>` - Displays pet image only

`,oekaki <link>` - Displays Oekaki drawing

`,pet <link>` - Displays pet information

`,time` - Tells you how long until the pound opens

_'''  # Chicken Smoothie related commands help

general_help = '''\
`,autoremind <on/off> <time>` - Turns on or off global auto reminding

`,remindme <time>` - Pings you after specified amount of time

_'''  # General commands help

informational_help = '''\
`,help` - Displays this message

`,support` - PM's you the link to the CS Pound Development Server

`,statistics` - Displays bot statistics
'''  # Informational commands help


def process_help(command):  # Get the help text from help.json
    global help_hash, help_list

    def monospace(string):  # Returns string in Discord monospace format
        return '`' + string + '`'  # `string`

    def italic(string):  # Returns string in Discord italics format
        return '*' + string + '*'  # *string*

    new_help_hash = hashlib.md5(open('help.json').read().encode()).hexdigest()  # MD5 hash of help.json
    if help_hash != new_help_hash:  # If help.json has been changed
        help_hash = new_help_hash  # Set hash to the new changes
        with open('help.json') as f:  # Open help.json
            help_list = json.load(f)  # Load the JSON data

    command_information = help_list[command]  # Get the command information of the command
    message = monospace(command_information['usage']) + ' - ' + command_information['description']  # `usage` - description
    if command_information['examples']:  # If there are examples for the command
        message += '\n' + italic('Examples:') + ' ' + ', '.join([monospace(value) for key, value in command_information['examples'].items()])  # *Examples:* `example1`, `example2`, `example3`

    if command_information['aliases']:  # If there are aliases for the command
        message += '\n' + italic('Aliases:') + ' ' + ', '.join([monospace(value) for key, value in command_information['aliases'].items()])  # *Aliases:* `alias1`, `alias2`, `alias3`

    return message


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, args: str = ''):
        embed = discord.Embed(colour=0x4ba139)  # Create empty embed
        # -------------------- CHICKENSMOOTHIE HELP --------------------
        if args == 'archive':  # If requested Archive command help
            embed.add_field(name='**Archive**', value=process_help(args))  # Add Archive help information to embed
        elif args == 'fair':  # If requested Fair command help
            embed.add_field(name='**Fair', value=process_help(args))  # Add Fair help information to embed
        elif args == 'oekaki':  # If requested Oekaki command help
            embed.add_field(name='**Oekaki**', value=process_help(args))  # Add Oekaki help information to embed
        elif args == 'pet':  # If included 'pet' argument
            embed.add_field(name='**Pet**', value=process_help(args))  # Embed Pet help information
        elif args == 'time':  # If included 'time' argument
            embed.add_field(name='**Time**', value=process_help(args))  # Embed Time help information
        elif args == 'trade':  # If included 'trade' argument
            embed.add_field(name='**Trade**', value=process_help(args))  # Embed Trade help information

        # -------------------- GENERAL HELP --------------------
        elif args == 'autoremind':  # If included 'autoremind' argument
            embed.add_field(name='**Auto Remind**', value=process_help(args))  # Embed Auto Remind help information
        elif args == 'remindme':  # If included 'remineme' argument
            embed.add_field(name='**Remind Me**', value=process_help(args))  # Embed Remind Me help information

        # -------------------- INFORMATIONAL HELP --------------------
        elif args == 'help':  # If included 'help' argument
            embed.add_field(name='**Help**', value=process_help(args))  # Embed Help help information
        elif args == 'support':
            embed.add_field(name='**Support**', value=process_help(args))  # Embed Support help information
        elif args == 'statistics':
            embed.add_field(name='**Statistics**', value=process_help(args))  # Embed Statistics help information

        else:  # If provided no arguments or requested a help topic that doesn't exist
            embed.add_field(name=":pencil: __**To know about command usage or examples, use: ,help <command>**__", value=warning_help)  # add Warning help information to embed
            embed.add_field(name=':dog: __**ChickenSmoothie Commands**__', value=chickensmoothie_help)  # Embed Chicken Smoothie related commands
            embed.add_field(name=':file_folder: __**General Commands**__', value=general_help)  # Embed General commands
            embed.add_field(name=':wrench: __**Informational Commands**__', value=informational_help)  # Embed informational commands

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
