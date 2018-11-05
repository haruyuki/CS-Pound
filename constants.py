import os


class Constants:
    prefix = ','  # The prefix used to call the bot
    owner_id = 277398425044123649
    discord_token = os.environ.get('discord', None)  # The Discord bot token
    discord_log_filename = 'discord.log'
    osu_key = os.environ.get('osu', None)  # The osu! API key
    support_link = 'https://invite.gg/cspound'  # Link to support server
    version = '2018.1105.23'  # Current version of the bot
    invite_link = 'https://www.tailstar.us/'  # Link to website or direct link to invite the bot
    mongodb_uri = os.environ.get('mongodb', None)  # The MongoDB connection URI
    database_name = 'cs_pound'  # The name of the MongoDB database to use
    osu_collection_name = 'osu_profiles'  # The name of the collection for osu! user linking
    autoremind_collection_name = 'auto_remind'  # The name of the collection for Auto Remind users
    autoremind_fetch_limit = 300  # The amount of documents to buffer. Should update as collection gets bigger
    cogs_dir = 'cogs'  # The directory where your cogs are placed
    playing_text = ',help | CS: haruyuki'  # The text that the bot is playing


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
