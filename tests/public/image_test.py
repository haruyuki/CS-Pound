import io

import asyncio

from chickensmoothie import image

loop = asyncio.get_event_loop()


class TestClass:
    def test_invalid_link(self):
        data = loop.run_until_complete(image('https://www.chickensmoothie.com/viewpet.php'))
        assert data is None

    def test_valid_link(self):
        data = loop.run_until_complete(image('https://www.chickensmoothie.com/viewpet.php?id=277461516'))
        assert isinstance(data, io.BytesIO)

    def test_pet_with_items(self):
        data = loop.run_until_complete(image('https://www.chickensmoothie.com/viewpet.php?id=275516239'))
        assert isinstance(data, io.BytesIO)
