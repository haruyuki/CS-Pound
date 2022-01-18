import discord
from discord.ext import commands


class Haruyuki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["haru"])
    @commands.guild_only()
    async def haruyuki(self, ctx):
        await ctx.send("Use it!")


def setup(bot):
    bot.add_cog(Haruyuki(bot))
