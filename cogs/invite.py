import discord
from discord.ext import commands

from constants import Constants, Strings


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        try:
            await ctx.author.send(Constants.invite_link)  # PM Discord link to the CS-Pound Development Server to user
            embed = discord.Embed(title='Invite', description=Strings.pm_successful, colour=0x4ba139)  # Create embed
        except discord.errors.Forbidden:  # If cannot send PM to user
            embed = discord.Embed(title='Invite', description=Strings.pm_unsuccessful, colour=0xff5252)  # Create embed
        await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(Invite(bot))
