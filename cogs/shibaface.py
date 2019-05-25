import aiohttp

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
            title = 'Shibaface!'
            embed = discord.Embed(title=title, description='Available commands:', colour=0xFFE559)
            embed.add_field(name='__**sf random**__', value='Display a random pet!', inline=False)
            await ctx.send(embed=embed)

    @shibaface.command()
    @commands.guild_only()
    async def random(self, ctx):
        title = 'Shibaface!'
        description = '[http://www.shibaface.com](http://www.shibaface.com)'

        async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
            async with session.get(Shibaface.random_pet_url) as response:  # GET HTTP response of pet image link
                pet_url = str(response.url)

        embed = discord.Embed(title=title, description=description, colour=0xFFE559)
        embed.set_image(url=pet_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Support(bot))
