import asyncio
import motor.motor_asyncio as amotor

from constants import Constants
from library import update_autoremind_times

loop = asyncio.get_event_loop()


def test_results():
    mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
    database = mongo_client[Constants.database_name]
    collection = database[Constants.autoremind_collection_name]

    objectid = loop.run_until_complete(collection.insert_one({'server_id': 'Travis CI Py.test', 'channel_id': 'Testing get_autoremind_documents function', 'user_id': 'Haruyuki', 'remind_time': 0}))
    times = loop.run_until_complete(update_autoremind_times())
    assert 0 in times

    loop.run_until_complete(collection.delete_one({'_id': objectid.inserted_id}))
    times = loop.run_until_complete(update_autoremind_times())
    assert 0 not in times
