import os


class Constants:
    prefix = ','  # Prefix used to call bot
    owner_id = 277398425044123649  # User ID of bot owner
    discord_token = os.environ.get('discord', None)  # Discord bot token from environment variables
    discord_log_filename = 'discord.log'  # Name of logging file
    osu_key = os.environ.get('osu', None)  # osu! API key from environment variables
    support_link = 'https://invite.gg/cspound'  # Link to support server
    version = '2018.1205.2'  # Current version of bot
    invite_link = 'https://haruyuki.moe/CS-Pound'  # Link to invite the bot
    mongodb_uri = os.environ.get('mongodb', None)  # MongoDB connection URI from environment variables
    database_name = 'cs_pound'  # Name of MongoDB database
    osu_collection_name = 'osu_profiles'  # Collection name for osu! user linking
    autoremind_collection_name = 'auto_remind'  # Collection name for Auto Remind users
    autoremind_fetch_limit = 300  # Amount of documents to buffer. Should update as collection gets bigger
    cogs_dir = 'cogs'  # Directory where cogs are placed
    playing_text = ',help | CS: haruyuki'  # Bot playing text


class Strings:
    invalid_pet_link = "That is not a valid pet link!"

    autoremind_off_successful = 'Your Auto Remind has been turned off successfully.'
    autoremind_not_set = "You don't have an Auto Remind setup!"
    autoremind_update_timeout = 'Operation timed out.'
    autoremind_update_cancel = 'Operation cancelled.'

    no_time = "You didn't provide a time!"
    invalid_time = "You didn't provide a valid time!"

    remindme_too_long = 'That time is too long!'

    giveaway_no_permission = "I don't have permission to create giveaways! Please ask the owner or admin to enable 'Add Reactions' and 'Read Message History'!"
    giveaway_user_no_permission = "You don't have permission to run this command!"

    pet_unsuccessful = 'An error has occurred while processing pet link.'

    pound_closed = "Sorry, the pound is closed at the moment. :("
    pound_opened = "Pound is currently open!"

    pm_successful = 'A PM has been sent to you!'
    pm_unsuccessful = "A PM couldn't be sent to you, it may be that you have 'Allow direct messages from server members' disabled in your privacy settings."
