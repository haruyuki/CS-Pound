import re

import aiohttp
import asyncio
import discord
import lxml.html

prefix = '.'
version = '2.0'


# -------------------- FUNCTIONS --------------------
def parse_short_time(time):
    timestr = time.lower()
    if re.findall('\\d{1,8}[smhd]', timestr) == []:
        return -1
    multiplier = 1
    for i in range(len(timestr)):
        if timestr[i] == 'd':
            multiplier *= 86400
        elif timestr[i]== 'h':
            multiplier *= 3600
        elif timestr[i] == 'm':
            multiplier *= 60
        elif timestr[i] == 's':
            timestr = timestr[:-1]
    return multiplier * int(''.join([x for x in timestr if x.isdigit()]))


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
