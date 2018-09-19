import hashlib
import logging
from os import listdir
from os.path import isfile, join
import subprocess
import sys
import traceback

import asyncio
import discord
from discord.ext import commands
import motor.motor_asyncio as amotor
import uvloop

from chickensmoothie import _get_web_data
from constants import Constants

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

cogs_dir = 'cogs'
autoremind_hash = ''
autoremind_times = []
cooldown = False
mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_connection_string)
database = mongo_client['cs_pound']
collection = database['auto_remind']

bot = commands.Bot(command_prefix=commands.when_mentioned_or(Constants.prefix), description='The Discord bot for all your ChickenSmoothie needs.', pm_help=False, case_insensitive=True)
bot.remove_command('help')
logger = logging.getLogger('discord')  # Create logger
logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')  # Set logging file
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))  # Set logging format
logger.addHandler(handler)  # Start logger

if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(f'{cogs_dir}.{extension}')
        except (discord.ClientException, ModuleNotFoundError):
            if extension == '.DS_Store':
                pass
            else:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()


async def mongodb_query(query):
    cursor = collection.find(query)
    results = await cursor.to_list(length=1000)
    return results


async def compose_message(time):  # Function to compose and send mention messages to channels
    print(f'Composing message for {time} minutes')
    grep_statement = 'grep \'[0-9]*\\s[0-9]*\\s[0-9]*\\s' + time + '\' autoremind.txt | cut -f2 -d\' \' | sort -u'  # Get channels with Auto Remind set at 'time'
    channel_ids = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run grep statement
    for i in range(len(channel_ids)):  # For each Discord channel ID
        grep_statement = 'grep \'[0-9]*\\s' + channel_ids[i] + '\\s[0-9]*\\s' + time + '\' autoremind.txt | cut -f3 -d\' \''  # Grab all unique Discord user ID's with that channel ID
        user_ids = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run grep statement
        if time == '1':  # If there is only one minute left
            message = time + ' minute until pound opens! '
        else:  # If there is more than 1 minute left
            message = time + ' minutes until pound opens! '
        for j in range(len(user_ids)):  # For each Discord user
            message += '<@' + user_ids[j] + '> '  # Message format for mentioning users | <@USER_ID>
        try:
            channel = bot.get_channel(int(channel_ids[i]))
            print(f'Channel is {channel}')
            await channel.send(message)  # Send message to Discord channel with mention message
            print(f'Message sent')
        except AttributeError:
            print('Some error appeared')
            pass


async def minute_check(time):  # Function to check if any user has Auto Remind setup at 'time'
    print(f'Running minute check for {time} minutes')
    global autoremind_hash, autoremind_times
    time = str(time)
    new_hash = hashlib.md5(open('autoremind.txt').read().encode()).hexdigest()  # MD5 hash of autoremind.txt
    if autoremind_hash != new_hash:  # If file has been modified since last check
        autoremind_hash = new_hash
        cut_statement = 'cut -f4 -d\' \' autoremind.txt | sort -u'  # Grab all unique reminding times from autoremind.txt
        autoremind_times = subprocess.Popen(cut_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run cut statement

    if time in autoremind_times:  # If someone has a Auto Remind set at current 'time'
        await compose_message(time)  # Run compose message


async def pound_countdown():  # Background task to countdown to when the pound opens
    global cooldown
    print('Started pound countdown function')
    await bot.wait_until_ready()  # Wait until bot has loaded before starting background task
    value = 0
    text = ''
    print('Bot is ready')
    while not bot.is_closed():  # While bot is still running
        sleep_amount = 0
        print('Bot is still running')
        if not cooldown:  # If command is not on cooldown
            print('Command not on cooldown')
            data = await _get_web_data('https://www.chickensmoothie.com/pound.php')  # Get pound data
            print('Received web data')
            if data[0]:  # If pound data is valid and contains content
                print('Data was sucessful')
                text = data[1].xpath('//h2/text()')  # List all texts with H2 element
                print(f'Texts with h2 element: {text}')
                try:  # Try getting pound opening text
                    print('Trying to get pound text')
                    text = text[1]  # Grab the pound opening time text
                    print(f'Received text: {text}')
                    value = [int(s) for s in text.split() if s.isdigit()]  # Extract the numbers in the text
                    print(f'Values in text: {value}')
                    if len(value) == 1:  # If there is only one number
                        value = value[0]
                        if 'hour' in text:  # If hour in pound opening time
                            print('Hour in text')
                            if value == 1:  # If there is one hour left
                                cooldown = True
                                value = 60  # Start countdown from 60 minutes
                                sleep_amount = 0
                            else:  # If there is more than one hour
                                sleep_amount = (value - 2) * 3600  # -1 hour and convert into seconds
                        elif 'minute' in text:  # If minute in pound opening time
                            print('Minute in text')
                            sleep_amount = 0
                            cooldown = True
                        elif 'second' in text:  # If second in pound opening time
                            pass
                    elif len(value) == 2:  # If there are two numbers
                        if 'hour' and 'minute' in text:
                            print('Hour and minute in text')
                            sleep_amount = value[1] * 60  # Get the minutes and convert to seconds
                            value = 60
                            text = 'minute'
                            cooldown = True
                        elif 'minute' and 'second' in text:
                            pass
                    elif len(value) == 0:  # If there are no times i.e. Pound recently closed or not opening anytime soon
                        print('No time')
                        sleep_amount = 3600  # 1 hour
                except IndexError:  # Pound is currently open
                    print('Pound open')
                    sleep_amount = 3600  # 1 hour
            else:  # If pound data isn't valid
                sleep_amount = 11400  # 3 hours 10 minutes
        else:  # If command is on cooldown
            if 'hour' in text:  # If hour in text
                if value != 0:  # If minutes left is not zero
                    await minute_check(value)  # Run minute check
                    value -= 1  # Remove one minute
                    sleep_amount = 60  # 1 minute
                else:  # If time ran out (i.e. Pound is now open)
                    cooldown = False
                    sleep_amount = 10800  # 3 hours
            elif 'minute' and 'second' in text:  # If minute and second in text
                sleep_amount = value[1]
                value = 1
            elif 'minute' in text:  # If minute in text
                if value > 0:  # If minutes left is not zero
                    await minute_check(value)  # Run minute check
                    value -= 1  # Remove one minute
                    sleep_amount = 60  # 1 minute
                else:  # If time ran out (i.e. Pound is now open)
                    cooldown = False
                    sleep_amount = 10800  # 3 hours
            elif 'second' in text:  # If second in text
                pass
            else:
                print(f'Cooldown but no value')
                sleep_amount = 10800  # 3 hours
        await asyncio.sleep(sleep_amount)  # Sleep for sleep amount
        print(f'Slept for: {sleep_amount}')
        print(f'Command is on cooldown: {cooldown}')


@bot.event
async def on_ready():  # When Client is loaded
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('--------')
    print(f'Discord.py Version: {discord.__version__}')
    print('--------')
    print(f'Use this link to invite {bot.user.name}: https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=268897512')
    print('--------')
    print(f'You are running {bot.user.name} v{Constants.version}')
    print('Created by Peko#7955')
    await bot.change_presence(activity=discord.Game(',help | By: Peko#7955'), status=discord.Status.online)

bot.loop.create_task(pound_countdown())
bot.run(Constants.discord_token, bot=True, reconnect=True)
