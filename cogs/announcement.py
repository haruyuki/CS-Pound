from discord.ext import commands


class Announcement:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['announce', 'am'])
    @commands.guild_only()
    async def announcement(self, ctx):
        pass

    @announcement.command()
    @commands.guild_only()
    async def on(self, ctx):
        pass

    @announcement.command()
    @commands.guild_only()
    async def off(self, ctx):
        pass

    @announcement.command()
    @commands.guild_only()
    async def latest(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Announcement(bot))
