import lxml.html

from library import _get_web_data


def test_results():
    assert _get_web_data('http://static.chickensmoothie.com/archive/34&petid=22.jpg') is False  # Test invalid pet link

    data = _get_web_data('https://www.chickensmoothie.com/viewpet.php?id=85468442')
    assert data[0] is True  # Test data is valid
    assert isinstance(data[1], lxml.html.HtmlElement)  # DOM is an HtmlElement
    assert isinstance(data[2], str)  # The connection HTML is string
