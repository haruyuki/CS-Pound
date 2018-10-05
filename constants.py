import os


class Constants:
    prefix = ','  # The prefix used to call the bot
    discord_token = os.environ.get('discord', None)  # The Discord bot token
    osu_key = os.environ.get('osu', None)  # The osu! API key
    support_link = 'https://invite.gg/cspound'  # Link to support server
    version = '2.3'  # Current version of the bot
    invite_link = 'https://www.tailstar.us/'  # Link to website or direct link to invite the bot
    mongodb_uri = os.environ.get('mongodb', None)  # The MongoDB connection URI
    database_name = 'cs_pound'  # The name of the MongoDB database to use
    osu_collection_name = 'osu_profiles'  # The name of the collection for osu! user linking
    autoremind_collection_name = 'auto_remind'  # The name of the collection for Auto Remind users
    autoremind_fetch_limit = 300  # The amount of documents to buffer. Should update as collection gets bigger
