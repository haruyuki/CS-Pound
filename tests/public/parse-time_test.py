from library import parse_time


class TestClass:
    def test_one_digit_single_times(self):
        assert parse_time('1s') == 1
        assert parse_time('2s') == 2
        assert parse_time('1m') == 60
        assert parse_time('2m') == 120
        assert parse_time('1h') == 3600
        assert parse_time('2h') == 7200
        assert parse_time('1d') == 86400
        assert parse_time('2d') == 172800

    def test_one_digit_double_times(self):
        assert parse_time('1m1s') == 61
        assert parse_time('1m2s') == 62
        assert parse_time('2m1s') == 121
        assert parse_time('2m2s') == 122
        assert parse_time('1h1s') == 3601
        assert parse_time('1h2s') == 3602
        assert parse_time('1h1m') == 3660
        assert parse_time('1h2m') == 3720
        assert parse_time('2h1s') == 7201
        assert parse_time('2h2s') == 7202
        assert parse_time('2h1m') == 7260
        assert parse_time('2h2m') == 7320
        assert parse_time('1d1s') == 86401
        assert parse_time('1d2s') == 86402
        assert parse_time('1d1m') == 86460
        assert parse_time('1d2m') == 86520
        assert parse_time('1d1h') == 90000
        assert parse_time('1d2h') == 93600
        assert parse_time('2d1s') == 172801
        assert parse_time('2d2s') == 172802
        assert parse_time('2d1m') == 172860
        assert parse_time('2d2m') == 172920
        assert parse_time('2d1h') == 176400
        assert parse_time('2d2h') == 180000

    def test_one_digit_triple_times(self):
        assert parse_time('1h1m1s') == 3661
        assert parse_time('1h1m2s') == 3662
        assert parse_time('1h2m1s') == 3721
        assert parse_time('1h2m2s') == 3722
        assert parse_time('2h1m1s') == 7261
        assert parse_time('2h1m2s') == 7262
        assert parse_time('2h2m1s') == 7321
        assert parse_time('2h2m2s') == 7322
        assert parse_time('1d1m1s') == 86461
        assert parse_time('1d1m2s') == 86462
        assert parse_time('1d2m1s') == 86521
        assert parse_time('1d2m2s') == 86522
        assert parse_time('1d1h1s') == 90001
        assert parse_time('1d1h2s') == 90002
        assert parse_time('1d1h1m') == 90060
        assert parse_time('1d1h2m') == 90120
        assert parse_time('1d2h1s') == 93601
        assert parse_time('1d2h2s') == 93602
        assert parse_time('1d2h1m') == 93660
        assert parse_time('1d2h2m') == 93720
        assert parse_time('2d1m1s') == 172861
        assert parse_time('2d1m2s') == 172862
        assert parse_time('2d2m1s') == 172921
        assert parse_time('2d2m2s') == 172922
        assert parse_time('2d1h1s') == 176401
        assert parse_time('2d1h2s') == 176402
        assert parse_time('2d1h1m') == 176460
        assert parse_time('2d1h2m') == 176520
        assert parse_time('2d2h1s') == 180001
        assert parse_time('2d2h2s') == 180002
        assert parse_time('2d2h1m') == 180060
        assert parse_time('2d2h2m') == 180120

    def test_one_digit_quad_times(self):
        assert parse_time('1d1h1m1s') == 90061
        assert parse_time('1d1h1m2s') == 90062
        assert parse_time('1d1h2m1s') == 90121
        assert parse_time('1d1h2m2s') == 90122
        assert parse_time('1d2h1m1s') == 93661
        assert parse_time('1d2h1m2s') == 93662
        assert parse_time('1d2h2m1s') == 93721
        assert parse_time('1d2h2m2s') == 93722
        assert parse_time('2d1h1m1s') == 176461
        assert parse_time('2d1h1m2s') == 176462
        assert parse_time('2d1h2m1s') == 176521
        assert parse_time('2d1h2m2s') == 176522
        assert parse_time('2d2h1m1s') == 180061
        assert parse_time('2d2h1m2s') == 180062
        assert parse_time('2d2h2m1s') == 180121
        assert parse_time('2d2h2m2s') == 180122

    def test_two_digit_times(self):
        assert parse_time('10s') == 10
        assert parse_time('20s') == 20
        assert parse_time('10m') == 600
        assert parse_time('20m') == 1200
        assert parse_time('10h') == 36000
        assert parse_time('20h') == 72000
        assert parse_time('10d') == 864000
        assert parse_time('20d') == 1728000

    def test_three_digit_times(self):
        assert parse_time('100s') == 100
        assert parse_time('200s') == 200
        assert parse_time('100m') == 6000
        assert parse_time('200m') == 12000
        assert parse_time('100h') == 360000
        assert parse_time('200h') == 720000
        assert parse_time('100d') == 8640000
        assert parse_time('200d') == 17280000

    def test_no_letter_single_times(self):
        assert parse_time('1') == 60
        assert parse_time('2') == 120

    def test_no_letter_double_times(self):
        assert parse_time('10') == 600
        assert parse_time('20') == 1200

    def test_no_letter_triple_times(self):
        assert parse_time('100') == 6000
        assert parse_time('200') == 12000

    def test_empty_times(self):
        assert parse_time('0s') == 0
        assert parse_time('0m') == 0
        assert parse_time('0h') == 0
