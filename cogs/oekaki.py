import discord
from discord.ext import commands

from chickensmoothie import _get_web_data


class Oekaki:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def oekaki(self, ctx, link: str = ''):
        data = await _get_web_data(link)  # Get Oekaki data
        if data[0]:  # If data is valid
            base_link = 'http://www.chickensmoothie.com/Forum/'

            oekaki_title = data[1].xpath('//h3[@class="first"]/a/text()')[0]  # Title of drawing
            image = 'https://www.chickensmoothie.com' + data[1].xpath('//li[@class="ok-topic-head-image large"]/img/@src')[0]  # Image of drawing
            user_icon = base_link[:-1] + data[1].xpath('//dl[@class="postprofile"]')[0].xpath('dt/a/img/@src')[0][1:]  # The profile picture of the artist
            warning_text = 'Reminder!! Copying another person\'s art without permission to reproduce their work is a form of art-theft!'  # General warning text regarding Oekaki art

            if data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')[0] == 'Click to view':  # If drawing is based off another drawing
                artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/@href')  # Drawing information titles
                artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/text()')  # Drawing information values
            else:  # If drawing is not based off another drawing
                artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/@href')  # Drawing information titles
                artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')  # Drawing information values

            artist_text = '[' + artist_values[0] + '](' + base_link + artist_links[0][1:] + ') [' + artist_values[1] + '(' + base_link + artist_links[1][1:] + ')]'  # [Artist Name](Link to Artist) [gallery](Link to Artist gallery) | Formats to Artist Name [gallery]

            embed = discord.Embed(title=oekaki_title, colour=0x4ba139, url=link)  # Create embed
            embed.add_field(name='Artist', value=artist_text)  # Add Artist field
            embed.set_footer(text=warning_text, icon_url="https://vignette.wikia.nocookie.net/pufflescp/images/6/68/Red_Warning_Triangle.png/revision/latest?cb=20160718024653&format=original")  # Add warning text to footer
            embed.set_image(url=image)  # Add drawing to embed
            embed.set_thumbnail(url=user_icon)  # Set thumbnail as user profile picture

            await ctx.send(embed=embed)  # Send embed
        else:  # If data is not valid
            await ctx.send(embed=data[1])  # Send embed


def setup(bot):
    bot.add_cog(Oekaki(bot))
