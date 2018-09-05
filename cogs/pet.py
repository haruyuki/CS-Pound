import discord
from discord.ext import commands

import chickensmoothie as cs


class Pet:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def pet(self, ctx, link: str = ''):  # Pet command
        pet = await cs.pet(link)  # Get pet data
        if pet is None:
            embed = discord.Embed(title='Pet', description='An error has occured while processing pet image.', colour=0xff5252)  # Create embed
        else:
            embed = discord.Embed(title=pet['owner'] + '\'s Pet', colour=0x4ba139)  # Create embed
            embed.set_image(url=pet['image'])  # Set image

            initial = True
            for key, value in pet.items():
                if (key == 'owner' or key == 'pps') and initial:
                    if key == 'pps':
                        if not value:
                            continue
                        else:
                            embed.add_field(name='PPS', value='[This pet has "PPS". What\'s that?](http://www.chickensmoothie.com/help/pets#pps)', inline=False)
                    elif key == 'owner':
                        value = f'[{pet["owner"]}]({pet["owner_link"]})'
                        embed.add_field(name=key.capitalize(), value=value, inline=False)
                else:
                    if key == 'image' or key == 'owner_link' or key == 'given_link':
                        pass
                    else:
                        if key == 'id':
                            key = 'Pet ID'
                        elif key == 'name':
                            if value == '':
                                continue
                            else:
                                key = 'Pet\'s name'
                        elif key == 'age':
                            key = 'Age'
                            value = f'{value} days'
                        elif key == 'given':
                            if value == '':
                                continue
                            else:
                                key = f'Given to {pet["owner"]} by'
                                value = f'[{pet["given"]}]({pet["given_link"]})'
                        else:
                            key = key.capitalize()
                        embed.add_field(name=key, value=value, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Pet(bot))
