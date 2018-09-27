import discord
import os
import sys

client = discord.AutoShardedClient()
token = os.environ.get('BOT_TOKEN', None)

if token is None:
    print('Please specify a token in Travis as an environment variable. The variable should be called "BOT_TOKEN"')
    with open(os.devnull, 'w') as devnull:
        sys.stderr = devnull
        exit()


@client.event
async def on_shard_ready(shard_id):
    print(f'Shard {shard_id} connected.')


@client.event
async def on_ready():
    user_count = sum([1 for _ in client.get_all_members()])
    print('===== START =====')
    print(f'This proof certifies that the bot with ID {client.user.id} holds the following statistics:')
    print(f'Guild Count: {len(client.guilds)}')
    print(f'User Count: {user_count}')
    print('===== END =====')
    await client.close()
    with open(os.devnull, 'w') as dev:
        sys.stderr = dev
        exit()

client.run(token)
