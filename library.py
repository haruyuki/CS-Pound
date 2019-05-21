import asyncio
from collections import Counter
import re
import zlib

import cv2
import motor.motor_asyncio as amotor
from sklearn.cluster import KMeans
import uvloop

from constants import Constants, Variables

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client[Constants.database_name]


# -------------------- FUNCTIONS --------------------
def crc(file):
    prev = 0
    for line in open(file, 'rb'):
        prev = zlib.crc32(line, prev)
    return '%X' % (prev & 0xFFFFFFFF)


def parse_time(timestr):  # A function to parse short time formats (1d, 2h, 3m, 4s) into seconds
    timestr = timestr.lower()
    times = re.findall(r'(\d{1,8}[smhd]?)', timestr)
    total = 0
    for time in times:
        if time.isdigit():
            time += 'm'
        total += int(time[:-1]) * seconds_per_unit[time[-1]]
    return total


def formatter(day, hour, minute, second):  # Pretty format time layout given days, hours, minutes and seconds
    def pluralise(string, value, and_placement=''):  # Correctly prefix or suffix ',' or 'and' placements
        if value == 0:  # If given time has no value
            return ''
        else:  # If given time has value
            return f'{" and " if and_placement == "pre" else ""}{value} {string}{"s" if value > 1 else ""}{" and " if and_placement == "suf" else ""}{", " if and_placement == "com" else ""}'
            # If 'and_placement' is set to prefix add 'and' otherwise leave blank
            # The value of the time
            # The type of time (day, hour, minute, second)
            # If value is larger than 1 then pluralise the time
            # If 'and_placement' is set to suffix add 'and' otherwise add a ',' instead if 'and_placement' is set to comma otherwise leave blank

    suffix = False
    comma = False
    if day != 0:  # If there are days
        if hour == 0 and minute == 0 and second == 0:
            pass
        elif hour == 0 and minute == 0:  # If there are no hours or minutes
            suffix = True
        elif hour == 0 and second == 0:  # If there are no hours or seconds
            suffix = True
        elif minute == 0 and second == 0:  # If there are no minutes or seconds
            suffix = True
        elif hour != 0 and minute != 0 and second != 0:  # If there are hours and minutes and seconds
            comma = True
        elif hour != 0 and minute == 0:  # If there are hours but no minutes
            comma = True
        elif hour != 0 and second == 0:  # If there are hours but no seconds
            comma = True
        elif minute != 0 and hour == 0:  # If there are minutes but no hours
            comma = True

    if suffix:
        day_section = pluralise('day', day, 'suf')  # Pluralise the day section with a suffixed 'and' placement
    elif comma:
        day_section = pluralise('day', day, 'com')  # Pluralise the day section with a suffixed ',' placement
    else:
        day_section = pluralise('day', day, '')  # Pluralise the day section with no placements

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
    return f'{day_section}{hour_section}{minute_section}{second_section}'  # Return the formatted text


def resolver(seconds):  # Pretty format time given seconds
    seconds = int(seconds)
    day, hour = divmod(seconds, 86400)
    hour, minute = divmod(hour, 3600)
    minute, second = divmod(minute, 60)

    formatted_string = formatter(day, hour, minute, second)
    return formatted_string


def get_dominant_colour(image):  # Get the RGB of the dominant colour in an image.
    # Slightly modified from https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/
    image = cv2.resize(image, (64, 64), interpolation=cv2.INTER_CUBIC)  # Resize image
    image = image.reshape((image.shape[0] * image.shape[1], 3))  # Reshape image a list of pixels
    clt = KMeans(n_clusters=3)
    labels = clt.fit_predict(image)  # Cluster and assign labels to pixels
    label_counts = Counter(labels)  # Count labels to find most popular
    dominant_colour = clt.cluster_centers_[label_counts.most_common(1)[0][0]]  # Subset out most popular centroid
    dominant_colour = [int(colour) for colour in dominant_colour]
    return list(dominant_colour)


async def update_autoremind_times():
    Variables.autoremind_times = set()
    autoremind_collection = database[Constants.autoremind_collection_name]
    cursor = autoremind_collection.find({})
    for document in await cursor.to_list(length=Constants.autoremind_fetch_limit):
        Variables.autoremind_times.add(document['remind_time'])
    return Variables.autoremind_times


async def get_autoremind_documents(time):  # Get documents of users with specified Auto Remind time
    documents = []
    autoremind_collection = database[Constants.autoremind_collection_name]
    cursor = autoremind_collection.find({'remind_time': time})
    for document in await cursor.to_list(length=Constants.autoremind_fetch_limit):
        documents.append(document)

    if documents:
        return documents
    else:
        return None


async def get_sending_channels(time):
    channel_ids = set()
    documents = await get_autoremind_documents(time)
    if documents is not None:
        for document in documents:
            channel_ids.add(int(document['channel_id']))
    return channel_ids


async def prepare_message(channel_id, time, pound_type):
    message = f'{time} minute{"" if time == 1 else "s"} until {pound_type} opens!'
    documents = await get_autoremind_documents(time)

    if documents is not None:
        for document in documents:
            if int(document['channel_id']) == channel_id:
                message += f' <@{document["user_id"]}>'
        return message
    else:
        return None


def calculate_sleep_amount(seconds):
    send_msg = False  # Assume no message needs to be sent
    sleep_amount = 0
    if Variables.cooldown:  # If command on cooldown
        if 0 < seconds <= 3600:  # If less than an hour remains
            send_msg = True
            seconds -= 60
            sleep_amount = 60  # Sleep for 1 minute
        else:  # If no time remains
            Variables.cooldown = False  # Put command off cooldown
            sleep_amount = 3600  # Sleep for 1 hour
    else:  # If command not on cooldown
        if seconds <= 0 or seconds >= 36000:  # If no times (i.e. Pound currently open or not opening anytime soon) or 10 hours
            sleep_amount = 3600  # Sleep for 1 hour
        elif seconds >= 7200:  # If over 2 hours remain
            sleep_amount = seconds - 7200  # Sleep until 2 hours remain
        elif seconds >= 3600:  # If over 1 hour but less than 2 hours remain
            sleep_amount = seconds - 3600  # Sleep until 1 hour remains
            Variables.cooldown = True  # Put command on cooldown
            seconds = 3600  # Set countdown to begin exactly at 1 hour
        elif seconds < 3600:  # If less than 1 hour remaining
            Variables.cooldown = True  # Put command on cooldown

    return seconds, sleep_amount, send_msg  # Return seconds remaining, sleep amount, whether sending message is needed
