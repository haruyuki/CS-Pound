import asyncio

from chickensmoothie import get_announcements

loop = asyncio.get_event_loop()


def test_results():
    data = loop.run_until_complete(get_announcements())
    assert isinstance(data, list)
