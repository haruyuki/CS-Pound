import asyncio

from chickensmoothie import pet

loop = asyncio.get_event_loop()


class TestClass:
    def test_invalid_link(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php'))
        assert data is None

    def test_pps_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=277461516'))

        assert data['pps'] is True
        assert 'https://static.chickensmoothie.com/pic.php?k=1D52FCF41D529B10FF7A82D698E38610' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 277461516
        assert data['name'] == ''
        assert data['adopted'] == '2018-10-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == ''
        assert data['given_link'] == ''

    def test_named_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275517241'))

        assert data['pps'] is False
        assert 'https://static.chickensmoothie.com/pic.php?k=D4A1B949640F125E0DE55BD4B5B6394E' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 275517241
        assert data['name'] == ''
        assert data['adopted'] == '2018-09-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == ''
        assert data['given_link'] == ''

    def test_given_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=21793613'))

        assert data['pps'] is False
        assert 'https://static.chickensmoothie.com/pic.php?k=CAD0977E70396057F7A7A78771A16FEC' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 21793613
        assert data['name'] == ''
        assert data['adopted'] == '2010-10-25'
        assert data['age'] > 0   # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_pps_named_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=271278924'))

        assert data['pps'] is True
        assert 'https://static.chickensmoothie.com/pic.php?k=1C1C5F13A70E00B81A17B90FF5EEB441' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 271278924
        assert data['name'] == 'Kokoro'
        assert data['adopted'] == '2018-07-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == ''
        assert data['given_link'] == ''

    def test_pps_given_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=274148542'))

        assert data['pps'] is True
        assert 'https://static.chickensmoothie.com/pic.php?k=29C901408AB3E776D839496CE6729A95' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 274148542
        assert data['name'] == ''
        assert data['adopted'] == '2018-08-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'CS Store'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=35343' in data['given_link']  # A unique session ID is appended to end of URL

    def test_named_given_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=5319635'))

        assert data['pps'] is False
        assert 'https://static.chickensmoothie.com/pic.php?k=60570E6DA157BA2523CBA6B2E9F0AC73' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 5319635
        assert data['name'] == 'Kip'
        assert data['adopted'] == '2009-11-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_pps_named_given_pet(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=149733321'))

        assert data['pps'] is True
        assert 'https://static.chickensmoothie.com/pic.php?k=E3ED84674D3923A39821A8915A3E1F40' in data['image']  # The hex colour background parameter changes depending on site events
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 149733321
        assert data['name'] == 'Likulau'
        assert data['adopted'] == '2014-12-08'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_pps_pet_with_items(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275516238'))

        assert data['pps'] is True
        assert data['image'] == 'https://www.chickensmoothie.com/pet/275516238&trans=1.jpg'
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 275516238
        assert data['name'] == ''
        assert data['adopted'] == '2018-09-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == ''
        assert data['given_link'] == ''

    def test_named_pet_with_items(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275516239'))

        assert data['pps'] is False
        assert data['image'] == 'https://www.chickensmoothie.com/pet/275516239&trans=1.jpg'
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 275516239
        assert data['name'] == 'Yuuya'
        assert data['adopted'] == '2018-09-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == ''
        assert data['given_link'] == ''

    def test_given_pet_with_items(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=36239046'))

        assert data['pps'] is False
        assert data['image']  == 'https://www.chickensmoothie.com/pet/36239046&trans=1.jpg'
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 36239046
        assert data['name'] == ''
        assert data['adopted'] == '2011-05-04'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_pps_named_pet_with_items(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275516244'))

        assert data['pps'] is True
        assert data['image'] == 'https://www.chickensmoothie.com/pet/275516244&trans=1.jpg'
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 275516244
        assert data['name'] == 'Pyon'
        assert data['adopted'] == '2018-09-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == ''
        assert data['given_link'] == ''

    def test_pps_given_pet_with_items(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=114662526'))

        assert data['pps'] is True
        assert data['image'] == 'https://www.chickensmoothie.com/pet/114662526&trans=1.jpg'
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 114662526
        assert data['name'] == ''
        assert data['adopted'] == '2013-12-15'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_named_given_pet_with_items(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=7945242'))

        assert data['pps'] is False
        assert data['image'] == 'https://www.chickensmoothie.com/pet/7945242&trans=1.jpg'
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 7945242
        assert data['name'] == 'Rocket'
        assert data['adopted'] == '2010-01-01'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL

    def test_pps_named_given_pet_with_items(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=94477107'))

        assert data['pps'] is True
        assert data['image'] == 'https://www.chickensmoothie.com/pet/94477107&trans=1.jpg'
        assert data['owner'] == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in data['owner_link']  # A unique session ID is appended to end of URL
        assert data['id'] == 94477107
        assert data['name'] == 'Chi'
        assert data['adopted'] == '2013-03-31'
        assert data['age'] > 0  # As age constantly increases
        assert data['growth'] == 'Full-grown'
        assert isinstance(data['rarity'], str)  # As rarity can change over time
        assert data['given'] == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in data['given_link']  # A unique session ID is appended to end of URL
