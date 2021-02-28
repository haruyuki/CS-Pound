import discord
from discord.ext import commands

from chickensmoothie import _get_web_data


class Oekaki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def oekaki(self, ctx, link: str = ''):
        data = await _get_web_data(link)  # Get Oekaki data
        if data[0]:  # If data is valid
            base_link = 'http://www.chickensmoothie.com/Forum/'

            oekaki_title = data[1].xpath('//h3[@class="first"]/a/text()')[0]  # Title of drawing
            image = 'https://www.chickensmoothie.com' + data[1].xpath('//li[@class="ok-topic-head-image large"]/a/img/@src')[0]  # Image of drawing
            user_icon = base_link[:-1] + data[1].xpath('//dl[@class="postprofile"]')[0].xpath('dt/a/img/@src')[0][1:]  # The profile picture of the artist
            warning_text = 'Reminder!! Copying another person\'s art without permission to reproduce their work is a form of art-theft!'  # General warning text regarding Oekaki art

            if data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')[0] == 'Click to view':  # If drawing is based off another drawing
                artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/@href')  # Drawing information titles
                artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/text()')  # Drawing information values
            else:  # If drawing is not based off another drawing
                artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/@href')  # Drawing information titles
                artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')  # Drawing information values

            embed = discord.Embed(title=oekaki_title, colour=0x4ba139, url=link)  # Create embed
            embed.set_footer(text=warning_text, icon_url="https://vignette.wikia.nocookie.net/pufflescp/images/6/68/Red_Warning_Triangle.png/revision/latest?cb=20160718024653&format=original")  # Add warning text to footer
            embed.set_image(url=image)  # Add drawing to embed
            embed.set_author(name=artist_values[0], url=base_link + artist_links[0][1:], icon_url=user_icon)

            await ctx.send(embed=embed)  # Send embed
        else:  # If data is not valid
            await ctx.send(embed=data[1])  # Send embed


def setup(bot):
    bot.add_cog(Oekaki(bot))
