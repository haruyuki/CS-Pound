from constants import Variables
from library import calculate_sleep_amount


class TestClass:
    def test_on_cooldown_less_than_1_hour(self):
        Variables.cooldown = True
        assert calculate_sleep_amount(1) == (-59, 60, True)
        assert calculate_sleep_amount(3599) == (3539, 60, True)
        assert calculate_sleep_amount(3600) == (3540, 60, True)
        assert calculate_sleep_amount(0) == (0, 3600, False)

    def test_off_cooldown_no_time(self):
        Variables.cooldown = False
        assert calculate_sleep_amount(-1) == (-1, 3600, False)
        assert calculate_sleep_amount(0) == (0, 3600, False)

    def test_off_cooldown_more_than_2_hours(self):
        Variables.cooldown = False
        assert calculate_sleep_amount(7201) == (7201, 1, False)
        assert calculate_sleep_amount(7200) == (7200, 0, False)

    def test_off_cooldown_between_1_and_2_hours(self):
        Variables.cooldown = False
        assert calculate_sleep_amount(3601) == (3600, 1, False)
        Variables.cooldown = False
        assert calculate_sleep_amount(3600) == (3600, 0, False)

    def test_off_cooldown_less_than_1_hour(self):
        Variables.cooldown = False
        assert calculate_sleep_amount(3599) == (3599, 0, False)
        Variables.cooldown = False
        assert calculate_sleep_amount(1) == (1, 0, False)

    def test_off_cooldown_10_hours(self):
        Variables.cooldown = False
        assert calculate_sleep_amount(36000) == (36000, 3600, False)