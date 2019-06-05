import random

import discord
from discord.ext import commands

from constants import ShibafaceC


class Shibaface(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['sf'])
    @commands.guild_only()
    async def shibaface(self, ctx):
        if ctx.invoked_subcommand is None:
            title = 'Shibaface!'
            embed = discord.Embed(title=title, description='Available commands:', colour=0xFFE559)
            embed.add_field(name='__**sf random**__', value='Display a random pet!', inline=False)
            await ctx.send(embed=embed)

    @shibaface.command()
    @commands.guild_only()
    async def random(self, ctx):
        title = 'Shibaface!'
        description = '[http://www.shibaface.com](http://www.shibaface.com)'

        embed = discord.Embed(title=title, description=description, colour=0xFFE559)
        embed.set_image(url=random.choice(ShibafaceC.adopts))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Shibaface(bot))
