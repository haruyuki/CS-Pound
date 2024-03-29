import discord
from discord.ext import commands

import chickensmoothie as cs


class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pound"])
    @commands.guild_only()
    async def time(self, ctx):
        data = await cs.get_pound_string()

        embed = discord.Embed(
            title=data[0], description=data[1], colour=0x4BA139
        )  # Create embed
        await ctx.send(embed=embed)  # Send embed


async def setup(bot):
    await bot.add_cog(Time(bot))
