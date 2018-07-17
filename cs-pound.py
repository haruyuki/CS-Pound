import asyncio
import discord
from discord.ext import commands
from library import prefix, version
import logging
from os import listdir
from os.path import isfile, join
import sys
import traceback
import uvloop

tokens = [token.replace('\n', '') for token in list(open('tokens.txt'))]  # Get tokens from tokens.txt file
cogs_dir = 'cogs'

bot = commands.Bot(command_prefix=prefix, description='The Discord bot for all your ChickenSmoothie needs.', pm_help=False, case_insensitive=True)
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


@bot.event
async def on_ready():  # When Client is loaded
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('--------')
    print(f'Discord.py Version: {discord.__version__}')
    print('--------')
    print(f'Use this link to invite {bot.user.name}: https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=268569600')
    print('--------')
    print(f'You are running {bot.user.name} v{version}')
    print('Created by Peko#7955')
    await bot.change_presence(activity=discord.Game(',help | By: Peko#7955'), status=discord.Status.online)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

bot.run(tokens[1], bot=True, reconnect=True)
