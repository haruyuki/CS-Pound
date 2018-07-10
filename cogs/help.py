import discord
from library import warning_help, chickensmoothie_help, general_help, informational_help, process_help
from discord.ext import commands


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, args: str = ''):
        embed = discord.Embed(colour=0x4ba139)  # Create empty embed
        if args == '':  # If provided no arguments or requested a help topic that doesn't exist
            embed.add_field(name=":pencil: __**To know about command usage or examples, use: ,help <command>**__", value=warning_help)  # add Warning help information to embed
            embed.add_field(name=':dog: __**ChickenSmoothie Commands**__', value=chickensmoothie_help)  # Embed Chicken Smoothie related commands
            embed.add_field(name=':file_folder: __**General Commands**__', value=general_help)  # Embed General commands
            embed.add_field(name=':wrench: __**Informational Commands**__', value=informational_help)  # Embed informational commands

        # -------------------- CHICKENSMOOTHIE HELP --------------------
        elif args == 'archive':  # If requested Archive command help
            embed.add_field(name='**Archive**', value=process_help(args))  # Add Archive help information to embed
        elif args == 'fair':  # If requested Fair command help
            embed.add_field(name='**Fair**', value=process_help(args))  # Add Fair help information to embed
        elif args == 'image':  # If requested Image command help
            embed.add_field(name='**Image**', value=process_help(args))
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
        else:
            embed = discord.Embed(title='Help', description='That command doesn\'t exist!', colour=0xff5252)  # Create embed

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
