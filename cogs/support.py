import discord
from discord.ext import commands

from constants import Constants


class Support:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def support(self, ctx):
        try:
            await ctx.author.send(Constants.support_link)  # PM Discord link to the CS-Pound Development Server to user
            embed = discord.Embed(title='Support', description='A PM has been sent to you!', colour=0x4ba139)  # Create embed
            if ctx.message.guild is None:
                pass
            else:
                await ctx.send(embed=embed)  # Send embed
        except discord.errors.Forbidden:  # If cannot send PM to user
            embed = discord.Embed(title='Support', description='A PM couldn\'t be sent to you, it may be that you have \'Allow direct messages from server members\' disabled in your privacy settings.', colour=0xff5252)  # Create embed
            await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(Support(bot))
