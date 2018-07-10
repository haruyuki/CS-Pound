import discord
from discord.ext import commands


class Support:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def support(self, ctx):
        try:
            await ctx.author.send('https://discord.gg/PbzHqm9')  # PM Discord link to the CS-Pound Development Server to user
            embed = discord.Embed(title='Support', description='A PM has been sent to you!', colour=0x4ba139)  # Create embed
        except discord.errors.Forbidden:  # If cannot send PM to user
            embed = discord.Embed(title='Support', description='A PM couldn\'t be sent to you, it may be that you have \'Allow direct messages from server members\' disabled in your privacy settings.', colour=0xff5252)  # Create embed
        await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(Support(bot))
