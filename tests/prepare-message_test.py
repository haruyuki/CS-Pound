import asyncio

import motor.motor_asyncio as amotor

from constants import Constants
from library import prepare_message

loop = asyncio.get_event_loop()

mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client[Constants.database_name]
collection = database[Constants.autoremind_collection_name]


class TestClass:
    def test_pound_message(self):
        objectid = loop.run_until_complete(
            collection.insert_one(
                {
                    "server_id": "Travis CI Py.test prepare-message",
                    "channel_id": "1234567890",
                    "user_id": "Haruyuki",
                    "remind_time": -1,
                }
            )
        )
        message = loop.run_until_complete(prepare_message(1234567890, -1, "Pound"))

        assert message == ["-1 minutes until Pound opens! <@Haruyuki>"]

        loop.run_until_complete(collection.delete_one({"_id": objectid.inserted_id}))
        message = loop.run_until_complete(prepare_message("1234567890", -1, "Pound"))
        assert message is None

    def test_lost_and_found_message(self):
        objectid = loop.run_until_complete(
            collection.insert_one(
                {
                    "server_id": "Travis CI Py.test prepare-message",
                    "channel_id": "1234567890",
                    "user_id": "Haruyuki",
                    "remind_time": -1,
                }
            )
        )
        message = loop.run_until_complete(
            prepare_message(1234567890, -1, "Lost & Found")
        )

        assert message == ["-1 minutes until Lost & Found opens! <@Haruyuki>"]

        loop.run_until_complete(collection.delete_one({"_id": objectid.inserted_id}))
        message = loop.run_until_complete(
            prepare_message("1234567890", -1, "Lost & Found")
        )
        assert message is None
