import discord
from discord.ext import commands

import chickensmoothie as cs
from constants import Strings


class PetImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['img'])
    @commands.guild_only()
    async def image(self, ctx, link: str = ''):
        pet_image = await cs.image(link)
        if pet_image is not None:
            await ctx.send(file=discord.File(fp=pet_image, filename='pet.png'))  # Upload the file to the channel where message came from
        else:  # If data is invalid
            embed = discord.Embed(title='Pet', description=Strings.pet_unsuccessful, colour=0xff5252)
            await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(PetImage(bot))
