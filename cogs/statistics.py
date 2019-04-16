from datetime import datetime
import os
import platform
import sys
import time

import discord
from discord.ext import commands
import psutil

from constants import Constants
from library import resolver

start_time = datetime.now()  # The time the script started running


class Statistics:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['stats'])
    @commands.guild_only()
    async def statistics(self, ctx):
        if ctx.invoked_subcommand is None:
            bot_id = self.bot.user.id
            python_version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
            discord_py_version = f'{discord.__version__}'
            bot_version = f'{Constants.version}'
            operating_system = f'{platform.system()}'
            guild_count = f'{len(self.bot.guilds)} guilds'
            cpu_percent = f'{psutil.cpu_percent()}%'
            memory_percent = f'{psutil.virtual_memory().percent}%'
            bot_memory = f'{round(psutil.Process(os.getpid()).memory_info().rss / 1024**2)} MB'
            cogs_loaded = f'{len(self.bot.cogs)} commands loaded'
            ping = f'{round(self.bot.latency * 1000)}ms'
            user_count = f'{len(set(self.bot.get_all_members()))} unique users'
            bot_uptime = resolver((datetime.now() - start_time).total_seconds())  # The time the bot (script) has been running
            system_uptime = resolver(round(time.time() - psutil.boot_time()))  # The time the system has been running

            description = f'''`Created by Haru#5616. CS: haruyuki`

**Owner ID:** `{Constants.owner_id}`
**CS-Pound ID:** `{bot_id}`

**Running on:** `{guild_count}`
**Serving:** `{user_count}`

**OS:** `{operating_system}`
**Commands:** `{cogs_loaded}`
**Ping:** `{ping}`

**Python version:** `{python_version}`
**discord.py version:** `{discord_py_version}`
**CS-Pound version:** `{bot_version}`

**CPU usage:** `{cpu_percent}`
**Memory usage:** `{memory_percent}`
**CS-Pound memory usage:** `{bot_memory}`

**CS-Pound uptime:** `{bot_uptime}`
**System uptime:** `{system_uptime}`'''

            embed = discord.Embed(colour=0x4ba139, timestamp=datetime.utcnow())  # Create empty embed
            embed.set_footer(text='Requested')
            embed.set_thumbnail(url="https://www.chickensmoothie.com/Forum/images/avatars/gallery/Bunnies/0001-1.png")
            embed.add_field(name='CS-Pound Stats', value=description)
            await ctx.send(embed=embed)  # Send embed

        else:
            pass


def setup(bot):
    bot.add_cog(Statistics(bot))
