import json
import os

from google.oauth2 import service_account
import pygsheets


def authorisation():
    scopes = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')  # The scopes the bot requires (Spreadsheets and Google Drive)
    credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '{}')  # Get the login credentials from environment variables
    service_account_info = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=scopes)
    return pygsheets.authorize(custom_credentials=credentials)


class Constants:
    prefix = ','  # Prefix used to call bot
    owner_id = 277398425044123649  # User ID of bot owner
    discord_token = os.environ.get('discord', None)  # Discord bot token from environment variables
    discord_log_filename = 'discord.log'  # Name of logging file
    support_link = 'https://invite.gg/cspound'  # Link to support server
    version = '2019.0821.1'  # Current version of bot
    invite_link = 'https://haruyuki.moe/CS-Pound'  # Link to invite the bot
    mongodb_uri = os.environ.get('mongodb', None)  # MongoDB connection URI from environment variables
    database_name = 'cs_pound'  # Name of MongoDB database
    giveaways_collection_name = 'giveaways'  # Collection name for giveaways
    other_collection_name = 'other'  # Collection name for any other singular data
    autoremind_collection_name = 'auto_remind'  # Collection name for Auto Remind users
    autoremind_fetch_limit = 500  # Amount of documents to buffer. Should update as collection gets bigger
    cogs_dir = 'cogs'  # Directory where cogs are placed
    playing_text = ',help | CS: haruyuki'  # Bot playing text
    contact_email = 'jumpy12359@gmail.com'  # Contact email
    google_sheets_api = authorisation()
    pound_pets_group = 'https://www.chickensmoothie.com/accounts/viewgroup.php?userid=2887&groupid=5813'
    username = 'haruyuki'
    password = os.environ.get('password', None)
    image_exists = False  # Variable used in poundpets.py


class OsuC:
    osu_key = os.environ.get('osu', None)  # osu! API key from environment variables
    osu_collection_name = 'osu_profiles'  # Collection name for osu! user linking


class ShibafaceC:
    adopts = [
        "http://www.shibaface.com//simple.php?a=1&v=616930622&.jpg",
        
        "http://www.shibaface.com//simple.php?a=2&v=3863830453&.jpg",
        "http://www.shibaface.com//simple.php?a=2&v=2733710090&.jpg",
        
        "http://www.shibaface.com//simple.php?a=3&v=1321334585&.jpg",
        "http://www.shibaface.com//simple.php?a=3&v=684429622&.jpg",
        "http://www.shibaface.com//simple.php?a=3&v=1081145739&.jpg",
        "http://www.shibaface.com//simple.php?a=3&v=70303178&.jpg",
        
        "http://www.shibaface.com//simple.php?a=4&v=3264379752&.jpg",
        "http://www.shibaface.com//simple.php?a=4&v=2462919478&.jpg",
        "http://www.shibaface.com//simple.php?a=4&v=770413587&.jpg",
        
        "http://www.shibaface.com//simple.php?a=5&v=2796625737&.jpg",
        
        "http://www.shibaface.com//simple.php?a=6&v=4286924414&.jpg",
        "http://www.shibaface.com//simple.php?a=6&v=1481761195&.jpg",
        "http://www.shibaface.com//simple.php?a=6&v=3612962465&.jpg",
        
        "http://www.shibaface.com//simple.php?a=7&v=1787679605&.jpg",
        "http://www.shibaface.com//simple.php?a=7&v=892570824&.jpg",
        "http://www.shibaface.com//simple.php?a=7&v=3678888637&.jpg",
        
        "http://www.shibaface.com//simple.php?a=8&v=801871411&.jpg",
        "http://www.shibaface.com//simple.php?a=8&v=3752420949&.jpg",
        "http://www.shibaface.com//simple.php?a=8&v=2447583262&.jpg",
        "http://www.shibaface.com//simple.php?a=8&v=337554917&.jpg",
        "http://www.shibaface.com//simple.php?a=8&v=237811670&.jpg",
        
        "http://www.shibaface.com//simple.php?a=9&v=1932053202&.jpg",
        "http://www.shibaface.com//simple.php?a=9&v=2464885526&.jpg",
        "http://www.shibaface.com//simple.php?a=9&v=3718603869&.jpg",
        "http://www.shibaface.com//simple.php?a=9&v=878677412&.jpg",
        
        "http://www.shibaface.com//simple.php?a=10&v=71155136&.jpg",
        "http://www.shibaface.com//simple.php?a=10&v=3886702161&.jpg",
        "http://www.shibaface.com//simple.php?a=10&v=917933900&.jpg",
        "http://www.shibaface.com//simple.php?a=10&v=1842730029&.jpg",
        
        # 12 and 11 are same as 15
        
        "http://www.shibaface.com//simple.php?a=13&v=3587337258&.jpg",
        
        "http://www.shibaface.com//simple.php?a=14&v=4230759892&.jpg",
        "http://www.shibaface.com//simple.php?a=14&v=4230759892&.jpg",
        "http://www.shibaface.com//simple.php?a=14&v=1652349824&.jpg",
        "http://www.shibaface.com//simple.php?a=14&v=1597368014&.jpg",
        "http://www.shibaface.com//simple.php?a=14&v=2863141717&.jpg",
        
        "http://www.shibaface.com//simple.php?a=15&v=3452204092&.jpg",
        "http://www.shibaface.com//simple.php?a=15&v=2309107800&.jpg",
        "http://www.shibaface.com//simple.php?a=15&v=727421615&.jpg",
        "http://www.shibaface.com//simple.php?a=15&v=2837778654&.jpg",
        "http://www.shibaface.com//simple.php?a=15&v=1537335902&.jpg",
        "http://www.shibaface.com//simple.php?a=15&v=3641729262&.jpg",
        "http://www.shibaface.com//simple.php?a=15&v=1044219840&.jpg",
        
        "http://www.shibaface.com//simple.php?a=16&v=3897577898&.jpg",
        "http://www.shibaface.com//simple.php?a=16&v=377466754&.jpg",
        "http://www.shibaface.com//simple.php?a=16&v=3967636870&.jpg",
        "http://www.shibaface.com//simple.php?a=16&v=3628818867&.jpg",
        
        "http://www.shibaface.com//simple.php?a=17&v=691507404&.jpg",
        "http://www.shibaface.com//simple.php?a=17&v=2722307003&.jpg",
        
        "http://www.shibaface.com//simple.php?a=18&v=702517282&.jpg",
        "http://www.shibaface.com//simple.php?a=18&v=1038255130&.jpg",
        "http://www.shibaface.com//simple.php?a=18&v=242071447&.jpg",
        "http://www.shibaface.com//simple.php?a=18&v=4054992969&.jpg",
        
        "http://www.shibaface.com//simple.php?a=19&v=346533213&.jpg",
        "http://www.shibaface.com//simple.php?a=19&v=1255994145&.jpg",
        "http://www.shibaface.com//simple.php?a=19&v=1318254441&.jpg",
        "http://www.shibaface.com//simple.php?a=19&v=1445523408&.jpg",
        
        "http://www.shibaface.com//simple.php?a=20&v=5814693&.jpg",
        "http://www.shibaface.com//simple.php?a=20&v=3653787699&.jpg",
        "http://www.shibaface.com//simple.php?a=20&v=3313204353&.jpg",
        "http://www.shibaface.com//simple.php?a=20&v=682463573&.jpg",
        "http://www.shibaface.com//simple.php?a=20&v=2126628669&.jpg",

        "http://www.shibaface.com//simple.php?a=21&v=3177907344&.jpg",
        
        "http://www.shibaface.com//simple.php?a=22&v=1827329311&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=168408059&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=2408724079&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3171222778&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=2584814560&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=2330014481&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3805371183&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3076918933&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=824019197&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3160999303&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=1187446590&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3460003776&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3882507926&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3166045533&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=2536845007&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=4258153507&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=2995456892&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=4097723858&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=1573905440&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3296755060&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=2319856551&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3615387272&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=3321789460&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=1965542607&.jpg",
        "http://www.shibaface.com//simple.php?a=22&v=1642977284&.jpg",
        
        "http://www.shibaface.com//simple.php?a=23&v=4166992292&.jpg",
        "http://www.shibaface.com//simple.php?a=23&v=3304946949&.jpg",
        "http://www.shibaface.com//simple.php?a=23&v=328051319&.jpg",
        "http://www.shibaface.com//simple.php?a=23&v=3768080741&.jpg",
        
        "http://www.shibaface.com//simple.php?a=24&v=1831654615&.jpg",
        "http://www.shibaface.com//simple.php?a=24&v=3367596353&.jpg",
        "http://www.shibaface.com//simple.php?a=24&v=1204682295&.jpg",
        "http://www.shibaface.com//simple.php?a=24&v=1371859000&.jpg",
        "http://www.shibaface.com//simple.php?a=24&v=1254355773&.jpg",
        "http://www.shibaface.com//simple.php?a=24&v=1324545807&.jpg",
        "http://www.shibaface.com//simple.php?a=24&v=201110019&.jpg",
        
        "http://www.shibaface.com//simple.php?a=25&v=2071511682&.jpg",
        "http://www.shibaface.com//simple.php?a=25&v=1170013249&.jpg",
        "http://www.shibaface.com//simple.php?a=25&v=3144680076&.jpg",
        "http://www.shibaface.com//simple.php?a=25&v=2784173064&.jpg",
        "http://www.shibaface.com//simple.php?a=25&v=1789449040&.jpg",
        
        "http://www.shibaface.com/simple.php?a=26&v=1548215726&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=1949879758&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=2725059461&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=1589307214&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=1993920301&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=1146617253&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=3561647540&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=2800033558&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=4020655702&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=2576556130&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=2342269542&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=3364057464&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=771003403&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=2048836578&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=3315039343&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=3214739040&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=656645833&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=770479105&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=4015281848&.jpg",
        "http://www.shibaface.com//simple.php?a=26&v=435331097&.jpg",

        "http://www.shibaface.com//simple.php?a=27&v=2382837759&.jpg",
        "http://www.shibaface.com//simple.php?a=27&v=3712378045&.jpg",
        "http://www.shibaface.com//simple.php?a=27&v=3426252229&.jpg",
        "http://www.shibaface.com//simple.php?a=27&v=3400823630&.jpg",

        "http://www.shibaface.com//simple.php?a=28&v=728535697&.jpg",
        "http://www.shibaface.com//simple.php?a=28&v=3999618975&.jpg",
        "http://www.shibaface.com//simple.php?a=28&v=376942479&.jpg",
        "http://www.shibaface.com//simple.php?a=28&v=2952271363&.jpg",
        
        "http://www.shibaface.com//simple.php?a=29&v=770741258&.jpg",
        "http://www.shibaface.com//simple.php?a=29&v=1381624741&.jpg",
        "http://www.shibaface.com//simple.php?a=29&v=3998373802&.jpg",
        "http://www.shibaface.com//simple.php?a=29&v=3284105793&.jpg",
        "http://www.shibaface.com//simple.php?a=29&v=280668487&.jpg",
        "http://www.shibaface.com//simple.php?a=29&v=1670175347&.jpg",
        
        "http://www.shibaface.com//simple.php?a=30&v=1734467225&.jpg",
        "http://www.shibaface.com//simple.php?a=30&v=45464398&.jpg",
        "http://www.shibaface.com//simple.php?a=30&v=3440276724&.jpg",

        "http://www.shibaface.com/simple.php?a=31&v=2380739611&.jpg",
        "http://www.shibaface.com/simple.php?a=31&v=1773326409&.jpg",
        "http://www.shibaface.com//simple.php?a=31&v=3607785200&.jpg",
        "http://www.shibaface.com//simple.php?a=31&v=1467018893&.jpg",
        "http://www.shibaface.com//simple.php?a=31&v=3897315764&.jpg"
    ]


class FlightRisingC:
    progeny_url = 'http://flightrising.com/includes/ol/scryer_progeny.php'


class Variables:
    cooldown = False
    autoremind_times = set()


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

    pm_successful = 'A PM has been sent to you!'
    pm_unsuccessful = "A PM couldn't be sent to you, it may be that you have 'Allow direct messages from server members' disabled in your privacy settings."
