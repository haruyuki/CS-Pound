import asyncio

from chickensmoothie import get_pound_time

loop = asyncio.get_event_loop()


def test_results():
    data = loop.run_until_complete(get_pound_time())
    assert isinstance(data, str)
