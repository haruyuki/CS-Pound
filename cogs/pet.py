import discord
from discord.ext import commands

import chickensmoothie as cs
from constants import Strings


class Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def pet(self, ctx, link: str = ''):  # Pet command
        pet = await cs.pet(link)  # Get pet data
        if pet is None:
            embed = discord.Embed(title='Pet', description=Strings.pet_unsuccessful, colour=0xff5252)  # Create embed
        else:
            embed = discord.Embed(title=pet.owner_name + '\'s Pet', colour=0x4ba139)  # Create embed
            embed.set_image(url=pet.image)  # Set image

            if pet.pps:
                embed.add_field(name='PPS', value='[This pet has "PPS". What\'s that?](http://www.chickensmoothie.com/help/pets#pps)', inline=False)
            if pet.store_pet:
                embed.add_field(name='Store', value='[This pet was sold in the store](https://www.chickensmoothie.com/store/)', inline=False)
            embed.add_field(name='Owner', value=pet.owner(), inline=False)
            embed.add_field(name='Pet ID', value=pet.id)
            if pet.name is not None:
                embed.add_field(name="Pet's name", value=pet.name)
            embed.add_field(name='Adopted', value=pet.adoption_date)
            if pet.age == 0:
                embed.add_field(name='Age', value='Less than a day old')
            else:
                embed.add_field(name='Age', value=f'{pet.age} days')
            embed.add_field(name='Growth', value=pet.growth)
            embed.add_field(name='Rarity', value=pet.rarity)
            if pet.given_name is not None:
                embed.add_field(name=f'Given to {pet.owner_name} by', value=pet.given_by())

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Pet(bot))
