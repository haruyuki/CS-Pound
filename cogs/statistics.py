from datetime import datetime, timedelta
import os
import time

import discord
from discord.ext import commands
import psutil

from library import version

start_time = datetime.now()  # The time the script started running


def resolver(day, hour, minute, second):  # Pretty format time layout given days, hours, minutes and seconds
    day_section = ''
    hour_section = ''
    minute_section = ''
    second_section = ''

    def pluralise(string, value, and_placement=''):  # Correctly prefix or suffix ',' or 'and' placements
        if value == 0:  # If given time has no value
            return ''
        else:  # If given time has value
            return (' and ' if and_placement == 'pre' else '') + str(value) + ' ' + string + ('s' if value > 1 else '') + (' and ' if and_placement == 'suf' else (', ' if and_placement == 'com' else ''))
            # If 'and_placement' is set to prefix add 'and' otherwise leave blank
            # The value of the time
            # The type of time (day, hour, minute, second)
            # If value is larger than 1 then pluralise the time
            # If 'and_placement' is set to suffix add 'and' otherwise add a ',' instead if 'and_placement' is set to comma otherwise leave blank

    if day != 0 and ((hour == 0 and minute == 0) or (hour == 0 and second == 0) or (minute == 0 and second == 0)):
        # If there are day(s) but:
        # No hours or minutes
        # No hours or seconds
        # No minutes or seconds
        day_section = pluralise('day', day, 'suf')  # Pluralise the day section with a suffixed 'and' placement
    elif day != 0 and ((hour != 0 and minute != 0 and second != 0) or (hour != 0 and minute == 0) or (hour != 0 and second == 0) or (minute != 0 and second == 0) or (hour == 0 and minute != 0) or (hour == 0 and second != 0) or (minute == 0 and second != 0)):
        # If there are day(s) but:
        # There are hour(s) and minute(s) and second(s)
        # There are hour(s) but no minutes
        # There are hour(s) but no seconds
        # There are minute(s) but no hours
        # There are minute(s) but no seconds
        # There are second(s) but no hours
        # There are second(s) but no minutes
        day_section = pluralise('day', day, 'com')  # Pluralise the day section with a suffixed ',' placement

    if minute == 0:  # If there are no minutes
        hour_section = pluralise('hour', hour)  # Pluralise the hour section
    elif minute != 0 and second == 0:  # If there are minute(s) but no seconds
        hour_section = pluralise('hour', hour, 'suf')  # Pluralise the hour section with a suffixed 'and' placement
    else:  # If there are minute(s) and second(s)
        hour_section = pluralise('hour', hour, 'com')  # Pluralise the hour section with a suffixed ',' placement

    minute_section = pluralise('minute', minute)  # Pluralise the minute section

    if hour != 0 or minute != 0:  # If there are hour(s) or minute(s)
        second_section = pluralise('second', second, 'pre')  # Pluralise the second section with a prefixed 'and' placement
    else:  # If there are no hours or minutes
        second_section = pluralise('second', second)  # Pluralise the second section
    return day_section + hour_section + minute_section + second_section  # Return the formatted text


class Statistics:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['stats'])
    @commands.guild_only()
    async def statistics(self, ctx):
        def converter(seconds):  # Convert seconds into days, hours, minutes and seconds
            d = datetime(1, 1, 1) + timedelta(seconds=int(seconds))  # Create tuple of date values
            return d.day-1, d.hour, d.minute, d.second  # Return tuple of date values
        system_memory_mb = str(round(psutil.virtual_memory()[3] / 1000 / 1024, 2)) + ' MB'  # Get the used virtual memory (physical memory) of the system | X MB
        system_memory_percent = str(psutil.virtual_memory()[2]) + '%'  # Get the available virtual memory (physical memory) of the system | X%
        bot_memory_mb = str(round(psutil.Process(os.getpid()).memory_info()[0] / 1024**2, 2)) + ' MB'  # Get the memory usage of the bot (i.e. This script) | X MB
        bot_memory_percent = str(round(psutil.Process(os.getpid()).memory_percent(), 2)) + '%'  # Get used memory percentage of the bot (i.e. This script) | X%
        discord_py_version = discord.__version__  # Discord.py version
        server_count = str(len(self.bot.guilds))  # The number of servers this CS Pound is in
        member_count = str(len(set(self.bot.get_all_members())))  # The number of unique users the CS Pound is connected to
        bot_uptime = converter((datetime.now() - start_time).total_seconds())  # The time the bot (script) has been running
        system_uptime = converter(round(time.time() - psutil.boot_time()))  # The time the system has been running

        bot_uptime = resolver(bot_uptime[0], bot_uptime[1], bot_uptime[2], bot_uptime[3])  # Pretty format the bot uptime
        system_uptime = resolver(system_uptime[0], system_uptime[1], system_uptime[2], system_uptime[3])  # Pretty format the system uptime

        embed = discord.Embed(title='Stats', description='', colour=0x4ba139)  # Create empty embed
        embed.add_field(name='System Memory Usage', value=f'{system_memory_percent} ({system_memory_mb})', inline=False)  # Add system memory usage to embed
        embed.add_field(name=self.bot.user.name + ' Memory Usage', value=f'{bot_memory_percent} ({bot_memory_mb})', inline=False)  # Add bot memory usage to embed
        embed.add_field(name=self.bot.user.name + ' Version', value=version, inline=False)  # Add bot version to embed
        embed.add_field(name='Discord.py Version', value=discord_py_version, inline=False)  # Add Discord.py version to embed
        embed.add_field(name='Server Count', value=server_count, inline=False)  # Add server count to embed
        embed.add_field(name='Member Count', value=member_count, inline=False)  # Add member count to embed
        embed.add_field(name=self.bot.user.name + ' Uptime', value=bot_uptime, inline=False)  # Add bot uptime to embed
        embed.add_field(name='System Uptime', value=system_uptime, inline=False)  # Add system uptime to embed
        await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(Statistics(bot))
