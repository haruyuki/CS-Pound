import aiohttp
import logging.handlers
import os
from os.path import isfile, join
import sys
import traceback

import discord
from discord.ext import commands

from constants import Constants
from library import update_autoremind_times

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(Constants.prefix),
    description="The Discord bot for all your ChickenSmoothie needs.",
    pm_help=False,
    case_insensitive=True,
)
bot.remove_command("help")  # Remove default help command to add custom one

logger = logging.getLogger("discord")  # Create logger
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    Constants.discord_log_filename, maxBytes=2097152, backupCount=1, encoding="utf-8"
)  # Set logging file
handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")
)  # Set logging format
logger.addHandler(handler)

if __name__ == "__main__":
    for extension in [
        f.replace(".py", "")
        for f in os.listdir(Constants.cogs_dir)
        if isfile(join(Constants.cogs_dir, f))
    ]:
        try:
            bot.load_extension(f"{Constants.cogs_dir}.{extension}")
        except (discord.ClientException, ModuleNotFoundError):
            if extension == ".DS_Store":
                pass
            else:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()


@bot.event
async def on_ready():  # When Client is loaded
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("--------")
    print(f"Discord.py Version: {discord.__version__}")
    print("--------")
    print(
        f"Use this link to invite {bot.user.name}: https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=268897512"
    )
    print("--------")
    print(f"You are running {bot.user.name} v{Constants.version}")
    print("Created by Haru#5616")
    await update_autoremind_times()
    await bot.change_presence(
        activity=discord.Game(Constants.playing_text), status=discord.Status.online
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f'Someone tried to run "{ctx.invoked_with}" a command that didn\'t exist')
        return
    elif isinstance(error, commands.CommandOnCooldown):
        print(
            f'Someone tried to run "{ctx.invoked_with}" while it was still on cooldown'
        )
        return
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        print(f'Someone tried to run "{ctx.invoked_with}" with a missing argument')
        return
    elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
        print(
            f'Someone tried to run "{ctx.invoked_with}" in a PM when it can\'t be used in a PM'
        )
        return
    elif isinstance(error, aiohttp.client_exceptions.ClientConnectorError):
        print(f'Someone tried to run "{ctx.invoked_with}" with an invalid URL')
        return
    raise error


bot.run(Constants.discord_token, bot=True, reconnect=True)
