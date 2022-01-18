import discord
from discord.ext import commands

from constants import Constants, Strings


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def support(self, ctx):
        try:
            await ctx.author.send(
                Constants.support_link
            )  # PM Discord link to the CS-Pound Development Server to user
            embed = discord.Embed(
                title="Support", description=Strings.pm_successful, colour=0x4BA139
            )  # Create embed
            if ctx.message.guild is not None:
                await ctx.send(embed=embed)  # Send embed
        except discord.errors.Forbidden:  # If cannot send PM to user
            embed = discord.Embed(
                title="Support", description=Strings.pm_unsuccessful, colour=0xFF5252
            )  # Create embed
            await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(Support(bot))
