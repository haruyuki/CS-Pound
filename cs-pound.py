# -------------------- IMPORTS --------------------
import aiohttp
import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import hashlib
import io
import json
import logging
import lxml.html
import math
import os
from PIL import Image, ImageFont, ImageDraw
import platform
import psutil
import subprocess
import time as pytime
import urllib.request

'''
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
call = 'DEV'  # Whether the bot is currently in 'DEV' or 'LIVE' mode
tokens = [token.replace('\n', '') for token in list(open('tokens.txt'))]  # Get tokens from tokens.txt file
cooldown = False  # Cooldown of Auto Remind
help_hash = ''  # Current hash of help.json
autoremind_hash = ''  # Current hash of autoremind.txt
autoremind_times = []  # Unique Auto Remind times

# -------------------- DISCORD --------------------
if call == 'LIVE':  # If being used for production
    token = tokens[0]  # Discord CS Pound Secret Token
    prefix = ','  # Prefix to call CS Pound Discord Bot
    version = '1.8'  # CS Pound Discord Bot version
else:  # If used for testing
    token = tokens[1]  # Discord CS Pound DEV Secret Token
    prefix = '.'  # Prefix to call CS Pound DEV Discord Bot
    reminder = 0
    version = 'DEV'  # CS Pound DEV Discord Bot version

# -------------------- HELP TEXT --------------------
warning_help = '''\
CS Pound website (Where you also get the invite link)
http://tailstar.us

-'''  # Title help

chickensmoothie_help2 = '''\
`,archive <query>` - Search the ChickenSmoothie archives (Under Development)

`,fair <link>` - Determine whether a trade is fair (Under Development)

`,image <link>` - Displays pet image only

`,oekaki <link>` - Displays Oekaki drawing

`,pet <link>` - Displays pet information

`,time` - Tells you how long until the pound opens

`,trade <link>` - Displays trade information (Under Development)

_'''

chickensmoothie_help = '''\
`,image <link>` - Displays pet image only

`,oekaki <link>` - Displays Oekaki drawing

`,pet <link>` - Displays pet information

`,time` - Tells you how long until the pound opens

_'''  # Chicken Smoothie related commands help

general_help = '''\
`,autoremind <on/off> <time>` - Turns on or off global auto reminding (Under Development)

`,remindme <time>` - Pings you after specified amount of time

_'''  # General commands help

informational_help = '''\
`,help` - Displays this message

`,support` - PM's you the link to the CS Pound Development Server

`,statistics` - Displays bot statistics
'''  # Informational commands help


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
    return finaltotal, htotal, mtotal, stotal  # Return a tuple


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


async def get_web_data(link, command_source):  # Get web data from link
    success = False  # Boolean for whether link is valid
    headers = {  # HTTP request headers
        'User-Agent': 'CS Pound Discord Bot Agent ' + version,  # Connecting User-Agent
        'From': 'jumpy12359@gmail.com'  # Contact email
    }
    if link == '' and command_source != 'pound':  # If no link provided
        description = 'You didn\'t provide a ' + command_source + ' link!'
        return success, discord.Embed(title=command_source.capitalize(), description=description, colour=0xff5252)  # Create embed
    else:  # If arguments provided
        try:  # Checking link format
            if command_source != 'pound':  # If command source does not come from ,time
                parameters = link.split('?')[1].split('&')  # Get the PHP $GET values
                success = True  # Link is valid
            else:  # If command source comes from ,time
                success = True
        except IndexError:  # If cannot get $GET value
            return success, discord.Embed(title=command_source.capitalize(), description='That is not a valid ' + command_source + ' link!', colour=0xff5252)  # Create embed
        if success:  # If link exists and is valid
            data = {}  # PHP $POST parameters
            if command_source == 'pet':  # If function is being called from the Pet command
                base_link = 'http://www.chickensmoothie.com/viewpet.php'  # Base PHP link for Pet command
                parameters = parameters[0].split('=')  # Split the $POST variable
                data[parameters[0]] = parameters[1]  # Add dictionary item with $POST variable and value
            elif command_source == 'oekaki':  # If function is being called from the Oekaki command
                base_link = 'http://www.chickensmoothie.com/Forum/viewtopic.php'  # Base PHP link for Oekaki command
                for param in range(len(parameters)):  # For each parameter
                    temp = parameters[param].split('=')  # Split the $POST variables
                    data[temp[0]] = temp[1]  # Add dictionary item with $POST variable and value
            elif command_source == 'pound':  # If function is being called from the Pound command
                base_link = 'http://www.chickensmoothie.com/pound.php'  # Base PHP link for Time command
            async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
                async with session.post(base_link, data=data, headers=headers) as response:  # POST the variables to the base php link
                    connection = await response.text()  # Request HTML page data
                    dom = lxml.html.fromstring(connection)  # Extract HTML from site
            return success, dom  # Return whether connection was successful and DOM data
        else:  # If link is not valid
            return success  # Return whether connection was successful


def process_help(command):  # Get the help text from help.json
    global help_hash

    def monospace(string):  # Returns string in Discord monospace format
        return '`' + string + '`'  # `string`

    def italic(string):  # Returns string in Discord italics format
        return '*' + string + '*'  # *string*

    new_help_hash = hashlib.md5(open('help.json').read().encode()).hexdigest()  # MD5 hash of help.json
    if help_hash != new_help_hash:  # If help.json has been changed
        help_hash = new_help_hash  # Set hash to the new changes
        with open('help.json') as f:  # Open help.json
            help_list = json.load(f)  # Load the JSON data

    command_information = help_list[command]  # Get the command information of the command
    message = monospace(command_information['usage']) + ' - ' + command_information['description']  # `usage` - description
    if command_information['examples']:  # If there are examples for the command
        message += '\n' + italic('Examples:') + ' ' + ', '.join([monospace(value) for key, value in command_information['examples'].items()])  # *Examples:* `example1`, `example2`, `example3`
    
    if command_information['aliases']:  # If there are aliases for the command
        message += '\n' + italic('Aliases:') + ' ' + ', '.join([monospace(value) for key, value in command_information['aliases'].items()])  # *Aliases:* `alias1`, `alias2`, `alias3`
    
    return message


# -------------------- DISCORD BOT SETTINGS --------------------
client = Bot(description='CS Pound by Peko#7955', command_prefix=prefix, pm_help=None)  # Set the bot description and prefix
client.remove_command('help')  # Remove default help command to add custom help
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
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=268569600'.format(client.user.id))
    print('--------')
    print('You are running ' + client.user.name + ' v' + version)
    print('Created by Peko#7955')
    await client.change_presence(game=discord.Game(name=',help | By: Peko#7955'), status=discord.Status.online)  # Change Playing status to ,help | By: Peko#7955


# -------------------- HELP COMMAND --------------------
@client.command(pass_context=True)
async def help(ctx, args=''):  # Help Command
    embed = discord.Embed(colour=0x4ba139)  # Create empty embed
    # -------------------- CHICKENSMOOTHIE HELP --------------------
    if args == 'archive':  # If requested Archive command help
        embed.add_field(name='**Archive**', value=process_help(args))  # Add Archive help information to embed
    elif args == 'fair':  # If requested Fair command help
        embed.add_field(name='**Fair', value=process_help(args))  # Add Fair help information to embed
    elif args == 'oekaki':  # If requested Oekaki command help
        embed.add_field(name='**Oekaki**', value=process_help(args))  # Add Oekaki help information to embed
    elif args == 'pet':  # If included 'pet' argument
        embed.add_field(name='**Pet**', value=process_help(args))  # Embed Pet help information
    elif args == 'pet2':  # If included 'pet2' argument
        embed.add_field(name='**Pet2**', value=process_help(args))  # Embed Pet2 help information
    elif args == 'time':  # If included 'time' argument
        embed.add_field(name='**Time**', value=process_help(args))  # Embed Time help information
    elif args == 'trade':  # If included 'trade' argument
        embed.add_field(name='**Trade**', value=process_help(args))  # Embed Trade help information

    # -------------------- GENERAL HELP --------------------
    elif args == 'autoremind':  # If included 'autoremind' argument
        embed.add_field(name='**Auto Remind**', value=process_help(args))  # Embed Auto Remind help information
    elif args == 'remindme':  # If included 'remineme' argument
        embed.add_field(name='**Remind Me**', value=process_help(args))  # Embed Remind Me help information

    # -------------------- INFORMATIONAL HELP --------------------
    elif args == 'help':  # If included 'help' argument
        embed.add_field(name='**Help**', value=process_help(args))  # Embed Help help information
    elif args == 'support':
        embed.add_field(name='**Support**', value=process_help(args))  # Embed Support help information
    elif args == 'statistics':
        embed.add_field(name='**Statistics**', value=process_help(args))  # Embed Statistics help information

    else:  # If provided no arguments or requested a help topic that doesn't exist
        embed.add_field(name=":pencil: __**To know about command usage or examples, use: ,help <command>**__", value=warning_help)  # add Warning help information to embed
        embed.add_field(name=':dog: __**ChickenSmoothie Commands**__', value=chickensmoothie_help)  # Embed Chicken Smoothie related commands
        embed.add_field(name=':file_folder: __**General Commands**__', value=general_help)  # Embed General commands
        embed.add_field(name=':wrench: __**Informational Commands**__', value=informational_help)  # Embed informational commands
    try:
        await client.whisper(embed=embed)  # PM the embed to the user
        if ctx.message.channel.is_private:  # If the user is calling command from PM
            embed = discord.Embed()  # Replace with new empty embed
        else:  # If the user is calling command from a channel
            embed = discord.Embed(title='Help', description='A PM has been sent to you!', colour=0x4ba139)  # Create embed
            await client.say(embed=embed)  # Send embed
    except discord.errors.Forbidden:  # If cannot send PM to user
        embed = discord.Embed(title='Help', description='A PM couldn\'t be sent to you, it may be that you have \'Allow direct messages from server members\' disabled in your privacy settings.', colour=0xff5252)  # Create embed
        await client.say(embed=embed)  # Send embed


# -------------------- AUTOREMIND COMMAND --------------------
@client.command(pass_context=True, no_pm=True)  # Disallow using this command in PM's
async def autoremind(ctx, args=''):  # Auto Remind command
    grep_statement = 'grep -n \'' + ctx.message.author.id + '\' autoremind.txt | cut -f1 -d:'  # Get line number of ID
    id_exists = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1]  # Run grep statement
    server_roles = ctx.message.server.roles  # List of roles in server
    for role in server_roles:  # For each role in the server
        if role.name == "CS Pound":  # If 'CS Pound' role exists
            permission = role.permissions.manage_roles  # Check whether role has 'Manage Roles' permission and set boolean value
            break  # Break out of for loop
    else:  # If role doesn't exist
        permission = False

    if permission:  # If bot has permission to 'Manage Roles'
        server_roles = ctx.message.server.roles  # List of roles in server
        for role in server_roles:  # Checks if role already exists in server
            if role.name == "Auto Remind":  # If role exists
                break  # Break out of for loop
        else:  # If role doesn't exist
            await client.create_role(ctx.message.server, name='Auto Remind')  # Create 'Auto Remind' role in server

    if args == 'off':  # If user wants to turn off Auto Remind
        if id_exists == '':  # If user doesn't exist in database
            embed = discord.Embed(title='Auto Remind', description='You don\'t have Auto Remind setup {0.mention}!'.format(ctx.message.author), colour=0xff5252)  # Create embed
        else:  # If user exists
            sed_statement = 'sed -i.bak ' + id_exists + 'd autoremind.txt'  # sed statement
            subprocess.Popen(sed_statement, shell=True)  # Run sed statement
            if permission:  # If bot has permission to 'Manage Roles'
                await client.remove_roles(ctx.message.author, discord.utils.get(server_roles, name='Auto Remind'))  # Remove role from user
                embed = discord.Embed(title='Auto Remind', description='You have been removed from the Auto Remind role.', colour=0x4ba139)  # Create embed
            else:  # If bot doesn't have permission to 'Manage Roles'
                embed = discord.Embed(title='Auto Remind', description='You have been removed from the Auto Remind.', colour=0x4ba139)  # Create embed

    else:  # If user is setting an Auto Remind
        valid = False
        if args == '':  # If no arguments provided
            embed = discord.Embed(title='Auto Remind', description='You didn\'t input a time!', colour=0xff5252)  # Create embed
        elif args.isdigit():  # If the input is a digit
            valid = True
        else:  # If the input isn't a digit
            args = args[:-1]  # Remove the minute marker
            if args.isdigit():  # If the input is a digit now
                valid = True
            else:  # If input is still not digit
                embed = discord.Embed(title='Auto Remind', description='That is not a valid time!', colour=0xff5252)  # Create embed

        if valid:  # If inputted time was valid
            if int(args) > 60:  # If time is bigger than 60 minutes
                embed = discord.Embed(title='Auto Remind', description='That time is too far!', colour=0xff5252)  # Create embed
            else:  # If time is less than 60 minutes
                if id_exists != '':  # If user has already set an Auto Remind
                    embed = discord.Embed(title='Auto Remind', description='You already have Auto Remind setup {0.mention}!'.format(ctx.message.author), colour=0xff5252)  # Create embed
                else:  # If user doesn't have an Auto Remind setup
                    text = ctx.message.server.id + ' ' + ctx.message.channel.id + ' ' + ctx.message.author.id + ' ' + args + '\n'  # Write in the format 'SERVER_ID CHANNEL_ID USER_ID REMIND_TIME'
                    with open('autoremind.txt', 'a+') as file:  # Open autoremind.txt
                        file.write(text)  # Write the text

                    if permission:  # If bot has 'Manage Roles' permission
                        await client.add_roles(ctx.message.author, discord.utils.get(server_roles, name='Auto Remind'))  # Add user to Auto Remind role

                    message = 'Will ping you ' + args + ' minutes before the pound opens!'
                    embed = discord.Embed(title='Auto Remind', description=message, colour=0x4ba139)  # Create embed

    await client.say(embed=embed)  # Send embed


# -------------------- IMAGE COMMAND --------------------
@client.command(no_pm=True, aliases=['img'], pass_context=True)  # Disallow using this command in PM's
async def image(ctx, link: str = ''):  # Autoremind command
    data = await get_web_data(link, 'pet')  # Get pet data
    if data[0]:  # If data is valid
        information = {}
        owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet
        titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
        values = data[1].xpath('//td[@class="r"]')  # Values of pet information

        pet_image = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
        if 'trans' in pet_image:  # If pet image is transparent (i.e. Pet has items)
            pet_image = 'http://www.chickensmoothie.com' + pet_image  # Pet image link
            transparent = True
        else:
            transparent = False

        if titles[0] == 'PPS':  # If pet is PPS
            pps = True
        else:  # If pet is not PPS
            pps = False

        if len(titles) + len(values) < 16:  # If the amount of titles and values don't add up
            no_name = True
        else:  # If they add up
            no_name = False

        if no_name:  # If pet has no name
            case1 = 'Pet\'s name:'
            case2 = 'Adopted:'
            case3 = 1
            case4 = 1
            if pps:  # If pet has no name and is PPS
                case1 = 'Pet\'s name:'
                case2 = 'Pet ID:'
                case3 = 2
                case4 = 1
        elif pps:  # If pet has a name and is PPS
            case1 = 'Pet ID:'
            case2 = 'Pet\'s name:'
            case3 = 2
            case4 = 1
        else:  # If pet has a name but is not PPS
            case1 = 'Pet\'s name:'
            case2 = 'Adopted:'
            case3 = 1
            case4 = 1

        temp = len(titles) - 1 if pps else len(titles)  # Is pet is PPS, remove one title, else all titles
        for i in range(temp):  # For each title in titles
            if titles[i] == (case1):
                information['Name'] = values[i].xpath('text()')[0]  # Add pet name to information dictionary
            elif titles[i] == (case2):
                information['Adopted'] = values[i].xpath('text()')[0]  # Add pet adoption date to information dictionary
            elif titles[i] == ('Growth:' if pps else 'Rarity:'):  # If pet is PPS, if titles[i] matches 'Growth:', otherwise if not PPS, if titles[i] matches with 'Rarity:'
                information['Rarity'] = 'rarities/' + values[i].xpath('img/@src')[0][12:]  # Local link to rarity image

        if titles[case3] == 'Pet ID:':
            filename = values[case4].xpath('text()')[0]  # Get pet ID
        else:  # If ID cannot be found
            filename = 'pet'

        async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
            async with session.get(pet_image) as response:  # GET HTTP response of pet image link
                connection = await response.read()  # Read the response content
                pet_image = io.BytesIO(connection)  # Convert the content into bytes

        image_files = [pet_image, information['Rarity']]
        font = ImageFont.truetype('Verdana.ttf', 12)  # Verdana font size 15

        images = map(Image.open, image_files)  # Map the image files
        widths, heights = zip(*(i.size for i in images))  # Tuple of widths and heights of both images
        images = list(map(Image.open, image_files))  # List of image file name

        temp_draw = ImageDraw.Draw(Image.new('RGBA', (0, 0)))  # Temporary drawing canvas to calculate text sizes
        max_width = max(widths)  # Max width of images
        total_height = sum(heights) + (15 * len(information))  # Total height of images
        current_width = 0
        for key, value in information.items():  # For each item in information
            temp_width = temp_draw.textsize(value, font=font)[0]  # Width of text
            if current_width < temp_width:  # If current width is less than width of texts
                current_width = temp_width
                max_width = temp_width * 2

        image = Image.new('RGBA', (max_width, total_height), (225, 246, 179, 255))  # Create an RGBA image of max_width x total_height, with colour 225, 246, 179
        pil_image = ImageDraw.Draw(image)  # Draw the image to PIL

        y_offset = 0  # Offset for vertically stacking images
        if transparent:  # If pet has items
            image.paste(images[0], (math.floor((max_width - images[0].size[0])/2), y_offset), images[0])  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[0]
        else:  # If pet doesn't have items
            image.paste(images[0], (math.floor((max_width - images[0].size[0])/2), y_offset))  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2)
        y_offset += images[0].size[1]  # Add height of image + 10 to offset
        for key, value in information.items():  # For each title in titles
            if key == 'Rarity':  # If key is 'Rarity'
                image.paste(images[1], (math.floor((max_width - images[1].size[0])/2), y_offset), images[1])  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[1]
            else:  # If any other key
                pil_image.text((math.floor(((max_width - math.floor(pil_image.textsize(value, font=font)[0]))/2)), y_offset), value, fill=(0, 0, 0), font=font)  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
            y_offset += 15  # Add offset of 30

        output_buffer = io.BytesIO()  # Convert the PIL output into bytes
        image.save(output_buffer, 'png')  # Save the bytes as a PNG format
        output_buffer.seek(0)  # Move the 'cursor' back to the start

        filename += '.png'  # Set filename as (Pet ID).png

        await client.send_file(ctx.message.channel, fp=output_buffer, filename=filename)  # Upload the file to the channel where message came from
    else:  # If data is invalid
        await client.say(embed=data[1])  # Send embed


# -------------------- OEKAKI COMMAND --------------------
@client.command(no_pm=True)  # Disallow using this command in PM's
async def oekaki(link: str = ''):  # Oekaki command
    data = await get_web_data(link, 'oekaki')  # Get Oekaki data
    if data[0]:  # If data is valid
        base_link = 'http://www.chickensmoothie.com/Forum/'

        oekaki_title = data[1].xpath('//h3[@class="first"]/a/text()')[0]  # Title of drawing
        image = 'https://www.chickensmoothie.com' + data[1].xpath('//li[@class="ok-topic-head-image large"]/img/@src')[0]  # Image of drawing
        user_icon = base_link[:-1] + data[1].xpath('//dl[@class="postprofile"]')[0].xpath('dt/a/img/@src')[0][1:]  # The profile picture of the artist
        titles = data[1].xpath('//table[@class="ok-drawing-info"]/tr/td[@class="label"]/text()')  # Get titles of drawing information
        warning_text = 'Reminder!! Copying another person\'s art without permission to reproduce their work is a form of art-theft!'  # General warning text regarding Oekaki art

        if data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')[0] == 'Click to view':  # If drawing is based off another drawing
            artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/@href')  # Drawing information titles
            artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[1].xpath('td')[1].xpath('a/text()')  # Drawing information values
        else:  # If drawing is not based off another drawing
            artist_links = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/@href')  # Drawing information titles
            artist_values = data[1].xpath('//table[@class="ok-drawing-info"]/tr')[0].xpath('td')[1].xpath('a/text()')  # Drawing information values

        artist_text = '[' + artist_values[0] + '](' + base_link + artist_links[0][1:] + ') [' + artist_values[1] + '(' + base_link + artist_links[1][1:] + ')]'  # [Artist Name](Link to Artist) [gallery](Link to Artist gallery) | Formats to Artist Name [gallery]

        embed = discord.Embed(title=oekaki_title, colour=0x4ba139, url=link)  # Create embed
        embed.add_field(name='Artist', value=artist_text)  # Add Artist field
        embed.set_footer(text=warning_text, icon_url="https://vignette.wikia.nocookie.net/pufflescp/images/6/68/Red_Warning_Triangle.png/revision/latest?cb=20160718024653&format=original")  # Add warning text to footer
        embed.set_image(url=image)  # Add drawing to embed
        embed.set_thumbnail(url=user_icon)  # Set thumbnail as user profile picture

        await client.say(embed=embed)  # Send embed
    else:  # If data is not valid
        await client.say(embed=data[1])  # Send embed


# -------------------- PET COMMAND --------------------
@client.command(no_pm=True)  # Disallow using this command in PM's
async def pet(link: str = ''):  # Pet command
    data = await get_web_data(link, 'pet')  # Get pet data
    if data[0]:  # If data is valid
        titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
        values = data[1].xpath('//td[@class="r"]')  # Values of pet information
        given = True  # Pet has been given by another user
        value_list = []

        petimg = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
        if 'trans' in petimg:  # If pet image is transparent (i.e. Pet has items)
            petimg = 'http://www.chickensmoothie.com' + petimg  # Pet image link
        owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet
        owner_link = 'http://www.chickensmoothie.com/' + data[1].xpath('//td[@class="r"]/a/@href')[0]  # Link to user profile

        if titles[0] == 'PPS':  # If pet is PPS
            value_list.append('[This pet has "PPS". What\'s that?](http://www.chickensmoothie.com/help/pets#pps)')  # Append PPS value
            value_list.append('[' + owner_name + '](' + owner_link + ')')  # [Owner Name](Link to Owner) | Formats to Owner Name
            pps = True
        else:  # If pet is not PPS
            value_list.append('[' + owner_name + '](' + owner_link + ')')  # [Owner Name](Link to Owner) | Formats to Owner Name
            pps = False

        tables = len(titles)  # Number of rows
        temp = tables - 1 if pps else tables  # -1 Rows if pet is PPS
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

        embed = discord.Embed(title=owner_name + '\'s Pet', colour=0x4ba139)  # Create embed
        embed.set_image(url=petimg)  # Set image

        for i in range(tables):  # For each title in titles
            if i == 0:  # If 'i' is first value (PPS or Owner name)
                embed.add_field(name=titles[i], value=value_list[i], inline=False)  # Add field with no inline
            else:  # Any other 'i'
                embed.add_field(name=titles[i], value=value_list[i], inline=True)  # Add field with inline
        await client.say(embed=embed)  # Send embed
    else:  # If data is not valid
        await client.say(embed=data[1])  # Send embed


# -------------------- REMINDME COMMAND --------------------
@client.command(pass_context=True, aliases=['rm'], no_pm=True)  # Disallow using this command in PM's
async def remindme(ctx, amount: str):  # Remind Me command
    finaltotal = time_extractor(amount)  # Get formatted times
    if finaltotal[0] == 0:  # If no time specified
        embed = discord.Embed(title='Remind Me', description='That is not a valid time!', colour=0xff5252)  # Create embed
        await client.say(embed=embed)  # Send embed
    elif finaltotal[0] > 86400:  # If time is longer than 24 hours
        embed = discord.Embed(title='Remind Me', description='That time is too long!', colour=0xff5252)  # Create embed
        await client.say(embed=embed)  # Send embed 
    else:  # If time is valid
        before_message = 'A reminder has been set for {0.mention} in '.format(ctx.message.author) + resolver(0, finaltotal[1], finaltotal[2], finaltotal[3]) + '.'  # A reminder has been set for USER in X hours, Y minutes, and Z seconds.
        embed = discord.Embed(title='Remind Me', description=before_message, colour=0x4ba139)   # Create embed
        await client.say(embed=embed)  # Send embed
        after_message = 'Reminder for {0.mention}!'.format(ctx.message.author)  # Reminder for USER!
        await asyncio.sleep(finaltotal[0])  # Sleep for set time
        await client.say(after_message)  # Send message


# -------------------- STATS COMMAND --------------------
@client.command(no_pm=True, aliases=['stats'])  # Disallow using this command in PM's
async def statistics():  # Statistics command
    def converter(seconds):  # Convert seconds into days, hours, minutes and seconds
        d = datetime(1, 1, 1) + timedelta(seconds=int(seconds))  # Create tuple of date values
        return d.day-1, d.hour, d.minute, d.second  # Return tuple of date values
    system_memory_mb = str(round(psutil.virtual_memory()[3] / 1000 / 1024, 2)) + ' MB'  # Get the used virtual memory (physical memory) of the system | X MB
    system_memory_percent = str(psutil.virtual_memory()[2]) + '%'  # Get the available virtual memory (physical memory) of the system | X%
    bot_memory_mb = str(round(psutil.Process(os.getpid()).memory_info()[0] / 1024**2, 2)) + ' MB'  # Get the memory usage of the bot (i.e. This script) | X MB
    bot_memory_percent = str(round(psutil.Process(os.getpid()).memory_percent(), 2)) + '%'  # Get used memory percentage of the bot (i.e. This script) | X%
    discord_py_version = discord.__version__  # Discord.py version
    server_count = str(len(client.servers))  # The number of servers this CS Pound is in
    member_count = str(len(set(client.get_all_members())))  # The number of unique users the CS Pound is connected to
    bot_uptime = converter((datetime.now() - start_time).total_seconds())  # The time the bot (script) has been running
    system_uptime = converter(round(pytime.time() - psutil.boot_time()))  # The time the system has been running

    bot_uptime = resolver(bot_uptime[0], bot_uptime[1], bot_uptime[2], bot_uptime[3])  # Pretty format the bot uptime
    system_uptime = resolver(system_uptime[0], system_uptime[1], system_uptime[2], system_uptime[3])  # Pretty format the system uptime

    embed = discord.Embed(title='Stats', description='', colour=0x4ba139)  # Create empty embed
    embed.add_field(name='System Memory Usage', value=system_memory_percent + ' (' + system_memory_mb + ')', inline=False)  # Add system memory usage to embed
    embed.add_field(name=client.user.name + ' Memory Usage', value=bot_memory_percent + ' (' + bot_memory_mb + ')', inline=False)  # Add bot memory usage to embed
    embed.add_field(name=client.user.name + ' Version', value=version, inline=False)  # Add bot version to embed
    embed.add_field(name='Discord.py Version', value=discord_py_version, inline=False)  # Add Discord.py version to embed
    embed.add_field(name='Server Count', value=server_count, inline=False)  # Add server count to embed
    embed.add_field(name='Member Count', value=member_count, inline=False)  # Add member count to embed
    embed.add_field(name=client.user.name + ' Uptime', value=bot_uptime, inline=False)  # Add bot uptime to embed
    embed.add_field(name='System Uptime', value=system_uptime, inline=False)  # Add system uptime to embed
    await client.say(embed=embed)  # Send embed


# -------------------- SUPPORT COMMAND --------------------
@client.command()
async def support():  # Support command
    try:
        await client.whisper('https://discord.gg/PbzHqm9')  # PM Discord link to the CS-Pound Development Server to user
        embed = discord.Embed(title='Support', description='A PM has been sent to you!', colour=0x4ba139)  # Create embed
    except discord.errors.Forbidden:  # If cannot send PM to user
        embed = discord.Embed(title='Support', description='A PM couldn\'t be sent to you, it may be that you have \'Allow direct messages from server members\' disabled in your privacy settings.', colour=0xff5252)  # Create embed
    await client.say(embed=embed)  # Send embed


# -------------------- TIME COMMAND --------------------
@client.command(no_pm=True, aliases=['pound'])  # Disallow using this command in PM's
async def time():  # Time command
    async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
        async with session.get('http://www.chickensmoothie.com/pound.php') as response:  # GET HTTP response of pound page
            connection = await response.text()  # Request HTML page data
            dom = lxml.html.fromstring(connection)  # Extract HTML from site
            text = dom.xpath('//h2/text()')  # Pound opening text

    try:
        if ':)' in text[1]:  # If :) in text
            output = text[1][:-85].replace('\n', r'').replace('\t', r'') + ' The pound opens at totally random times of day, so check back later to try again :)'  # Remove excess formatting text
        else:  # If any other text in text
            output = text[1].replace('Sorry, the pound is closed at the moment.', '').replace('\n', r'').replace('\t', r'') + '.'
    except IndexError:  # If text doesn't exist
        output = 'Pound is currently open!'

    embed = discord.Embed(title='Time', description=output, colour=0x4ba139)  # Create embed
    await client.say(embed=embed)  # Send embed


# -------------------- TRADE COMMAND --------------------
@client.command(no_pm=True)  # Disallow using this command in PM's
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

    embed = discord.Embed(title='Trade', description='This command is still under development!', colour=0xff5252)  # Create embed
    await client.say(embed=embed)  # Send embed


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
'''


async def compose_message(time):  # Function to compose and send mention messages to channels
    grep_statement = 'grep \'[0-9]*\\s[0-9]*\\s[0-9]*\\s' + time + '\' autoremind.txt | cut -f2 -d\' \' | sort -u'  # Get channels with Auto Remind set at 'time'
    channel_ids = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run grep statement
    for i in range(len(channel_ids)):  # For each Discord channel ID
        grep_statement = 'grep \'[0-9]*\\s' + channel_ids[i] + '\\s[0-9]*\\s' + time + '\' autoremind.txt | cut -f3 -d\' \''  # Grab all unique Discord user ID's with that channel ID
        user_ids = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run grep statement
        if time == '1':  # If there is only one minute left
            message = time + ' minute until pound opens! '
        else:  # If there is more than 1 minute left
            message = time + ' minutes until pound opens! '
        for j in range(len(user_ids)):  # For each Discord user
            message += '<@' + user_ids[j] + '> '  # Message format for mentioning users | <@USER_ID>
        await client.send_message(client.get_channel(channel_ids[i]), content=message)  # Send message to Discord channel with mention message


async def minute_check(time):  # Function to check if any user has Auto Remind setup at 'time'
    global autoremind_hash, autoremind_times
    time = str(time)
    new_hash = hashlib.md5(open('autoremind.txt').read().encode()).hexdigest()  # MD5 hash of autoremind.txt
    if autoremind_hash != new_hash:  # If file has been modified since last check
        autoremind_hash = new_hash
        cut_statement = 'cut -f4 -d\' \' autoremind.txt | sort -u'  # Grab all unique reminding times from autoremind.txt
        autoremind_times = subprocess.Popen(cut_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run cut statement
    else:
    if time in autoremind_times:  # If someone has a Auto Remind set at current 'time'
        await compose_message(time)  # Run compose message
    else:


async def pound_countdown():  # Background task to countdown to when the pound opens
    global cooldown  # Use cooldown from global scope
    await client.wait_until_ready()  # Wait until client has loaded before starting background task
    while not client.is_closed:  # While client is still running
        if not cooldown:  # If command is not on cooldown
            pound_logger.info('Command not on cooldown.')
            data = await get_web_data('', 'pound')  # Get pound data
            pound_logger.info('Pound web data received.')
            if data[0]:  # If pound data is valid and contains content
                text = data[1].xpath('//h2/text()')  # List all texts with H2 element
                try:  # Try getting pound opening text
                    text = text[1]  # Grab the pound opening time text
                    value = [int(s) for s in text.split() if s.isdigit()]  # Extract the numbers in the text
                    if len(value) == 1:  # If there is only one number
                        value = value[0]
                        if 'hour' in text:  # If hour in pound opening time
                            if value == 1:  # If there is one hour left
                                cooldown = True
                                value = 60  # Start countdown from 60 minutes
                                sleep_amount = 0
                            else:  # If there is more than one hour
                                sleep_amount = (value - 2) * 3600  # -1 hour and convert into seconds
                        elif 'minute' in text:  # If minute in pound opening time
                            sleep_amount = 0
                            cooldown = True
                        elif 'second' in text:  # If second in pound opening time
                            pass
                    elif len(value) == 2:  # If there are two numbers
                        if 'hour' and 'minute' in text:
                            sleep_amount = value[1] * 60  # Get the minutes and convert to seconds
                            value = 60
                            text = 'minute'
                            cooldown = True
                        elif 'minute' and 'second' in text:
                            pass
                    elif len(value) == 0:  # If there are no times i.e. Pound recently closed or not opening anytime soon
                        sleep_amount = 3600  # 1 hour
                except IndexError:  # Pound is currently open
                    sleep_amount = 3600  # 1 hour
            else:  # If pound data isn't valid
                sleep_amount = 11400  # 3 hours 10 minutes
        else:  # If command is on cooldown
            if 'hour' in text:  # If hour in text
                if value != 0:  # If minutes left is not zero
                    await minute_check(value)  # Run minute check
                    value -= 1  # Remove one minute
                    sleep_amount = 60  # 1 minute
                else:  # If time ran out (i.e. Pound is now open)
                    cooldown = False
                    sleep_amount = 10800  # 3 hours
            elif 'minute' and 'second' in text:  # If minute and second in text
                pound_logger.info('Minute and second in text')
                sleep_amount = value[1]
                value = 1
            elif 'minute' in text:  # If minute in text
                if value != 0:  # If minutes left is not zero
                    await minute_check(value)  # Run minute check
                    value -= 1  #  Remove one minute
                    sleep_amount = 60  # 1 minute
                else:  # If time ran out (i.e. Pound is now open)
                    cooldown = False
                    sleep_amount = 10800  # 3 hours
            elif 'second' in text:  # If second in text
                pass
        await asyncio.sleep(sleep_amount)  # Sleep for sleep amount

client.loop.create_task(pound_countdown())  # Run 'pound_countdown' background task
client.run(token)  # Start bot
