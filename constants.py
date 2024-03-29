import json
import os

from google.oauth2 import service_account
import pygsheets
from dotenv import load_dotenv

load_dotenv()

def authorisation():
    scopes = (
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    )  # The scopes the bot requires (Spreadsheets and Google Drive)
    credentials_raw = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", "{}"
    )  # Get the login credentials from environment variables
    service_account_info = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=scopes
    )
    return pygsheets.authorize(custom_credentials=credentials)


class Constants:
    prefix = ","  # Prefix used to call bot
    owner_id = 277398425044123649  # User ID of bot owner
    discord_token = os.environ.get(
        "discord", None
    )  # Discord bot token from environment variables
    discord_log_filename = "discord.log"  # Name of logging file
    support_link = "https://invite.gg/cspound"  # Link to support server
    version = "2022.1217.0"  # Current version of bot
    invite_link = "https://haruyuki.moe/CS-Pound"  # Link to invite the bot
    mongodb_uri = os.environ.get(
        "mongodb", None
    )  # MongoDB connection URI from environment variables
    database_name = "cs_pound"  # Name of MongoDB database
    giveaways_collection_name = "giveaways"  # Collection name for giveaways
    other_collection_name = "other"  # Collection name for any other singular data
    autoremind_collection_name = "auto_remind"  # Collection name for Auto Remind users
    autoremind_fetch_limit = (
        1500  # Amount of documents to buffer. Should update as collection gets bigger
    )
    cogs_dir = "cogs"  # Directory where cogs are placed
    playing_text = ",help | CS: haruyuki"  # Bot playing text
    contact_email = "jumpy12359@gmail.com"  # Contact email
    google_sheets_api = authorisation()
    pound_pets_group = "https://www.chickensmoothie.com/accounts/viewgroup.php?userid=2887&groupid=5813&pageSize=3000"
    username = "haruyuki"
    password = os.environ.get("password", None)
    image_exists = False  # Variable used in poundpets.py


class FlightRisingC:
    progeny_url = "http://flightrising.com/includes/ol/scryer_progeny.php"
    cprogeny_url = "https://www1.flightrising.com/scrying/ajax-predict"
    token = os.environ.get("flightrising_token", None)


class Variables:
    autoremind_times = set()
    cooldown = False


class Strings:
    invalid_pet_link = "That is not a valid pet link!"

    autoremind_off_successful = "Your Auto Remind has been turned off successfully."
    autoremind_not_set = "You don't have an Auto Remind setup!"
    autoremind_update_timeout = "Operation timed out."
    autoremind_update_cancel = "Operation cancelled."

    no_time = "You didn't provide a time!"
    invalid_time = "You didn't provide a valid time!"

    remindme_too_long = "That time is too long!"

    giveaway_no_permission = "I don't have permission to create giveaways! Please ask the owner or admin to enable 'Add Reactions' and 'Read Message History'!"
    giveaway_user_no_permission = "You don't have permission to run this command!"

    pet_unsuccessful = "An error has occurred while processing pet link."

    pm_successful = "A PM has been sent to you!"
    pm_unsuccessful = "A PM couldn't be sent to you, it may be that you have 'Allow direct messages from server members' disabled in your privacy settings."
