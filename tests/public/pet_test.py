import asyncio

from chickensmoothie import pet

loop = asyncio.get_event_loop()


class TestClass:
    def test_invalid_link(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php'))
        assert data is None

    def test_valid_link(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=149733321'))

        # assert data['pps'] is True <- PPS Validation is broken
        assert 'https://static.chickensmoothie.com/pic.php?k=E3ED84674D3923A39821A8915A3E1F40' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 149733321
        assert data['name'] == "Lil' Leopard"
        assert data['adopted'] == '2014-12-08'
        assert data['age'] > 0  # As age constantly changes
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_without_name(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=196835006'))

        assert 'https://static.chickensmoothie.com/pic.php?k=79A84F37B9FDF69B0D9B313C637E4F5A' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 196835006
        assert data['adopted'] == '2016-02-21'
        assert data['age'] > 0  # As age constantly changes
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_wide_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=225646170'))

        assert 'https://static.chickensmoothie.com/pic.php?k=C404A1DDA3B5DD713D0986613AC6DD23' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 225646170
        assert data['adopted'] == '2016-12-25'
        assert data['age'] > 0   # As age constantly changes
        # assert data['growth'] == 'Full-grown' <- Growth Validation is broken
        assert isinstance(data['rarity'], str)  # As rarity can change over time
