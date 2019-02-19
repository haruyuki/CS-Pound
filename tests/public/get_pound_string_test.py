import asyncio

from chickensmoothie import get_pound_string

loop = asyncio.get_event_loop()


def test_results():
    data = loop.run_until_complete(get_pound_string())
    assert isinstance(data, tuple)
