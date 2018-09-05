import aiohttp
import discord
from discord.ext import commands

import chickensmoothie as cs


class PetImage:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['img'])
    @commands.guild_only()
    async def image(self, ctx, link: str = ''):
        pet_image = await cs.image(link)
        if pet_image is not None:
            await ctx.send(file=discord.File(fp=pet_image, filename='pet.png'))  # Upload the file to the channel where message came from
        else:  # If data is invalid
            await ctx.send(embed=pet_image)  # Send embed


def setup(bot):
    bot.add_cog(PetImage(bot))
