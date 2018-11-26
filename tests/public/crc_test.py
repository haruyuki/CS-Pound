from library import crc


def test_results():
    assert crc('tests/public/assets/crc.json') == '9A2987F9'
