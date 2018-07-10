from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        cog = 'cogs.' + cog

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        cog = 'cogs.' + cog

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        cog = 'cogs.' + cog

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`SUCCESS`**')


def setup(bot):
    bot.add_cog(Admin(bot))
