import aiohttp
import discord
from discord.ext import commands
import lxml.html


class Time:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pound'])
    @commands.guild_only()
    async def time(self, ctx):
        async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
            async with session.get('http://www.chickensmoothie.com/pound.php') as response:  # GET HTTP response of pound page
                connection = await response.text()  # Request HTML page data
                dom = lxml.html.fromstring(connection)  # Extract HTML from site
                text = dom.xpath('//h2/text()')  # Pound opening text

        try:
            if ':)' in text[1]:  # If :) in text
                output = text[1][:-85].replace('\n', r'').replace('\t', r'') + ' The pound opens at totally random times of day, so check back later to try again :)'  # Remove excess formatting text
            else:  # If any other text in text
                output = text[1].replace('Sorry, the pound is closed at the moment.', '').replace('\n', r'').replace('\t', r'') + '.'
        except IndexError:  # If text doesn't exist
            output = 'Pound is currently open!'

        embed = discord.Embed(title='Time', description=output, colour=0x4ba139)  # Create embed
        await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(Time(bot))
