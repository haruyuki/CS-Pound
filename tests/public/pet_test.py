import asyncio

from chickensmoothie import pet

loop = asyncio.get_event_loop()


class TestClass:
    def test_invalid_link(self):
        data = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php'))
        assert data is None

    def test_pps_pet(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=277461516'))

        assert pet.__repr__() == "<Pet id=277461516 name='{self.name}'>"
        assert pet_class.pps is True
        assert pet_class.store_pet is False
        assert 'https://static.chickensmoothie.com/pic.php?k=1D52FCF41D529B10FF7A82D698E38610' in pet_class.image_url  # The hex colour background parameter changes depending on site events
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 277461516
        assert pet_class.name is None
        assert pet_class.adoption_date == '2018-10-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name is None
        assert pet_class.given_url is None

    def test_named_pet(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275517241'))

        assert pet_class.pps is False
        assert pet_class.store_pet is False
        assert 'https://static.chickensmoothie.com/pic.php?k=D4A1B949640F125E0DE55BD4B5B6394E' in pet_class.image_url  # The hex colour background parameter changes depending on site events
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 275517241
        assert pet_class.name == 'Telly'
        assert pet_class.adoption_date == '2018-09-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name is None
        assert pet_class.given_url is None

    def test_given_pet(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=21793613'))

        assert pet_class.pps is False
        assert pet_class.store_pet is False
        assert 'https://static.chickensmoothie.com/pic.php?k=CAD0977E70396057F7A7A78771A16FEC' in pet_class.image_url  # The hex colour background parameter changes depending on site events
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 21793613
        assert pet_class.name is None
        assert pet_class.adoption_date == '2010-10-25'
        assert pet_class.age > 0   # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in pet_class.given_url  # A unique session ID is appended to end of URL

    def test_pps_named_pet(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=283255080'))

        assert pet_class.pps is True
        assert pet_class.store_pet is False
        assert 'https://static.chickensmoothie.com/pic.php?k=179D56B1EFF8F3F859C25B8268B51CBB' in pet_class.image_url  # The hex colour background parameter changes depending on site events
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 283255080
        assert pet_class.name == 'Theo'
        assert pet_class.adoption_date == '2018-12-05'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name is None
        assert pet_class.given_url is None

    def test_pps_given_pet(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=274148542'))

        assert pet_class.pps is True
        assert pet_class.store_pet is True
        assert 'https://static.chickensmoothie.com/pic.php?k=36236346D1BBED5C3A10BA6F0C06A700' in pet_class.image_url  # The hex colour background parameter changes depending on site events
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 274148542
        assert pet_class.name is None
        assert pet_class.adoption_date == '2018-08-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'CS Store'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=35343' in pet_class.given_url  # A unique session ID is appended to end of URL

    def test_named_given_pet(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=5319635'))

        assert pet_class.pps is False
        assert pet_class.store_pet is False
        assert 'https://static.chickensmoothie.com/pic.php?k=60570E6DA157BA2523CBA6B2E9F0AC73' in pet_class.image_url  # The hex colour background parameter changes depending on site events
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 5319635
        assert pet_class.name == 'Kip'
        assert pet_class.adoption_date == '2009-11-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in pet_class.given_url  # A unique session ID is appended to end of URL

    def test_pps_named_given_pet(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=149733321'))

        assert pet_class.pps is True
        assert pet_class.store_pet is False
        assert 'https://static.chickensmoothie.com/pic.php?k=E3ED84674D3923A39821A8915A3E1F40' in pet_class.image_url  # The hex colour background parameter changes depending on site events
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 149733321
        assert pet_class.name == 'Likulau'
        assert pet_class.adoption_date == '2014-12-08'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in pet_class.given_url  # A unique session ID is appended to end of URL

    def test_pps_pet_with_items(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275516238'))

        assert pet_class.pps is True
        assert pet_class.store_pet is False
        assert pet_class.image_url == 'https://www.chickensmoothie.com/pet/275516238&trans=1.jpg'
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 275516238
        assert pet_class.name is None
        assert pet_class.adoption_date == '2018-09-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name is None
        assert pet_class.given_url is None

    def test_named_pet_with_items(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275516239'))

        assert pet_class.pps is False
        assert pet_class.store_pet is False
        assert pet_class.image_url == 'https://www.chickensmoothie.com/pet/275516239&trans=1.jpg'
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 275516239
        assert pet_class.name == 'Yuuya'
        assert pet_class.adoption_date == '2018-09-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name is None
        assert pet_class.given_url is None

    def test_given_pet_with_items(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=36239046'))

        assert pet_class.pps is False
        assert pet_class.store_pet is False
        assert pet_class.image_url == 'https://www.chickensmoothie.com/pet/36239046&trans=1.jpg'
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 36239046
        assert pet_class.name is None
        assert pet_class.adoption_date == '2011-05-04'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in pet_class.given_url  # A unique session ID is appended to end of URL

    def test_pps_named_pet_with_items(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=275516244'))

        assert pet_class.pps is True
        assert pet_class.store_pet is False
        assert pet_class.image_url == 'https://www.chickensmoothie.com/pet/275516244&trans=1.jpg'
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 275516244
        assert pet_class.name == 'Pyon'
        assert pet_class.adoption_date == '2018-09-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name is None
        assert pet_class.given_url is None

    def test_pps_given_pet_with_items(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=114662526'))

        assert pet_class.pps is True
        assert pet_class.store_pet is False
        assert pet_class.image_url == 'https://www.chickensmoothie.com/pet/114662526&trans=1.jpg'
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 114662526
        assert pet_class.name is None
        assert pet_class.adoption_date == '2013-12-15'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in pet_class.given_url  # A unique session ID is appended to end of URL

    def test_named_given_pet_with_items(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=7945242'))

        assert pet_class.pps is False
        assert pet_class.store_pet is False
        assert pet_class.image_url == 'https://www.chickensmoothie.com/pet/7945242&trans=1.jpg'
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 7945242
        assert pet_class.name == 'Rocket'
        assert pet_class.adoption_date == '2010-01-01'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in pet_class.given_url  # A unique session ID is appended to end of URL

    def test_pps_named_given_pet_with_items(self):
        pet_class = loop.run_until_complete(pet('https://www.chickensmoothie.com/viewpet.php?id=94477107'))

        assert pet_class.pps is True
        assert pet_class.store_pet is False
        assert pet_class.image_url == 'https://www.chickensmoothie.com/pet/94477107&trans=1.jpg'
        assert pet_class.owner_name == 'haruyuki'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=841634' in pet_class.owner_link  # A unique session ID is appended to end of URL
        assert pet_class.id == 94477107
        assert pet_class.name == 'Chi'
        assert pet_class.adoption_date == '2013-03-31'
        assert pet_class.age > 0  # As age constantly increases
        assert pet_class.growth == 'Full-grown'
        assert isinstance(pet_class.rarity, str)  # As rarity can change over time
        assert pet_class.given_name == 'Pound'
        assert 'https://www.chickensmoothie.com/Forum/memberlist.php?mode=viewprofile&u=2887' in pet_class.given_url  # A unique session ID is appended to end of URL
