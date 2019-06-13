import asyncio

import lxml.html

from flightrising import _get_web_data

loop = asyncio.get_event_loop()


def test_results():
    data = loop.run_until_complete(_get_web_data('http://flightrising.com/main.php?p=lair&id=430187&tab=dragon&did=52548928'))
    assert data[0] is True  # Test data is valid
    assert isinstance(data[1], lxml.html.HtmlElement)  # DOM is an HtmlElement
