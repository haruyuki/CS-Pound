import asyncio

import discord
from discord.ext import commands

from constants import Strings
from library import parse_time, resolver


class RemindMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rm'])
    @commands.guild_only()
    async def remindme(self, ctx, *amount: str):  # Remind Me command
        amount = ''.join(amount)
        try:
            temp = amount.split('m')
            print(temp)
            if len(temp) == 2 and temp[-1].isdigit():
                temp[-1] = temp[-1] + 's'
            temp[-2] = temp[-2] + 'm'
            print(temp)
            amount = temp
        except IndexError:
            pass
        amount = ''.join(amount)

        total = parse_time(amount)  # Get formatted times
        if total == 0:  # If no time specified
            embed = discord.Embed(title='Remind Me', description=Strings.invalid_time, colour=0xff5252)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        elif total > 86400:  # If time is longer than 24 hours
            embed = discord.Embed(title='Remind Me', description=Strings.remindme_too_long, colour=0xff5252)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:  # If time is valid
            before_message = f'A reminder has been set for {ctx.message.author.mention} in {resolver(total)}.'  # A reminder has been set for USER in X hours, Y minutes, and Z seconds.
            embed = discord.Embed(title='Remind Me', description=before_message, colour=0x4ba139)   # Create embed
            await ctx.send(embed=embed)  # Send embed
            after_message = f'Reminder for {ctx.message.author.mention}!'  # Reminder for USER!
            await asyncio.sleep(total)  # Sleep for set time
            await ctx.send(after_message)  # Send message


def setup(bot):
    bot.add_cog(RemindMe(bot))
