import discord
from discord.ext import commands
from library import get_web_data


class Pet:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def pet(self, ctx, link: str = ''):  # Pet command
        data = await get_web_data(link, 'pet')  # Get pet data
        if data[0]:  # If data is valid
            titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
            values = data[1].xpath('//td[@class="r"]')  # Values of pet information
            given = True  # Pet has been given by another user
            value_list = []

            petimg = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
            if 'trans' in petimg:  # If pet image is transparent (i.e. Pet has items)
                petimg = 'http://www.chickensmoothie.com' + petimg  # Pet image link
            owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet
            owner_link = 'http://www.chickensmoothie.com/' + data[1].xpath('//td[@class="r"]/a/@href')[0]  # Link to user profile

            if titles[0] == 'PPS':  # If pet is PPS
                value_list.append('[This pet has "PPS". What\'s that?](http://www.chickensmoothie.com/help/pets#pps)')  # Append PPS value
                value_list.append('[' + owner_name + '](' + owner_link + ')')  # [Owner Name](Link to Owner) | Formats to Owner Name
                pps = True
            else:  # If pet is not PPS
                value_list.append('[' + owner_name + '](' + owner_link + ')')  # [Owner Name](Link to Owner) | Formats to Owner Name
                pps = False

            tables = len(titles)  # Number of rows
            temp = tables - 1 if pps else tables  # -1 Rows if pet is PPS
            for i in range(temp):  # For each title in titles
                if i == 0:  # If 'i' is at first value (PPS or Owner name)
                    pass  # Pass as first value has already been set
                elif temp - i == 2 or temp - i == 1:  # If 'i' is at second last or last value
                    if titles[i] == ('Age:' if pps else 'Growth:') or not given:  # If text of titles at 'i' is 'Age:' if pet is PPS otherwise 'Growth:' or pet not given
                        given = False
                        if temp - i == 2:  # If 'i' is second last value (i.e. Growth)
                            value_list.append(values[i].xpath('text()')[0])  # Append growth of pet
                        elif temp - i == 1:  # If 'i' is last value (i.e. Rarity)
                            value_list.append(values[i].xpath('img/@alt')[0])  # Append rarity of pet
                    elif titles[i] == ('Growth:' if pps else 'Rarity:') or given:  # If text of titles at 'i' is 'Growth:' is pet is PPS otherwise 'Rarity:' or pet is given
                        given = True
                        if temp - i == 2:  # If 'i' is second last value (i.e. Rarity)
                            value_list.append(values[i].xpath('img/@alt')[0])  # Append rarity of pet
                        elif temp - i == 1:  # If 'i' is last value (i.e. Given by)
                            titles[i] = titles[i].replace('\t', '').replace('\n', '')  # Remove extra formatting
                            value_list.append('[' + data[1].xpath('//td[@class="r"]/a/text()')[1] + ']' + '(' + 'http://www.chickensmoothie.com/' + data[1].xpath('//td[@class="r"]/a/@href')[1] + ')')  # Append given user profile
                else:  # Any other 'i'
                    value_list.append(values[i].xpath('text()')[0])  # Append text

            embed = discord.Embed(title=owner_name + '\'s Pet', colour=0x4ba139)  # Create embed
            embed.set_image(url=petimg)  # Set image

            for i in range(tables):  # For each title in titles
                if i == 0:  # If 'i' is first value (PPS or Owner name)
                    embed.add_field(name=titles[i], value=value_list[i], inline=False)  # Add field with no inline
                else:  # Any other 'i'
                    embed.add_field(name=titles[i], value=value_list[i], inline=True)  # Add field with inline
            await ctx.send(embed=embed)  # Send embed
        else:  # If data is not valid
            await ctx.send(embed=data[1])  # Send embed


def setup(bot):
    bot.add_cog(Pet(bot))
