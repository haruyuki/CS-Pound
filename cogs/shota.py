import discord
from discord.ext import commands


class Shota(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def shota(self, ctx):
        member = ctx.author
        role = discord.utils.get(ctx.guild.roles, name="正太")

        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send('Removed 正太')
        else:
            await member.add_roles(role)
            await ctx.send('Added 正太')


def setup(bot):
    bot.add_cog(Shota(bot))
