import asyncio
from collections import Counter
import re
import zlib

import motor.motor_asyncio as amotor
import uvloop

from constants import Constants, Variables

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client[Constants.database_name]


# -------------------- FUNCTIONS --------------------
def parse_time(
    time_string,
):  # A function to parse short time formats (1d, 2h, 3m, 4s) into seconds
    time_string = time_string.lower()
    times = re.findall(r"(\d{1,8}[smhd]?)", time_string)
    total = 0
    for time in times:
        if time.isdigit():
            time += "m"
        total += int(time[:-1]) * seconds_per_unit[time[-1]]
    return total


def formatter(
    day, hour, minute, second
):  # Pretty format time layout given days, hours, minutes and seconds
    def pluralise(
        string, value, and_placement=""
    ):  # Correctly prefix or suffix ',' or 'and' placements
        if value == 0:  # If given time has no value
            return ""
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
        elif (
            hour != 0 and minute != 0 and second != 0
        ):  # If there are hours and minutes and seconds
            comma = True
        elif hour != 0 and minute == 0:  # If there are hours but no minutes
            comma = True
        elif hour != 0 and second == 0:  # If there are hours but no seconds
            comma = True
        elif minute != 0 and hour == 0:  # If there are minutes but no hours
            comma = True

    if suffix:
        day_section = pluralise(
            "day", day, "suf"
        )  # Pluralise the day section with a suffixed 'and' placement
    elif comma:
        day_section = pluralise(
            "day", day, "com"
        )  # Pluralise the day section with a suffixed ',' placement
    else:
        day_section = pluralise(
            "day", day, ""
        )  # Pluralise the day section with no placements

    if minute == 0:  # If there are no minutes
        hour_section = pluralise("hour", hour)  # Pluralise the hour section
    elif minute != 0 and second == 0:  # If there are minute(s) but no seconds
        hour_section = pluralise(
            "hour", hour, "suf"
        )  # Pluralise the hour section with a suffixed 'and' placement
    else:  # If there are minute(s) and second(s)
        hour_section = pluralise(
            "hour", hour, "com"
        )  # Pluralise the hour section with a suffixed ',' placement

    minute_section = pluralise("minute", minute)  # Pluralise the minute section

    if hour != 0 or minute != 0:  # If there are hour(s) or minute(s)
        second_section = pluralise(
            "second", second, "pre"
        )  # Pluralise the second section with a prefixed 'and' placement
    else:  # If there are no hours or minutes
        second_section = pluralise("second", second)  # Pluralise the second section
    return f"{day_section}{hour_section}{minute_section}{second_section}"  # Return the formatted text


def resolver(seconds):  # Pretty format time given seconds
    seconds = int(seconds)
    day, hour = divmod(seconds, 86400)
    hour, minute = divmod(hour, 3600)
    minute, second = divmod(minute, 60)

    formatted_string = formatter(day, hour, minute, second)
    return formatted_string


def multi_replace(string, replacements):
    # Taken from https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
    substrs = sorted(replacements, key=len, reverse=True)
    regexp = re.compile("|".join(map(re.escape, substrs)))
    return regexp.sub(lambda match: replacements[match.group(0)], string)


async def update_autoremind_times():
    Variables.autoremind_times = set()
    autoremind_collection = database[Constants.autoremind_collection_name]
    Variables.autoremind_times = set(
        await autoremind_collection.distinct("remind_time")
    )
    return Variables.autoremind_times


async def get_autoremind_documents(
    time,
):  # Get documents of users with specified Auto Remind time
    documents = []
    autoremind_collection = database[Constants.autoremind_collection_name]
    cursor = autoremind_collection.find({"remind_time": time})
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
            channel_ids.add(int(document["channel_id"]))
    return channel_ids


async def prepare_message(channel_id, time, pound_type):
    message_group = []
    offset = 0
    message = f'{time} minute{"" if time == 1 else "s"} until {pound_type} opens!'
    documents = await get_autoremind_documents(time)
    if documents is not None:
        for document in documents:
            if int(document["channel_id"]) == channel_id:
                message_to_send = message + f' <@{document["user_id"]}>'
                if len(message_to_send) + offset > 2000:
                    message_group.append(message)
                    message = f'{time} minute{"" if time == 1 else "s"} until {pound_type} opens!'
                    offset = 1
                else:
                    offset += 1
                message += f' <@{document["user_id"]}>'
        message_group.append(message)
        return message_group
    else:
        return None


def calculate_sleep_amount(seconds):
    send_msg = False  # Assume no message needs to be sent
    sleep_amount = 0
    if (
        seconds <= 0 or seconds >= 36000
    ):  # If no times (i.e. Pound currently open or not opening anytime soon) or 10 hours
        sleep_amount = 3600  # Sleep for 1 hour
        Variables.cooldown = False
    elif seconds >= 7200:  # If over 2 hours remain
        sleep_amount = seconds - 7200  # Sleep until 2 hours remain
    elif seconds > 3600:  # If over 1 hour but less than 2 hours remain
        sleep_amount = seconds - 3600  # Sleep until 1 hour remains
        Variables.cooldown = True  # Put command on cooldown
        seconds = 3600  # Set countdown to begin exactly at 1 hour
    elif 0 < seconds <= 3600:  # If less than an hour remains
        send_msg = True
        seconds -= 60
        sleep_amount = 60  # Sleep for 1 minute
        Variables.cooldown = True
    else:  # If no time remains
        sleep_amount = 3600  # Sleep for 1 hour
        Variables.cooldown = False

    return (
        seconds,
        sleep_amount,
        send_msg,
    )  # Return seconds remaining, sleep amount, whether sending message is needed, whether to start self timer
