import io
from urllib.parse import urlparse
import urllib.request

import discord
from discord.ext import commands

from constants import Shibaface


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['sf'])
    @commands.guild_only()
    async def shibaface(self, ctx):
        if ctx.invoked_subcommand is None:
            title = f'Shibaface!'
            embed = discord.Embed(title=title, description='Available commands:', colour=0xFFE559)
            embed.add_field(name='__**sf random**__', value='Display a random pet!', inline=False)
            await ctx.send(embed=embed)

    @shibaface.command()
    @commands.guild_only()
    async def random(self, ctx):
        response = urllib.request.urlopen(Shibaface.random_pet_url)
        data = response.read()
        image = io.BytesIO(data)
        image.seek(0)
        filename = urlparse(response.url).query
        await ctx.send(file=discord.File(fp=image, filename=filename))


def setup(bot):
    bot.add_cog(Support(bot))
