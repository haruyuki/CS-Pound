import re

import motor.motor_asyncio as amotor
from osuapi import OsuApi, AHConnector, enums

from constants import Constants

mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client[Constants.database_name]


async def get_user(user, mode):
    osu_collection = database[Constants.osu_collection_name]

    if isinstance(user, int):
        cursor = osu_collection.find({'user_id': str(user)})
        document = await cursor.to_list(length=1)
        try:
            document = document[0]
            user = document['osu_user']
        except IndexError:
            return None

    regex = re.compile(
        r'^(?:http)s?://osu\.ppy\.sh/users/')  # Regex to check if a link is provided

    if user.isdigit():  # If user provided an ID
        user = int(user)
    elif re.match(regex, user) is not None:  # If user provided an link
        link_split = user.split('/')
        user_id = [i for i in link_split if i.isdigit()]  # Get the user ID
        user = int(user_id[0])  # Convert ID into integer
    elif user.isalpha():  # If user provided a username
        pass

    if mode == 'taiko':  # If taiko mode selected
        gamemode = enums.OsuMode.taiko
    elif mode == 'ctb' or mode == 'catch' or mode == 'fruits':  # If catch the beat mode selected
        gamemode = enums.OsuMode.ctb
    elif mode == 'mania':  # If mania mode selected
        gamemode = enums.OsuMode.mania
    else:  # Set default gamemode
        gamemode = enums.OsuMode.osu

    api = OsuApi(Constants.osu_key, connector=AHConnector())  # Connect to osu! API
    result = await api.get_user(user, mode=gamemode)
    try:
        user_data = result[0]
    except IndexError:
        user_data = None

    return user_data
