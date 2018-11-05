import asyncio

import discord
from discord.ext import commands

from library import parse_time, formatter


class RemindMe:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rm'])
    @commands.guild_only()
    async def remindme(self, ctx, amount: str):  # Remind Me command
        final_total = parse_time(amount)  # Get formatted times
        if final_total[0] == 0:  # If no time specified
            embed = discord.Embed(title='Remind Me', description='That is not a valid time!', colour=0xff5252)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        elif final_total[0] > 86400:  # If time is longer than 24 hours
            embed = discord.Embed(title='Remind Me', description='That time is too long!', colour=0xff5252)  # Create embed
            await ctx.send(embed=embed)  # Send embed
        else:  # If time is valid
            before_message = f'A reminder has been set for {ctx.message.author.mention} in {formatter(final_total[1], final_total[2], final_total[3], final_total[4])}.'  # A reminder has been set for USER in X hours, Y minutes, and Z seconds.
            embed = discord.Embed(title='Remind Me', description=before_message, colour=0x4ba139)   # Create embed
            await ctx.send(embed=embed)  # Send embed
            after_message = f'Reminder for {ctx.message.author.mention}!'  # Reminder for USER!
            await asyncio.sleep(final_total[0])  # Sleep for set time
            await ctx.send(after_message)  # Send message


def setup(bot):
    bot.add_cog(RemindMe(bot))
