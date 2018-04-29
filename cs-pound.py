# -------------------- IMPORTS --------------------
import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import logging
import lxml.html
import math
import os
from PIL import Image, ImageFont, ImageDraw
import platform
import psutil
import pyimgur
import requests
import time as pytime
import urllib.request

'''
Imgur Album
https://imgur.com/a/BiVzx

ChickenSmoothie PHP Links
http://static.chickensmoothie.com/archive/image.php?k=<LONG PET ID>&bg=<HEX COLOUR>
http://static.chickensmoothie.com/pic.php?k=<LONG PET ID>
http://www.chickensmoothie.com/viewpet.php?id=<PET ID>
http://www.chickensmoothie.com/archive/<YEAR>/<EVENT>/<ANIMAL>
http://www.chickensmoothie.com/archive/<YEAR>/<EVENT>/Artist-<ARTIST NAME>
http://www.chickensmoothie.com/trades/viewtrade.php?id=<TRADE ID>&userid=<USER ID>signature=<RANDOM SIGNATURE>
http://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=<USER ID>
http://static.chickensmoothie.com/item/<ITEM TYPE ID>&p=<ITEM ID>.jpg
http://www.chickensmoothie.com/pet/<PET ID>&trans=1.jpg
http://www.chickensmoothie.com/oekaki/image/image.php?id=<OEKAKI ID>&size=<SMALL/MEDIUM/LARGE>&format=auto&rev=1513122186

Development Board
https://trello.com/b/RAJhtsl8/cs-pound-development-board
'''

# -------------------- VARIABLES --------------------
start_time = datetime.now()  # The time the script started running
call = 'LIVE'  # Whether the bot is currently in 'DEV' or 'LIVE' mode

# -------------------- TOKENS --------------------
def decryption_imgur(a):  # Decrypt Imgur Token
    a = list(a)  # Create list of encrypted token
    b = '0123456789abcdef'  # String of hexadecimal characters
    c = []  # List of unencrypted token characters
    d = []  # Temporary list
    for e in range(len(a)):  # For each character in 'a' list
        f = b[(b.find(a[e]) + 6) % 16]  # Move character forward by 6
        d.append(f)  # Append to 'd' list

    a = ''.join(map(str, d))  # Combine 'd' list into one string
    a = [a[g:g+2] for g in range(0, len(a), 2)]  # Split into every 2nd character
    for h in range(len(a)):  # For each item in 'a' list
        i = '0x' + a[h]  # Add '0x' to each item for conversion from hexadecimal
        j = int(i, 16)  # Convert from hexadecimal to integer
        k = abs(int(j) - 256)  # Absolute value of converted integer minus 256
        l = format(int(k), 'x')  # Convert integer back to hexadecimal
        c.append(l)  # Append to 'c' list

    return ''.join(map(str, c))  # Combine 'c' list into one string

def decryption_discord(a):  # Decrypt Discord token
    pass

tokens = [i.replace('\n', '') for i in list(open('tokens.txt'))]  # Get tokens from tokens.txt file
CLIENT_ID = decryption_imgur(tokens[0])  # Imgur Client ID
CLIENT_SECRET = decryption_imgur(tokens[1])  # Imgur Secret ID

# -------------------- DISCORD --------------------
if call == 'LIVE':  # If being used for production
    token = tokens[2]  # Discord CS Pound Secret Token
    prefix = ','  # Prefix to call CS Pound Discord Bot
    version = '1.6.1'  # CS Pound Discord Bot version
else:  # If used for testing
    token = tokens[3]  # Discord CS Pound DEV Secret Token
    prefix = '.'  # Prefix to call CS Pound DEV Discord Bot
    reminder = 0
    version = 'DEV'  # CS Pound DEV Discord Bot version

# -------------------- HELP TEXT --------------------
warning_help = '''\
CS Pound website (Where you also get the invite link)
http://tailstar.us

-'''

chickensmoothie_help2 = '''\
`,archive <query>` - Search the ChickenSmoothie archives (Under Development)

`,fair <link>` - Determine whether a trade is fair (Under Development)

`,image <link>` - Displays pet image only

`,oekaki <link>` - Displays Oekaki drawing

`,pet <link>` - Displays pet information

`,pet2 <link>` - Displays pet screenshot

`,time` - Tells you how long until the pound opens

`,trade <link>` - Displays trade information (Under Development)

_'''

chickensmoothie_help = '''\
`,image <link>` - Displays pet image only

`,oekaki <link>` - Displays Oekaki drawing

`,pet <link>` - Displays pet information

`,pet2 <link>` - Displays pet screenshot

`,time` - Tells you how long until the pound opens

_'''

general_help2 = '''\
`,autoremind <on/off> <time>` - Turns on or off global auto reminding (Under Development)

`,remindme <time>` - Pings you after specified amount of time

_'''

general_help = '''\
`,remindme <time>` - Pings you after specified amount of time

_'''

informational_help = '''\
`,help` - Displays this message

`,support` - PM's you the link to the CS Pound Development Server

`,statistics` - Displays bot statistics
'''

# -------------------- CHICKENSMOOTHIE HELP TEXT --------------------
archive_help = '''\
`,archive <year> <month/event> <species/artist>` - Displays all pets within the specified query. Species/artist is optional, if not provided, displays all pets in that query.
*Examples:* `,archive 2012 august cat` `,archive 2008 special-releases` `,archive 2011 kwanzaa sorren-fey`

Note: This command usage may change at any time as I\'m still figuring out how I should set this up'''  # Help of Archive command

fair_help = '''\
`,fair <trade link>` - Determines whether a trade is fair using general trading rules from http://www.chickensmoothie.com/Forum/viewtopic.php?f=20&t=2066303
*Example:* `,fair http://www.chickensmoothie.com/trades/viewtrade.php?id=69636615&userid=841634&signature=rkVfZpJ8QINKNRs6sdnbrA`
'''  # Help of Fair command

image_help = '''\
`,image <link>` - Displays only the pet image from the given link
*Example:* `,image http://www.chickensmoothie.com/viewpet.php?id=54685939`
*Aliases:* `,img`'''  # Help of Image command

oekaki_help = '''\
`,oekaki <link>` - Displays Oekaki drawing from the link
*Example:* `,oekaki http://www.chickensmoothie.com/Forum/viewtopic.php?f=34&t=3664993`'''  # Help of Oekaki command

pet_help = '''\
`,pet <link>` - Displays information about the pet from the link
*Example:* `,pet http://www.chickensmoothie.com/viewpet.php?id=54685939`'''  # Help of Pet command

pet2_help = '''\
`,pet2 <link>` - Displays a image of the pet and it's information
*Example:* `,pet2 http://www.chickensmoothie.com/viewpet.php?id=54685939`'''  # Help of Pet2 command

time_help = '''\
`,time` - Tells you how long before the pound opens
*Usage:* `,time`
*Aliases:* `,pound`

Note: Message Might not display properly if pound just closed'''  # Help of Time command

trade_help = '''\
`,trade <link>` - Displays trade information. A maximum 8 pets will be displayed on each side
*Example:* `,trade http://www.chickensmoothie.com/trades/viewtrade.php?id=70508878&userid=841634&signature=dEs5tySl0Mmp8usx4CGbhw`

Note: Make sure to use the sharing trade link!'''  # Help of Trade command

# -------------------- GENERAL HELP TEXT --------------------
autoremind_help = '''\
`,autoremind <on/off> <time>` - Turns on or off auto reminding. If turned on and time is not provided it will automatically default to 10 minutes
*Examples:* `,autoremind off` `,autoremind on` `,autoremind on 15m`'''  # Help of Autoremind command

remindme_help = '''\
`,remindme <time>` - Pings you after specified amount of time. Maximum reminding time is 24h
*Examples:* `,remindme 1h6m23s` `,remindme 12m` `,remindme 1h10s`
*Aliases:* `,rm`

Note: At this current moment there is no way to remove set remindme\'s, so make sure you\'ve typed it right before sending!'''  # Help of Remindme command

# -------------------- INFORMATIONAL HELP TEXT --------------------
help_help = '''\
`,help` - Displays the help message
*Usage:* `,help`'''  # Help of Help command

support_help = '''\
`,support` - PM's you the link to the CS Pound Development Server
*Usage:* `,support`'''  # Help of Support command

statistics_help = '''\
`,stats` - Displays CS Pound bot statistics
*Usage:* `,statistics`
*Aliases:* `,stats`'''  # Help of Stats command


# -------------------- FUNCTIONS --------------------
def time_extractor(time):  # Convert given time into seconds
    time = time.lower()  # Change all letters to lowercase
    htotal = 0
    mtotal = 0
    stotal = 0
    if 'h' not in time and 'm' not in time and 's' not in time:  # If there is no time at all
        pass
    elif 'h' in time or 'hr' in time:  # If hours in input
        htotal = time.split('h')[0]  # Split input and get number of hours
        if 'm' in time:  # If minutes in input
            temp = time.split('h')[1]  # Split input and get leftover time (minutes and seconds)
            mtotal = temp.split('m')[0]  # Split temp and get number of minutes
            if 's' in time:  # If seconds in input
                temp = time.split('h')[1]  # Split input and get leftover time (minutes and seconds)
                temp2 = temp.split('m')[1]  # Split temp and get leftover time (seconds)
                stotal = temp2.split('s')[0]  # Split temp2 and get number of seconds
        else:  # If no minutes in input
            if 's' in time:  # If seconds in input
                temp = time.split('h')[1]  # Split input and get leftover time (seconds)
                stotal = temp.split('s')[0]  # Split temp and get number of seconds
    else:  # If no hours in input
        if 'm' in time:  # If minutes in input
            mtotal = time.split('m')[0]  # Split input and get number of minutes
            if 's' in time:  # If seconds in input
                temp = time.split('m')[1]  # Split input and get leftover time (seconds)
                stotal = temp.split('s')[0]  # Split temp and get number of seconds
        else:  # If no minutes in input
            if 's' in time:  # If seconds in input
                stotal = time.split('s')[0]  # Split input and get number of seconds
    htotal = int(htotal)  # Convert 'htotal' into integer
    mtotal = int(mtotal)  # Convert 'mtotal' into integer
    stotal = int(stotal)  # Convert 'stotal' into integer
    if htotal == 0 and mtotal == 0 and stotal == 0:  # If hours, minutes and seconds is 0
        finaltotal = 0
    else:  # If values in hours, minutes or seconds
        finaltotal = int((htotal * 60 * 60) + (mtotal * 60) + stotal)  # Total time in seconds
    return finaltotal, htotal, mtotal, stotal


def resolver(day, hour, minute, second):  # Pretty format time layout given days, hours, minutes and seconds
    day_section = ''
    hour_section = ''
    minute_section = ''
    second_section = ''

    def pluralise(string, value, and_placement=''):  # Correctly prefix or suffix ',' or 'and' placements
        if value == 0:  # If given time has no value
            return ''
        else:  # If given time has value
            return (' and ' if and_placement == 'pre' else '') + str(value) + ' ' + string + ('s' if value > 1 else '') + (' and ' if and_placement == 'suf' else (', ' if and_placement == 'com' else ''))
            # If 'and_placement' is set to prefix add 'and' otherwise leave blank
            # The value of the time
            # The type of time (day, hour, minute, second)
            # If value is larger than 1 then pluralise the time
            # If 'and_placement' is set to suffix add 'and' otherwise add a ',' instead if 'and_placement' is set to comma otherwise leave blank

    if day != 0 and ((hour == 0 and minute == 0) or (hour == 0 and second == 0) or (minute == 0 and second == 0)):
        # If there are day(s) but:
        # No hours or minutes
        # No hours or seconds
        # No minutes or seconds
        day_section = pluralise('day', day, 'suf')  # Pluralise the day section with a suffixed 'and' placement
    elif day != 0 and ((hour != 0 and minute != 0 and second != 0) or (hour != 0 and minute == 0) or (hour != 0 and second == 0) or (minute != 0 and second == 0) or (hour == 0 and minute != 0) or (hour == 0 and second != 0) or (minute == 0 and second != 0)):
        # If there are day(s) but:
        # There are hour(s) and minute(s) and second(s)
        # There are hour(s) but no minutes
        # There are hour(s) but no seconds
        # There are minute(s) but no hours
        # There are minute(s) but no seconds
        # There are second(s) but no hours
        # There are second(s) but no minutes
        day_section = pluralise('day', day, 'com')  # Pluralise the day section with a suffixed ',' placement

    if minute == 0:  # If there are no minutes
        hour_section = pluralise('hour', hour)  # Pluralise the hour section
    elif minute != 0 and second == 0:  # If there are minute(s) but no seconds
        hour_section = pluralise('hour', hour, 'suf')  # Pluralise the hour section with a suffixed 'and' placement
    else:  # If there are minute(s) and second(s)
        hour_section = pluralise('hour', hour, 'com')  # Pluralise the hour section with a suffixed ',' placement

    minute_section = pluralise('minute', minute)  # Pluralise the minute section
    
    if hour != 0 or minute != 0:  # If there are hour(s) or minute(s)
        second_section = pluralise('second', second, 'pre')  # Pluralise the second section with a prefixed 'and' placement
    else:  # If there are no hours or minutes
        second_section = pluralise('second', second)  # Pluralise the second section
    return day_section + hour_section + minute_section + second_section  # Return the formatted text

def get_web_data(link, command_source): # Get web data from link
    success = False  # Boolean for whether link is valid
    headers = {  # HTTP connection headers
        'User-Agent': 'CS Pound Discord Bot Agent ' + version,  # Connecting User-Agent
        'From': 'jumpy12359@gmail.com'  # Contact email
    }
    if link == '':  # If no link provided
        return success, discord.Embed(title=command_source.capitalize(), description='You didn\'t provide a ' + command_source + ' link!', colour=0xff5252)  # Embed message of not providing link
    else:  # If arguments provided
        try:  # Checking link format
            parameters = link.split('?')[1].split('&')  # Get the PHP $GET values
            success = True  # Link is valid
        except IndexError:  # If cannot get $GET value
            return success, discord.Embed(title=command_source.capitalize(), description='That is not a valid ' + command_source + ' link!', colour=0xff5252)  # Embed message of not valid link
        if success:  # If link exists and is valid
            data = {}  # PHP $POST parameters
            if command_source == 'pet':  # If function is being called from the Pet command
                base_link = 'http://www.chickensmoothie.com/viewpet.php'  # Base PHP link for Pet Command
                parameters = parameters[0].split('=')  # Split the $POST variable
                data[parameters[0]] = parameters[1]  # Add dictionary item with $POST variable and value
            elif command_source == 'oekaki':  # If function is being called from the Oekaki command
                base_link = 'http://www.chickensmoothie.com/Forum/viewtopic.php'
                for i in range(len(parameters)):  # For each parameter
                    temp = parameters[i].split('=')  # Split the $POST variables
                    data[temp[0]] = temp[1]  # Add dictionary item with $POST variable and value
            elif command_source == 'pound':  # If function is being called from the Pound command
                pass

            response = requests.post(base_link, params=data)  # Request HTML page data
            dom = lxml.html.fromstring(response.text)  # Extract HTML from site
            return success, dom  # Return whether connection was successful and DOM data
        else:
            return success  # Return whether connection was successful

# -------------------- DISCORD BOT SETTINGS --------------------
client = Bot(description='CS Pound by Peko#7955', command_prefix=prefix, pm_help=None)
client.remove_command('help')  # Remove default command help to add custom help
logger = logging.getLogger('discord')  # Create logger
logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')  # Set logging file
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))  # Set logging format
logger.addHandler(handler)  # Start logger


@client.event
async def on_ready():  # When Client is loaded
    print('Logged in as ' + client.user.name + ' (ID: ' + client.user.id + ')')
    print('--------')
    print('Current Discord.py Version: {}'.format(discord.__version__))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=134144'.format(client.user.id))
    print('--------')
    print('You are running ' + client.user.name + ' v' + version)
    print('Created by Peko#7955')
    await client.change_presence(game=discord.Game(name=',help | By: Peko#7955'), status=discord.Status.online)  # Change Playing Discord bot is playing


# -------------------- HELP COMMAND --------------------
@client.command(pass_context=True)
async def help(ctx, args=''):  # Help Command
    embed = discord.Embed(colour=0x4ba139)  # Create empty embed
    # -------------------- CHICKENSMOOTHIE HELP --------------------
    if args == 'archive':  # If requested Archive command help
        embed.add_field(name='**Archive**', value=archive_help)  # Add Archive help information to embed
    elif args == 'fair':  # If requested Fair command help
        embed.add_field(name='**Fair', value=fair_help)  # Add Fair help information to embed
    elif args == 'oekaki':  # If requested Oekaki command help
        embed.add_field(name='**Oekaki**', value=oekaki_help)  # Add Oekaki help information to embed
    elif args == 'pet':  # If included 'pet' argument
        embed.add_field(name='**Pet**', value=pet_help)  # Embed Pet help information
    elif args == 'pet2':  # If included 'pet2' argument
        embed.add_field(name='**Pet2**', value=pet2_help)  # Embed Pet2 help information
    elif args == 'time':  # If included 'time' argument
        embed.add_field(name='**Time**', value=time_help)  # Embed Time help information
    elif args == 'trade':  # If included 'trade' argument
        embed.add_field(name='**Trade**', value=trade_help)  # Embed Trade help information

    # -------------------- GENERAL HELP --------------------
    elif args == 'autoremind':  # If included 'autoremind' argument
        embed.add_field(name='**Auto Remind**', value=autoremind_help)  # Embed Auto Remind help information
    elif args == 'remindme':  # If included 'remineme' argument
        embed.add_field(name='**Remind Me**', value=remindme_help)  # Embed Remind Me help information

    # -------------------- INFORMATIONAL HELP --------------------
    elif args == 'help':  # If included 'help' argument
        embed.add_field(name='**Help**', value=help_help)  # Embed Help help information
    elif args == 'support':
        embed.add_field(name='**Support**', value=support_help)
    elif args == 'statistics':
        embed.add_field(name='**Statistics**', value=statistics_help)

    else:  # If provided no arguments
        embed.add_field(name=":pencil: __**To know about command usage or examples, use: ,help <command>**__", value=warning_help)  # add Warning help information to embed
        embed.add_field(name=':dog: __**ChickenSmoothie Commands**__', value=chickensmoothie_help)  # Embed title
        embed.add_field(name=':file_folder: __**General Commands**__', value=general_help)
        embed.add_field(name=':wrench: __**Informational Commands**__', value=informational_help)
    try:
        await client.whisper(embed=embed)
        if ctx.message.channel.is_private:
            embed = discord.Embed()
        else:
            embed = discord.Embed(title='Help', description='A PM has been sent to you!', colour=0x4ba139)
            await client.say(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(title='Help', description='A PM couldn\'t be sent to you, it may be that you have \'Allow direct messages from server members\' disabled in your privacy settings.', colour=0xff5252)
        await client.say(embed=embed)

# -------------------- AUTOREMIND COMMAND --------------------
@client.command(no_pm=True)  # Disable PM'ing the Bot
async def autoremind(args, time='10m'):  # Autoremind command
    embed = discord.Embed(title='Auto Remind', description='This command is still under development!', colour=0xff5252)
    # subprocess.Popen('grep -n \'7954161711\' autoremind.txt | cut -f1 -d:', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1]
    # linecache.getline('autoremind.txt', 11)[:-1]
    await client.say(embed=embed)


# -------------------- IMG COMMAND --------------------
@client.command(no_pm=True, aliases=['img'])  # Disable PM'ing the Bot
async def image(link: str=''):  # Autoremind command
    data = get_web_data(link, 'pet')
    if data[0]:
        petimg = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
        if 'trans' in petimg:  # If pet image is transparent (i.e. Pet has items)
            petimg = 'http://www.chickensmoothie.com' + petimg  # Pet image link
        owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet

        embed = discord.Embed(title=owner_name + '\'s Pet', colour=0x4ba139)  # Create Discord embed
        embed.set_image(url=petimg)  # Set image
        await client.say(embed=embed)
    else:
        await client.say(embed=data[1])


# -------------------- OEKAKI COMMAND --------------------
@client.command(no_pm=True)  # Disable PM'ing the Bot
async def oekaki(link: str=''):  # Oekaki command
    data = get_web_data(link, 'oekaki')
    if data[0]:
        base_link = 'http://www.chickensmoothie.com/Forum/'
        
        oekaki_title = data[1].xpath('//h3[@class="first"]/a/text()')[0]
        image = data[1].xpath('//li[@class="ok-topic-head-image large"]/img/@src')[0]
        #user_icon = base_link + data[1].xpath('//dl[@class="postprofile"]')[0].xpath('dt/a/img/@src')[0][1:]
        #titles = data[1].xpath('//table[@class="ok-drawing-info"]/tr/td[@class="label"]/text()')
        warning_title = 'Reminder!'
        warning_text = 'Copying another person\'s art without permission to reproduce their work is a form of art-theft! [Read the full art rules here.](http://www.chickensmoothie.com/Forum/viewtopic.php?f=10&t=30437)'

        if data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')[0] == 'Click to view':
            artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/@href')
            artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/text()')  # Is Based on
        else:
            artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/@href')
            artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')  # No Based on

        artist_text = '[' + artist_values[0] + '](' + base_link + artist_links[0][1:] + ') [' + artist_values[1] + '(' + base_link + artist_links[1][1:] + ')]'
        
        embed = discord.Embed(title=oekaki_title, colour=0x4ba139, url=link)  # Create Discord embed
        embed.add_field(name='Artist', value=artist_text)
        embed.add_field(name=warning_title, value=warning_text)

        #embed.add_field(name=titles[0], value=artist_text)

        # TITLE dom.xpath('//div[@class="inner"]/h3/a/text()')
        # TITLE URL dom.xpath('//div[@class="inner"]/h3/a/@href') OR JUST ORIGINAL LINK PROVIDED

        # ALL TITLES AND VALUES dom.xpath('//table[@class="ok-drawing-info"]/tr/td/text()')
        # Could split x[0], x[1] AND x[2], x[3] AND x[4], x[5]

        # HOW MANY PEOPLE LIKE THIS dom.xpath('//span[@class="liked_people"]/text()')

        embed.set_image(url=image)
        #embed.set_thumbnail(url=user_icon)
        await client.say(embed=embed)
    else:
        await client.say(embed=data[1])

# -------------------- PET COMMAND --------------------
@client.command(no_pm=True)  # Disable PM'ing the Bot
async def pet(link: str=''):  # Pet command
    data = get_web_data(link, 'pet')
    if data[0]:
        titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
        values = data[1].xpath('//td[@class="r"]')  # Values of pet information
        tables = len(titles)
        given = True  # Pet has been given by another user
        value_list = []

        petimg = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
        if 'trans' in petimg:  # If pet image is transparent (i.e. Pet has items)
            petimg = 'http://www.chickensmoothie.com' + petimg  # Pet image link
        owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet
        owner_link = 'http://www.chickensmoothie.com/' + data[1].xpath('//td[@class="r"]/a/@href')[0]  # Link to user profile

        if titles[0] == 'PPS':  # If pet is PPS
            value_list.append('[This pet has "PPS". What\'s that?](http://www.chickensmoothie.com/help/pets#pps)')  # Append PPS value
            value_list.append('[' + owner_name + '](' + owner_link + ')')  # Append user value
            pps = True
        else:  # If pet is not PPS
            value_list.append('[' + owner_name + '](' + owner_link + ')')  # Append user value
            pps = False

        temp = tables - 1 if pps else tables
        for i in range(temp):  # For each title in titles
            if i == 0:  # If 'i' is at first value (PPS or Owner name)
                pass  # Pass as first value has already been set
            elif temp - i == 2 or temp - i == 1:  # If 'i' is at second last or last value
                if titles[i] == ('Age:' if pps else 'Growth:') or not given:  # If text of titles at 'i' is 'Age:' if pet is PPS otherwise 'Growth:' or pet not given
                    given = False
                    if temp - i == 2:  # If 'i' is second last value (i.e. Growth)
                        value_list.append(values[i].xpath('text()')[0])  # Append growth of pet
                    elif temp - i == 1:  # If 'i' is last value (i.e. Rarity)
                        value_list.append(values[i].xpath('img/@alt')[0])  # Append rarity of pet
                elif titles[i] == ('Growth:' if pps else 'Rarity:') or given:  # If text of titles at 'i' is 'Growth:' is pet is PPS otherwise 'Rarity:' or pet is given
                    given = True
                    if temp - i == 2:  # If 'i' is second last value (i.e. Rarity)
                        value_list.append(values[i].xpath('img/@alt')[0])  # Append rarity of pet
                    elif temp - i == 1:  # If 'i' is last value (i.e. Given by)
                        titles[i] = titles[i].replace('\t', '').replace('\n', '')  # Remove extra formatting
                        value_list.append('[' + data[1].xpath('//td[@class="r"]/a/text()')[1] + ']' + '(' + 'http://www.chickensmoothie.com/' + data[1].xpath('//td[@class="r"]/a/@href')[1] + ')')  # Append given user profile
            else:  # Any other 'i'
                value_list.append(values[i].xpath('text()')[0])  # Append text

        embed = discord.Embed(title=owner_name + '\'s Pet', colour=0x4ba139)  # Create Discord embed
        embed.set_image(url=petimg)  # Set image

        for i in range(tables):  # For each title in titles
            if i == 0:  # If 'i' is first value (PPS or Owner name)
                embed.add_field(name=titles[i], value=value_list[i], inline=False)  # Add field with no inline
            else:  # Any other 'i'
                embed.add_field(name=titles[i], value=value_list[i], inline=True)  # Add field with inline
        await client.say(embed=embed)
    else:
        await client.say(embed=data[1])


# -------------------- PET2 COMMAND --------------------
@client.command(no_pm=True)  # Disable PM'ing the Bot
async def pet2(link: str=''):  # Pet2 command
    data = get_web_data(link, 'pet')
    if data[0]:  # If connection is made
        titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
        values = data[1].xpath('//td[@class="r"]')  # Values of pet information
        tables = len(values)
        given = True  # Pet has been given by another user
        value_list = []

        petimg = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
        if 'trans' in petimg:  # If pet image is transparent (i.e. Pet has items)
            petimg = 'http://www.chickensmoothie.com' + petimg  # Pet image link
        owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet
        owner_link = 'http://www.chickensmoothie.com/' + data[1].xpath('//td[@class="r"]/a/@href')[0]  # Link to user profile
        image_name = petimg.replace('http://static.chickensmoothie.com/pic.php?k=', '').replace('&bg=e0f6b2', '')  # Pet ID
        store_location = 'pets/' + image_name + '.jpg'  # Storage location of pet image files
        if image_name + '.jpg' not in os.listdir('pets/'):  # If image doesn't already exist in pet/
            urllib.request.urlretrieve(petimg, store_location)  # Download image and save to pets/

        if titles[0] == 'PPS':  # If pet is PPS
            value_list.append('This pet has "PPS". What\'s that?')  # Append PPS text
            value_list.append(owner_name)  # Append user name
            pps = True
        else:
            value_list.append(owner_name)  # Append user name
            pps = False

        for i in range(tables):  # For each value in values
            if i == 0:  # If 'i' is at first value (PPS or Owner name)
                pass  # Pass as first value has already been set
            elif tables - i == 2 or tables - i == 1:  # If 'i' is at second last or last value
                if titles[i] == ('Age:' if pps else 'Growth:') or not given:  # If text of titles at 'i' is 'Age:' if pet is PPS otherwise 'Growth:' or pet not given
                    given = False
                    if tables - i == 2:  # If 'i' is second last value (i.e. Growth)
                        value_list.append(values[i].xpath('text()')[0])  # Append growth of pet
                    elif tables - i == 1:  # If 'i' is last value (i.e. Rarity)
                        value_list.append('')  # Append nothing as it will be an image
                        specified_rarity = 'rarities/' + values[i].xpath('img/@src')[0][12:]  # Link to rarity image
                elif titles[i] == ('Growth:' if pps else 'Rarity:') or given:  # If text of titles at 'i' is 'Growth:' is pet is PPS otherwise 'Rarity:' or pet is given
                    given = True
                    if tables - i == 2:  # If 'i' is second last value (i.e. Rarity)
                        value_list.append('')  # Append nothing as it will be an image
                        specified_rarity = 'rarities/' + values[i].xpath('img/@src')[0][12:]  # Link to rarity image
                    elif tables - i == 1:  # If 'i' is last value (i.e. Given by)
                        titles[i] = titles[i].replace('\t', '').replace('\n', '')  # Remove extra formatting
                        given_by = data[1].xpath('//td[@class="r"]/a/text()')[1]
                        value_list.append(data[1].xpath('//td[@class="r"]/a/text()')[1])  # Name of given user
            else:  # Any other 'i'
                value_list.append(values[i].xpath('text()')[0])  # Append text

        image_files = [store_location, specified_rarity]  # Images list

        title_font = ImageFont.truetype('Verdana Bold.ttf', 15)  # Verdana Bold font size 15
        value_font = ImageFont.truetype('Verdana.ttf', 15)  # Verdana font size 15

        images = map(Image.open, image_files)  # Map the image files
        widths, heights = zip(*(i.size for i in images))  # Tuple of widths and heights of both images
        images = list(map(Image.open, image_files))  # List of image file name

        temp_draw = ImageDraw.Draw(Image.new('RGBA', (0, 0)))  # Temporary drawing canvas to calculate text sizes

        max_width = max(widths)  # Max width of images
        total_height = sum(heights) + (30 * len(titles))  # Total height of images
        current_width = 0
        for i in range(len(titles)):  # For each title in titles
            temp_width = temp_draw.textsize(titles[i], font=title_font)[0] + temp_draw.textsize(value_list[i], font=value_font)[0] + 10  # Width of text
            if current_width < temp_width:  # If current width is less than width of texts
                current_width = temp_width
                max_width = temp_width * 2

        image = Image.new('RGBA', (max_width, total_height))  # Create image of max_width x total_height
        d = ImageDraw.Draw(image)

        y_offset = 0  # Offset for vertically stacking images
        image.paste(images[0], (math.floor((max_width - images[0].size[0])/2), y_offset))  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2)
        y_offset += images[0].size[1] + 10  # Add height of image + 10 to offset
        for i in range(len(titles)):  # For each title in titles
            d.text((math.floor(((max_width - math.floor(d.textsize(titles[i], font=title_font)[0]))/2) - math.floor((d.textsize(titles[i], font=title_font)[0]/2))) - 5, y_offset), titles[i], fill=(0, 0, 0), font=title_font)  # Paste text at 'i' at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset)
            if titles[i] == 'Rarity:':  # If text at 'i' is 'Rarity:'
                image.paste(images[1], (math.floor(((max_width - math.floor(d.textsize(titles[i], font=title_font)[0]))/2) + math.floor((d.textsize(titles[i], font=title_font)[0]/2))) + 5, y_offset))  # Paste second image at ((MAX_WIDTH - (TEXT_WIDTH / 2) + (TEXT_WIDTH / 2) + 5, y_offset)
                y_offset += 5  # Add offset of 5
            elif titles[i] == 'Owner:' or 'Given to' in titles[i] or titles[i] == 'PPS':  # If title at 'i' is 'Owner' or 'Given to' or 'PPS'
                d.text((math.floor(((max_width - math.floor(d.textsize(value_list[i], font=value_font)[0]))/2) + math.floor((d.textsize(value_list[i], font=value_font)[0]/2))) + 5, y_offset), value_list[i], fill=(0, 0, 255), font=value_font)
            else:  # If any other 'i'
                d.text((math.floor(((max_width - math.floor(d.textsize(value_list[i], font=value_font)[0]))/2) + math.floor((d.textsize(value_list[i], font=value_font)[0]/2))) + 5, y_offset), value_list[i], fill=(0, 0, 0), font=value_font)
            y_offset += 30  # Add offset of 30

        pixels = image.load()  # Load image pixel data
        for y in range(image.size[1]):  # For each y pixel in image height
            for x in range(image.size[0]):  # For each x pixel in image width
                if pixels[x, y][3] < 5:    # If pixel alpha value is < 5
                    pixels[x, y] = (225, 246, 179, 255)

        image.save('pet.png', 'PNG')  # Save image as pet.png

        im = pyimgur.Imgur(CLIENT_ID, client_secret=CLIENT_SECRET, access_token='fc5c0ffccff4387cef948df004edb1411575eaac', refresh_token='54b539be920b6327b31537ea7ad2514093a5c661')  # Connect to Imgur
        uploaded_image = im.upload_image(path='pet.png', title=owner_name + '\'s Pet', description=image_name, album='BiVzx')  # Upload image

        embed = discord.Embed(title=owner_name + '\'s Pet', colour=0x4ba139)  # Create Discord embed
        embed.set_image(url=uploaded_image.link)  # Set image as uploaded Imgur image link
        await client.say(embed=embed)
        os.system('rm pet.png')  # Delete pet.png
    else:
        await client.say(embed=data[1])


# -------------------- REMINDME COMMAND --------------------
@client.command(pass_context=True, aliases=['rm'])  # Pass information of sending user
async def remindme(ctx, amount: str):  # Remindme command
    if ctx.message.server is None:  # If message source does not come from a server (i.e. PM)
        pass
    else:  # If message comes from server
        finaltotal = time_extractor(amount)  # Get formatted times
        if finaltotal[0] == 0:  # If no time specified
            embed = discord.Embed(title='Remind Me', description='That is not a valid time!', colour=0xff5252)  # Add invalid time message to embed
            await client.say(embed=embed)
        elif finaltotal[0] > 86400:  # If time is longer than 24 hours
            embed = discord.Embed(title='Remind Me', description='That time is too long!', colour=0xff5252)
            await client.say(embed=embed)
        else:  # If time is valid
            before_message = 'A reminder has been set for {0.mention} in '.format(ctx.message.author) + resolver(0, finaltotal[1], finaltotal[2], finaltotal[3]) + '.'
            embed = discord.Embed(title='Remind Me', description=before_message, colour=0x4ba139)
            await client.say(embed=embed)
            after_message = 'Reminder for {0.mention}!'.format(ctx.message.author)
            await asyncio.sleep(finaltotal[0])
            await client.say(after_message)


# -------------------- STATS COMMAND --------------------
@client.command(no_pm=True, aliases=['stats'])  # Disable PM'ing the Bot
async def statistics():  # Stats command
    def converter(seconds):  # Convert seconds into days, hours, minutes and seconds
        d = datetime(1, 1, 1) + timedelta(seconds=int(seconds))  # Create tuple of date values
        return d.day-1, d.hour, d.minute, d.second
    system_memory = str(psutil.virtual_memory()[2]) + '%'  # Get the available virtual memory (physical memory) of the system
    bot_memory = str(round(psutil.Process(os.getpid()).memory_info()[0] / 1024**2, 2)) + ' MB'  # Get the memory usage of this python process
    discord_py_version = discord.__version__  # Discord.py version
    server_count = str(len(client.servers))  # The number of servers this CS Pound is in
    member_count = str(len(set(client.get_all_members())))  # The number of users the CS Pound is connected to
    bot_uptime = converter((datetime.now() - start_time).total_seconds())
    system_uptime = converter(round(pytime.time() - psutil.boot_time()))

    bot_uptime = resolver(bot_uptime[0], bot_uptime[1], bot_uptime[2], bot_uptime[3])
    system_uptime = resolver(system_uptime[0], system_uptime[1], system_uptime[2], system_uptime[3])

    embed = discord.Embed(title='Stats', description='', colour=0x4ba139)  # Create empty embed with the title 'Stats'
    embed.add_field(name='System Memory Usage', value=system_memory, inline=False)  # Add system memory usage to embed
    embed.add_field(name=client.user.name + ' Memory Usage', value=bot_memory, inline=False)  # Add bot memory usage to embed
    embed.add_field(name=client.user.name + ' Version', value=version, inline=False)  # Add bot version to embed
    embed.add_field(name='Discord.py Version', value=discord_py_version, inline=False)  # Add Discord.py version to embed
    embed.add_field(name='Server Count', value=server_count, inline=False)  # Add server count to embed
    embed.add_field(name='Member Count', value=member_count, inline=False)  # Add member count to embed
    embed.add_field(name=client.user.name + ' Uptime', value=bot_uptime, inline=False)  # Add bot uptime to embed
    embed.add_field(name='System Uptime', value=system_uptime, inline=False)  # Add system uptime to embed
    await client.say(embed=embed)  # Display the embed message


# -------------------- SUPPORT COMMAND --------------------
@client.command()
async def support():  # Support command
    try:  # Test if PM can be sent
        await client.whisper('https://discord.gg/PbzHqm9')  # Discord link to the CS-Pound Development Server
        embed = discord.Embed(title='Support', description='A PM has been sent to you!', colour=0x4ba139)  # Add success messsage to embed
    except discord.errors.Forbidden:  # If PM can't be sent
        embed = discord.Embed(title='Support', description='A PM couldn\'t be sent to you, it may be that you have \'Allow direct messages from server members\' disabled in your privacy settings.', colour=0xff5252)  # Add unable to send embed message to embed
    await client.say(embed=embed)  # Display the embed message



# -------------------- TIME COMMAND --------------------
@client.command(no_pm=True, aliases=['pound'])  # Disable PM'ing the Bot
async def time():  # Time command
    connection = urllib.request.urlopen('http://www.chickensmoothie.com/pound.php')  # Connect to ChickenSmoothie Pound webpage
    dom = lxml.html.fromstring(connection.read())  # Extract HTML from site
    text = dom.xpath('//h2/text()')  # Get text of h2 elements

    try:
        if ':)' in text[1]:  # If :) in text
            output = text[1][:-85].replace('\n', r'').replace('\t', r'') + ' The pound opens at totally random times of day, so check back later to try again :)'  # Remove excess formatting text
        else:  # If any other text in text
            output = text[1].replace('Sorry, the pound is closed at the moment.', '').replace('\n', r'').replace('\t', r'') + '.'
    except IndexError:  # If text doesn't exist
        output = 'Pound is currently open!'

    embed = discord.Embed(title='Time', description=output, colour=0x4ba139)
    await client.say(embed=embed)


# -------------------- TRADE COMMAND --------------------
@client.command(no_pm=True)  # Disable PM'ing the Bot
async def trade(link: str):  # Trade command
    # -------------------- SINGLE --------------------
    # CS for CS - NOT POSSIBLE
    # CS for Item -
    # CS for Items -
    # CS for Nothing - http://www.chickensmoothie.com/trades/viewtrade.php?id=59757406&userid=841634&signature=pUx-1Cu5mIrMmid1Pma3Hg
    # CS for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70918155&userid=637563&signature=eBWgqHuAoANFvtQ5K4uStw
    # CS for Pets - http://www.chickensmoothie.com/trades/viewtrade.php?id=70593080&userid=860480&signature=9NHDwxASVbGUEGVFkLxz4Q

    # Item for Item - http://www.chickensmoothie.com/trades/viewtrade.php?id=70677823&userid=785388&signature=GqqEKyNntwu1HHJpZ9ZYZw
    # Item for Items -
    # Item for Nothing -
    # Item for Pet -
    # Item for Pets -

    # Items for Items -
    # Items for Nothing - http://www.chickensmoothie.com/trades/viewtrade.php?id=70682077&userid=774240&signature=GkAYl_h3Ckh4oW4btErBLQ
    # Items for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70647510&userid=752234&signature=LUv9AageFFlJoBqdWcgdGw
    # Items for Pets - http://www.chickensmoothie.com/trades/viewtrade.php?id=70636452&userid=841634&signature=hVN5UG3C-A67wNu97w9Yjg

    # Pet for Nothing - http://www.chickensmoothie.com/trades/viewtrade.php?id=70508510&userid=841634&signature=eM2zskjOK_JJ8ib1k590TA
    # Pet for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70825942&userid=841634&signature=ww70aosoToHU0UIi0t9Axg
    # Pet for Pets - http://www.chickensmoothie.com/trades/viewtrade.php?id=70981341&userid=680104&signature=8KXjvplmOEkB5hlBU2JooQ

    # Pets for Nothing - http://www.chickensmoothie.com/trades/viewtrade.php?id=70709592&userid=841634&signature=8XyEtMg95aNJaK8o4FzbDA

    # -------------------- DOUBLE --------------------
    # Pet & CS for CS - NOT LIKELY
    # Pet & CS for Item -
    # Pet & CS for Items -
    # Pet & CS for Nothing -
    # Pet & CS for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70709033&userid=850489&signature=fLCQUHEjiFIsb9K3G55TKw
    # Pet & CS for Pets -

    # Pet & Item for CS -
    # Pet & Item for Item -
    # Pet & Item for Items -
    # Pet & Item for Nothing -
    # Pet & Item for Pet -
    # Pet & Item for Pets -

    # Pet & Items for CS -
    # Pet & Items for Item -
    # Pet & Items for Items -
    # Pet & Items for Nothing -
    # Pet & Items for Pet -
    # Pet & Items for Pets - http://www.chickensmoothie.com/trades/viewtrade.php?id=70656174&userid=841634&signature=KEDJPnRWztNyu2zjQzv8Ig

    # Pets & CS for CS - NOT LIKELY
    # Pets & CS for Item -
    # Pets & CS for Items -
    # Pets & CS for Nothing - http://www.chickensmoothie.com/trades/viewtrade.php?id=70647444&userid=841634&signature=_Xrq30ZlTjPFDm4O2pue6Q
    # Pets & CS for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70862085&userid=916377&signature=bIzCc1ONVtrEE6FcNdaoIA
    # Pets & CS for Pets - http://www.chickensmoothie.com/trades/viewtrade.php?id=70602251&userid=860480&signature=gXvTHcHUwasU-y9KMcoWfw

    # Pets & Item for CS -
    # Pets & Item for Item -
    # Pets & Item for Items -
    # Pets & Item for Nothing -
    # Pets & Item for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70710482&userid=716769&signature=5-vWlkNnUOSwqgN8SiLSLg
    # Pets & Item for Pets -

    # Pets & Items for CS - http://www.chickensmoothie.com/trades/viewtrade.php?id=70497300&userid=841634&signature=Cb6wsO2LD85mJTzef2LGrQ
    # Pets & Items for Item - http://www.chickensmoothie.com/trades/viewtrade.php?id=70689635&userid=369413&signature=2be6oDbNrqONGyXLf9mWHg
    # Pets & Items for Items -
    # Pets & Items for Nothing - http://www.chickensmoothie.com/trades/viewtrade.php?id=69538685&userid=841634&signature=dmcf3rGMDHfHWa217U-taw
    # Pets & Items for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70632848&userid=167347&signature=8IC6-eCUI5ksPorFoen0PQ
    # Pets & Items for Pets -

    # Item & CS for CS - NOT LIKELY
    # Item & CS for Item -
    # Item & CS for Items -
    # Item & CS for Nothing -
    # Item & CS for Pet -
    # Item & CS for Pets -

    # Items & CS for CS - NOT LIKELY
    # Items & CS for Item -
    # Items & CS for Items -
    # Items & CS for Nothing -
    # Items & CS for Pet -
    # Items & CS for Pets -

    # -------------------- TRIPLE --------------------
    # Pet & Item & CS for CS - NOT LIKELY
    # Pet & Item & CS for Item -
    # Pet & Item & CS for Items -
    # Pet & Item & CS for Nothing -
    # Pet & Item & CS for Pet -
    # Pet & Item & CS for Pets -

    # Pet & Items & CS for CS - NOT LIKELY
    # Pet & Items & CS for Item -
    # Pet & Items & CS for Items -
    # Pet & Items & CS for Nothing -
    # Pet & Items & CS for Pet -
    # Pet & Items & CS for Pets -

    # Pets & Item & CS for CS - NOT LIKELY
    # Pets & Item & CS for Item -
    # Pets & Item & CS for Items -
    # Pets & Item & CS for Nothing -
    # Pets & Item & CS for Pet -
    # Pets & Item & CS for Pets -

    # Pets & Items & CS for CS - NOT LIKELY
    # Pets & Items & CS for Item -
    # Pets & Items & CS for Items -
    # Pets & Items & CS for Nothing -
    # Pets & Items & CS for Pet - http://www.chickensmoothie.com/trades/viewtrade.php?id=70863369&userid=916377&signature=lrtsp_22iSyFqgEtN8vNJQ
    # Pets & Items & CS for Pets - http://www.chickensmoothie.com/trades/viewtrade.php?id=70685767&userid=860480&signature=MLvj4HtA1Fzt6TscnWkxKw

    embed = discord.Embed(title='Trade', description='This command is still under development!', colour=0xff5252)
    await client.say(embed=embed)

'''
# -------------------- EMBED TEST COMMAND --------------------
@client.command()
async def discordembedtest():
    embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~", colour=0xaf4119, url="https://discordapp.com", description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```")

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="author name", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="🤔", value="some of these properties have certain limits...")
    embed.add_field(name="😱", value="try exceeding some of them!")
    embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
    embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
    embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

    await client.say(embed=embed)

async def countdown():
    await client.wait_until_ready()
    counter = 0
    while not client.is_closed:
        counter += 1
        # await client.send_message(channel, counter)
        await asyncio.sleep(60)

client.loop.create_task(countdown())
'''
client.run(token)  # Start bot
