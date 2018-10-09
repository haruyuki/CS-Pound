import asyncio

import motor.motor_asyncio as amotor

from constants import Constants
from library import get_sending_channels

loop = asyncio.get_event_loop()


def test_results():
    mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
    database = mongo_client[Constants.database_name]
    collection = database[Constants.autoremind_collection_name]

    objectid = loop.run_until_complete(collection.insert_one({'server_id': 'Travis CI Py.test get_sending_channels', 'channel_id': '1234567890', 'user_id': 'Haruyuki', 'remind_time': 0}))
    channels = loop.run_until_complete(get_sending_channels(0))
    assert len(channels) == 1
    for channel in channels:
        assert channel == 1234567890

    loop.run_until_complete(collection.delete_one({'_id': objectid.inserted_id}))
    document = loop.run_until_complete(get_sending_channels(0))
    assert document == set()
