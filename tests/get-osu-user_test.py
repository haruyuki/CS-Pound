import asyncio

from osu import get_user

loop = asyncio.get_event_loop()


class TestClass:
    def test_get_standard_data(self):
        data = loop.run_until_complete(get_user('Haruyuki Arita', 'osu'))
        assert data is not None
        assert data.user_id == 7109858
        assert data.username == 'Haruyuki Arita'

    def test_get_data_by_id(self):
        data = loop.run_until_complete(get_user('7109858', 'osu'))
        assert data is not None
        assert data.user_id == 7109858
        assert data.username == 'Haruyuki Arita'

    def test_get_data_by_link(self):
        data = loop.run_until_complete(get_user('http://osu.ppy.sh/users/7109858', 'osu'))
        assert data is not None
        assert data.user_id == 7109858
        assert data.username == 'Haruyuki Arita'

    def test_get_taiko_data(self):
        data = loop.run_until_complete(get_user('Haruyuki Arita', 'taiko'))
        assert data is not None
        assert data.user_id == 7109858
        assert data.username == 'Haruyuki Arita'

    def test_get_catch_data(self):
        data = loop.run_until_complete(get_user('Haruyuki Arita', 'catch'))
        assert data is not None
        assert data.user_id == 7109858
        assert data.username == 'Haruyuki Arita'

    def test_get_mania_data(self):
        data = loop.run_until_complete(get_user('Haruyuki Arita', 'mania'))
        assert data is not None
        assert data.user_id == 7109858
        assert data.username == 'Haruyuki Arita'

    def test_db_linked_user(self):
        data = loop.run_until_complete(get_user(277398425044123649, 'osu'))
        assert data is not None
        assert data.user_id == 7109858
        assert data.username == 'Haruyuki Arita'

    def test_db_unlinked_user(self):
        data = loop.run_until_complete(get_user(1, 'osu'))
        assert data is None

    def test_invalid_user(self):
        data = loop.run_until_complete(get_user('NonExistentUserName123', 'osu'))
        assert data is None
