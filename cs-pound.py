import discord
import random
import asyncio
import sys
import traceback
from discord.ext import commands

prefix = ','
version = '2.0'
tokens = [token.replace('\n', '') for token in list(open('tokens.txt'))]  # Get tokens from tokens.txt file
extensions = ['cogs.help', 'cogs.admin']

bot = commands.Bot(command_prefix=prefix, description='Rewrite Test', pm_help=False)
bot.remove_command('help')

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

bot.run(tokens[0], bot=True, reconnect=True)
