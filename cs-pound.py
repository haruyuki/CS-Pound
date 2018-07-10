import asyncio
import discord
from library import prefix, version
import logging
import sys
import traceback
from discord.ext import commands

tokens = [token.replace('\n', '') for token in list(open('tokens.txt'))]  # Get tokens from tokens.txt file
extensions = ['cogs.admin', 'cogs.pet', 'cogs.help', 'cogs.support', 'cogs.statistics']

bot = commands.Bot(command_prefix=prefix, description='The Discord bot for all your ChickenSmoothie needs.', pm_help=False)
bot.remove_command('help')
logger = logging.getLogger('discord')  # Create logger
logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')  # Set logging file
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))  # Set logging format
logger.addHandler(handler)  # Start logger

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
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

bot.run(tokens[1], bot=True, reconnect=True)
