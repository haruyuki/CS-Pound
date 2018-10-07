import asyncio

from chickensmoothie import pet

loop = asyncio.get_event_loop()


def test_results():
    assert loop.run_until_complete(pet('http://static.chickensmoothie.com/archive/34&petid=22.jpg')) is None  # Test invalid pet link

    data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=149733321'))

    assert data['pps'] is True
    assert 'https://static.chickensmoothie.com/pic.php?k=E3ED84674D3923A39821A8915A3E1F40' in data['image_link']  # T hex colour background parameter changes depending on site events
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
