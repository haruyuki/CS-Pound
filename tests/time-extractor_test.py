from library import time_extractor


def test_result():
    assert time_extractor('1s') == (1, 0, 0, 1)
    assert time_extractor('2s') == (2, 0, 0, 2)
    assert time_extractor('1m') == (60, 0, 1, 0)
    assert time_extractor('1m1s') == (61, 0, 1, 1)
    assert time_extractor('1m2s') == (62, 0, 1, 2)
    assert time_extractor('2m') == (120, 0, 2, 0)
    assert time_extractor('2m1s') == (121, 0, 2, 1)
    assert time_extractor('2m2s') == (122, 0, 2, 2)
    assert time_extractor('1h') == (3600, 1, 0, 0)
    assert time_extractor('1h1s') == (3601, 1, 0, 1)
    assert time_extractor('1h2s') == (3602, 1, 0, 2)
    assert time_extractor('1h1m') == (3660, 1, 1, 0)
    assert time_extractor('1h1m1s') == (3661, 1, 1, 1)
    assert time_extractor('1h1m2s') == (3662, 1, 1, 2)
    assert time_extractor('1h2m') == (3720, 1, 2, 0)
    assert time_extractor('1h2m1s') == (3721, 1, 2, 1)
    assert time_extractor('1h2m2s') == (3722, 1, 2, 2)
    assert time_extractor('2h') == (7200, 2, 0, 0)
    assert time_extractor('2h1s') == (7201, 2, 0, 1)
    assert time_extractor('2h2s') == (7202, 2, 0, 2)
    assert time_extractor('2h1m') == (7260, 2, 1, 0)
    assert time_extractor('2h1m1s') == (7261, 2, 1, 1)
    assert time_extractor('2h1m2s') == (7262, 2, 1, 2)
    assert time_extractor('2h2m') == (7320, 2, 2, 0)
    assert time_extractor('2h2m1s') == (7321, 2, 2, 1)
    assert time_extractor('2h2m2s') == (7322, 2, 2, 2)

    assert time_extractor('1') == (0, 0, 0, 0)
    assert time_extractor('2') == (0, 0, 0, 0)
    assert time_extractor('0s') == (0, 0, 0, 0)
    assert time_extractor('0m') == (0, 0, 0, 0)
    assert time_extractor('0h') == (0, 0, 0, 0)
