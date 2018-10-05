import asyncio
import motor.motor_asyncio as amotor

from constants import Constants
from library import get_autoremind_documents

loop = asyncio.get_event_loop()


def test_results():
    mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
    database = mongo_client[Constants.database_name]
    collection = database[Constants.autoremind_collection_name]

    objectid = loop.run_until_complete(collection.insert_one({'server_id': 'Travis CI Py.test', 'channel_id': 'Testing get_autoremind_documents function', 'user_id': 'Haruyuki', 'remind_time': 0}))
    document = loop.run_until_complete(get_autoremind_documents(0))
    assert len(document) == 1
    document = document[0]
    assert document['server_id'] == 'Travis CI Py.test'
    assert document['channel_id'] == 'Testing get_autoremind_documents function'
    assert document['user_id'] == 'Haruyuki'
    assert document['remind_time'] == 0

    loop.run_until_complete(collection.delete_one({'_id': objectid.inserted_id}))
    document = loop.run_until_complete(get_autoremind_documents(0))
    assert document == []
