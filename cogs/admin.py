from contextlib import redirect_stdout
import io
import textwrap
import traceback

from discord.ext import commands

from constants import Constants


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    @staticmethod
    def cleanup_code(content):
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @staticmethod
    def get_syntax_error(e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(hidden=True)
    async def load(self, ctx, *, cog):
        cog = Constants.cogs_dir + cog

        try:
            self.bot.load_extension(cog)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\u2705')

    @commands.command()
    async def unload(self, ctx, *, cog: str):
        cog = Constants.cogs_dir + cog

        try:
            self.bot.unload_extension(cog)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\u2705')

    @commands.command()
    async def reload(self, ctx, *, cog: str):
        cog = Constants.cogs_dir + cog

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\u2705')

    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self.last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Admin(bot))
