import asyncio
import re

import discord
from discord.ext import commands
import motor.motor_asyncio as amotor

from constants import Constants, Strings, Variables
import chickensmoothie as cs
import library

mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client[Constants.database_name]
collection = database[Constants.autoremind_collection_name]


class AutoRemind:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ar'])
    @commands.guild_only()  # Command can only be run in guilds
    async def autoremind(self, ctx, args=''):
        if args == 'off' or args == 'cancel':  # If user is turning off Auto Remind
            cursor = collection.find({'user_id': str(ctx.author.id)})  # Get document of user
            user_data = await cursor.to_list(length=1)
            try:
                user_data = user_data[0]
                user_object_id = user_data['_id']
            except IndexError:
                user_data = None
                user_object_id = None

            if user_data is not None:
                await collection.delete_one({'_id': user_object_id})
                await ctx.send(Strings.autoremind_off_successful)
            else:
                await ctx.send(Strings.autoremind_not_set)
        else:  # If user is setting an Auto Remind
            time = re.findall(r'^(\d{1,2})m?$', args)  # Get the requested Auto Remind time
            if time != 0:  # If user provided a valid time
                time = int(time[0])  # Convert the time into an integer
                if time > 60:
                    await ctx.send('That time is too far!')
                else:
                    cursor = collection.find({'user_id': str(ctx.author.id)})  # Get document of user
                    user_data = await cursor.to_list(length=1)
                    try:
                        user_data = user_data[0]
                        user_object_id = user_data['_id']
                    except IndexError:
                        user_data = None

                    if user_data is not None:
                        if int(user_data['channel_id']) == ctx.channel.id:
                            old_time = user_data['remind_time']
                            await collection.update_one({'_id': user_object_id}, {'$set': {'server_id': str(ctx.guild.id), 'channel_id': str(ctx.channel.id), 'remind_time': time}})
                            await ctx.send(f'Your Auto Remind has been updated from {old_time} minute{"" if old_time == 1 else "s"} to {time} minute{"" if time == 1 else "s"}!')

                        else:
                            description = (f'You already have a {user_data["remind_time"]} minute Auto Remind setup at <#{user_data["channel_id"]}>!\n'  # You aleady have a X minute Auto Remind setup at #channel!
                                           'Are you sure you want to overwrite it to this channel? (yes/no) (No `,` prefix needed!)')
                            embed = discord.Embed(title='Auto Remind', description=description, colour=0xff5252)
                            await ctx.send(embed=embed)

                            def predicate(m):
                                return m.author == ctx.author and m.channel == ctx.channel

                            try:
                                msg = await self.bot.wait_for('message', check=predicate, timeout=30.0)
                            except asyncio.TimeoutError:
                                await ctx.send(Strings.autoremind_update_timeout)
                            else:
                                lowered = msg.content.lower()
                                if lowered in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
                                    await collection.update_one({'_id': user_object_id}, {'$set': {'server_id': str(ctx.guild.id), 'channel_id': str(ctx.channel.id), 'remind_time': time}})
                                    await ctx.send(f'Will remind you {time} minute{"" if time == 1 else "s"} before the pound opens!')
                                else:
                                    await ctx.send(Strings.autoremind_update_cancel)
                    else:
                        await collection.insert_one({'server_id': str(ctx.guild.id), 'channel_id': str(ctx.channel.id), 'user_id': str(ctx.author.id), 'remind_time': time})
                        await ctx.send(f'Your Auto Remind has been set for {time} minute{"" if time == 1 else "s"}!')
                    await library.update_autoremind_times()
            elif args == '':  # If no arguments provided
                await ctx.send(Strings.no_time)
            else:
                await ctx.send(Strings.invalid_time)


def setup(bot):
    bot.add_cog(AutoRemind(bot))
    bot.loop.create_task(pound_countdown(bot))


async def pound_countdown(bot):  # Background task to countdown to when the pound opens
    await bot.wait_until_ready()  # Wait until bot has loaded before starting background task
    while not bot.is_closed():  # While bot is still running
        if not Variables.cooldown:  # If command is not on cooldown
            string = await cs.get_pound_string()  # Get pound text
            seconds = cs.get_pound_time(string)  # Extract total seconds

        seconds, sleep_amount, send_msg = library.calculate_sleep_amount(seconds)

        if send_msg:  # If sending message is needed
            time = round(seconds / 60)
            if time in Variables.autoremind_times:
                channel_ids = await library.get_sending_channels(time)
                for channel in channel_ids:
                    sending_channel = bot.get_channel(channel)
                    message = await library.prepare_message(channel, time)
                    try:
                        await sending_channel.send(message)
                    except (AttributeError, discord.errors.Forbidden):
                        pass

        await asyncio.sleep(sleep_amount)  # Sleep for sleep amount
