import asyncio

import lxml.html

from chickensmoothie import _get_web_data

loop = asyncio.get_event_loop()


def test_results():
    assert loop.run_until_complete(_get_web_data('http://static.chickensmoothie.com/archive/34&petid=22.jpg')) is False  # Test invalid pet link

    data = loop.run_until_complete(_get_web_data('https://www.chickensmoothie.com/viewpet.php?id=277461516'))
    assert data[0] is True  # Test data is valid
    assert isinstance(data[1], lxml.html.HtmlElement)  # DOM is an HtmlElement
    assert isinstance(data[2], str)  # The connection HTML is string
