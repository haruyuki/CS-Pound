from library import parse_short_time


def test_results():
    assert parse_short_time('1s') == 1
    assert parse_short_time('2s') == 2
    assert parse_short_time('1m') == 60
    assert parse_short_time('2m') == 120
    assert parse_short_time('1h') == 3600
    assert parse_short_time('2h') == 7200
    assert parse_short_time('1d') == 86400
    assert parse_short_time('2d') == 172800

    assert parse_short_time('60s') == 60
    assert parse_short_time('60m') == 3600
    assert parse_short_time('24h') == 86400
    assert parse_short_time('30d') == 2592000
