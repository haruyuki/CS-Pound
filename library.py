from collections import Counter
import re

import asyncio
import cv2
import motor.motor_asyncio as amotor
from sklearn.cluster import KMeans

from chickensmoothie import _get_web_data
from constants import Constants

autoremind_times = []
cooldown = False
mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_connection_string)
database = mongo_client['cs_pound']
collection = database['test']


# -------------------- FUNCTIONS --------------------
def parse_short_time(time):
    timestr = time.lower()
    if not re.findall('\\d{1,8}[smhd]', timestr):
        return -1
    multiplier = 1
    for i in range(len(timestr)):
        if timestr[i] == 'd':
            multiplier *= 86400
        elif timestr[i] == 'h':
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


def get_dominant_colour(image):  # Get the RGB of the dominant colour in an image.
    # Slightly modified from https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/
    image = cv2.resize(image, (25, 25), interpolation=cv2.INTER_AREA)  # Resize image
    image = image.reshape((image.shape[0] * image.shape[1], 3))  # Reshape image a list of pixels
    clt = KMeans(n_clusters=4)
    labels = clt.fit_predict(image)  # Cluster and assign labels to pixels
    label_counts = Counter(labels)  # Count labels to find most popular
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]  # Subset out most popular centroid
    return list(dominant_color)


async def mongodb_query(query):
    cursor = collection.find(query)
    results = await cursor.to_list(length=1000)
    return results


async def compose_message(bot, time):  # Function to compose and send mention messages to channels
    channel_ids = set()  # Create a set to prevent duplicate channel ID's
    results = await mongodb_query({'remind_time': time})  # Query the collection for documents with an Auto Remind time of 'time'
    for i in range(len(results)):
        channel_ids.add(int(results[i]['channel_id']))
    channel_ids = list(channel_ids)
    print(f'Channel IDs: {channel_ids}')

    for channel in range(len(channel_ids)):  # For each Discord channel ID
        results = await mongodb_query({'channel_id': str(channel_ids[channel]), 'remind_time': time})
        user_ids = []
        for i in range(len(results)):
            user_ids.append(int(results[i]['_id']))
        print(f'User IDS: {user_ids}')

        # grep_statement = 'grep \'[0-9]*\\s' + str(channel_ids[channel]) + '\\s[0-9]*\\s' + time + '\' autoremind.txt | cut -f3 -d\' \''  # Grab all unique Discord user ID's with that channel ID
        # user_ids = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run grep statement
        if time == 1:  # If there is only one minute left
            message = f'{time} minute until pound opens! '
        else:  # If there is more than 1 minute left
            message = f'{time} minutes until pound opens! '
        for j in range(len(user_ids)):  # For each Discord user
            message += f'<@{user_ids[j]}> '  # Message format for mentioning users | <@USER_ID>
        try:
            sending_channel = bot.get_channel(channel_ids[channel])
            print(f'Channel is {channel}')
            await sending_channel.send(message)  # Send message to Discord channel with mention message
            print(f'Message sent')
        except AttributeError:
            print('Some error appeared')
            pass


async def minute_check(bot, time):  # Function to check if any user has Auto Remind setup at 'time'
    global autoremind_times
    autoremind_times = set()
    results = await mongodb_query({})
    print(f'SHOULD BE SINGLE RESULT HERE: {results}')
    for i in range(len(results)):
        autoremind_times.add(results[i]['remind_time'])
    print(f'Auto Remind times: {autoremind_times}')
    if time in autoremind_times:  # If someone has a Auto Remind set at current 'time'
        await compose_message(bot, time)  # Run compose message


async def pound_countdown(bot):  # Background task to countdown to when the pound opens
    global cooldown
    print('Started pound countdown function')
    await bot.wait_until_ready()  # Wait until bot has loaded before starting background task
    value = 0
    text = ''
    print('Bot is ready')
    await minute_check(bot, 1)
    while not bot.is_closed():  # While bot is still running
        sleep_amount = 0
        print('Bot is still running')
        if not cooldown:  # If command is not on cooldown
            print('Command not on cooldown')
            data = await _get_web_data('https://www.chickensmoothie.com/pound.php')  # Get pound data
            print('Received web data')
            if data[0]:  # If pound data is valid and contains content
                print('Data was sucessful')
                text = data[1].xpath('//h2/text()')  # List all texts with H2 element
                print(f'Texts with h2 element: {text}')
                try:  # Try getting pound opening text
                    print('Trying to get pound text')
                    text = text[1]  # Grab the pound opening time text
                    print(f'Received text: {text}')
                    value = [int(s) for s in text.split() if s.isdigit()]  # Extract the numbers in the text
                    print(f'Values in text: {value}')
                    if len(value) == 1:  # If there is only one number
                        value = value[0]
                        if 'hour' in text:  # If hour in pound opening time
                            print('Hour in text')
                            if value == 1:  # If there is one hour left
                                cooldown = True
                                value = 60  # Start countdown from 60 minutes
                                sleep_amount = 0
                            else:  # If there is more than one hour
                                sleep_amount = (value - 2) * 3600  # -1 hour and convert into seconds
                        elif 'minute' in text:  # If minute in pound opening time
                            print('Minute in text')
                            sleep_amount = 0
                            cooldown = True
                        elif 'second' in text:  # If second in pound opening time
                            pass
                    elif len(value) == 2:  # If there are two numbers
                        if 'hour' and 'minute' in text:
                            print('Hour and minute in text')
                            sleep_amount = value[1] * 60  # Get the minutes and convert to seconds
                            value = 60
                            text = 'minute'
                            cooldown = True
                        elif 'minute' and 'second' in text:
                            print('Minute and second in text')
                    elif len(value) == 0:  # If there are no times i.e. Pound recently closed or not opening anytime soon
                        print('No time')
                        sleep_amount = 3600  # 1 hour
                except IndexError:  # Pound is currently open
                    print('Pound open')
                    sleep_amount = 3600  # 1 hour
            else:  # If pound data isn't valid
                sleep_amount = 11400  # 3 hours 10 minutes
        else:  # If command is on cooldown
            if 'hour' in text:  # If hour in text
                if value != 0:  # If minutes left is not zero
                    await minute_check(bot, value)  # Run minute check
                    value -= 1  # Remove one minute
                    sleep_amount = 60  # 1 minute
                else:  # If time ran out (i.e. Pound is now open)
                    cooldown = False
                    sleep_amount = 10800  # 3 hours
            elif 'minute' and 'second' in text:  # If minute and second in text
                sleep_amount = value[1]
                value = 1
            elif 'minute' in text:  # If minute in text
                if value > 0:  # If minutes left is not zero
                    await minute_check(bot, value)  # Run minute check
                    value -= 1  # Remove one minute
                    sleep_amount = 60  # 1 minute
                else:  # If time ran out (i.e. Pound is now open)
                    cooldown = False
                    sleep_amount = 10800  # 3 hours
            elif 'second' in text:  # If second in text
                pass
            else:
                print(f'Cooldown but no value')
                sleep_amount = 10800  # 3 hours
        await asyncio.sleep(sleep_amount)  # Sleep for sleep amount
        print(f'Slept for: {sleep_amount}')
        print(f'Command is on cooldown: {cooldown}')
