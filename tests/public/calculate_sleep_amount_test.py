from constants import Variables
from library import calculate_sleep_amount


class TestClass:
    def test_no_time(self):
        assert calculate_sleep_amount(-1) == (-1, 3600, False)
        assert calculate_sleep_amount(0) == (0, 3600, False)

    def test_10_hours(self):
        assert calculate_sleep_amount(36000) == (36000, 3600, False)

    def test_more_than_2_hours(self):
        assert calculate_sleep_amount(7201) == (7201, 1, False)
        assert calculate_sleep_amount(7200) == (7200, 0, False)

    def test_between_1_and_2_hours(self):
        assert calculate_sleep_amount(3601) == (3600, 1, False)
        assert calculate_sleep_amount(7199) == (7199, 3599, False)

    def test_less_than_1_hour(self):
        assert calculate_sleep_amount(1) == (-59, 60, True)
        assert calculate_sleep_amount(3599) == (3539, 60, True)
        assert calculate_sleep_amount(3600) == (3540, 60, True)
        assert calculate_sleep_amount(0) == (0, 3600, False)
