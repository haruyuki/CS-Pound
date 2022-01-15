import asyncio
import subprocess

import motor.motor_asyncio as amotor

from constants import Constants
from library import update_autoremind_times

loop = asyncio.get_event_loop()
mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client[Constants.database_name]
collection = database[Constants.autoremind_collection_name]

update_task = loop.create_task(update_autoremind_times())

def test_results():
    loop.run_until_complete(collection.insert_one({'server_id': 'Travis CI Py.test', 'channel_id': 'Testing update_autoremind_times function', 'user_id': 'Haruyuki', 'remind_time': 0}))
    assert 0 in loop.run_until_complete(update_task)

    loop.run_until_complete(collection.delete_one({'_id': objectid.inserted_id}))
    assert 0 not in loop.run_until_complete(update_task)
