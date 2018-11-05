from library import formatter


class TestClass:
    def test_seconds(self):
        assert formatter(0, 0, 0, 1) == '1 second'
        assert formatter(0, 0, 0, 2) == '2 seconds'

    def test_minutes(self):
        assert formatter(0, 0, 1, 0) == '1 minute'
        assert formatter(0, 0, 2, 0) == '2 minutes'

    def test_hours(self):
        assert formatter(0, 1, 0, 0) == '1 hour'
        assert formatter(0, 2, 0, 0) == '2 hours'

    def test_days(self):
        assert formatter(1, 0, 0, 0) == '1 day'
        assert formatter(2, 0, 0, 0) == '2 days'

    def test_double_combined(self):
        assert formatter(0, 0, 1, 1) == '1 minute and 1 second'
        assert formatter(0, 0, 1, 2) == '1 minute and 2 seconds'
        assert formatter(0, 0, 2, 1) == '2 minutes and 1 second'
        assert formatter(0, 0, 2, 2) == '2 minutes and 2 seconds'

        assert formatter(0, 1, 0, 1) == '1 hour and 1 second'
        assert formatter(0, 1, 0, 2) == '1 hour and 2 seconds'
        assert formatter(0, 1, 1, 0) == '1 hour and 1 minute'
        assert formatter(0, 1, 2, 0) == '1 hour and 2 minutes'
        assert formatter(0, 2, 0, 1) == '2 hours and 1 second'
        assert formatter(0, 2, 0, 2) == '2 hours and 2 seconds'
        assert formatter(0, 2, 1, 0) == '2 hours and 1 minute'
        assert formatter(0, 2, 2, 0) == '2 hours and 2 minutes'

        assert formatter(1, 0, 0, 1) == '1 day and 1 second'
        assert formatter(1, 0, 0, 2) == '1 day and 2 seconds'
        assert formatter(1, 0, 1, 0) == '1 day and 1 minute'
        assert formatter(1, 0, 2, 0) == '1 day and 2 minutes'
        assert formatter(1, 1, 0, 0) == '1 day and 1 hour'
        assert formatter(1, 2, 0, 0) == '1 day and 2 hours'
        assert formatter(2, 0, 0, 1) == '2 days and 1 second'
        assert formatter(2, 0, 0, 2) == '2 days and 2 seconds'
        assert formatter(2, 0, 1, 0) == '2 days and 1 minute'
        assert formatter(2, 0, 2, 0) == '2 days and 2 minutes'
        assert formatter(2, 1, 0, 0) == '2 days and 1 hour'
        assert formatter(2, 2, 0, 0) == '2 days and 2 hours'

    def test_triple_combined(self):
        assert formatter(0, 1, 1, 1) == '1 hour, 1 minute and 1 second'
        assert formatter(0, 1, 1, 2) == '1 hour, 1 minute and 2 seconds'
        assert formatter(0, 1, 2, 1) == '1 hour, 2 minutes and 1 second'
        assert formatter(0, 1, 2, 2) == '1 hour, 2 minutes and 2 seconds'
        assert formatter(0, 2, 1, 1) == '2 hours, 1 minute and 1 second'
        assert formatter(0, 2, 1, 2) == '2 hours, 1 minute and 2 seconds'
        assert formatter(0, 2, 2, 1) == '2 hours, 2 minutes and 1 second'
        assert formatter(0, 2, 2, 2) == '2 hours, 2 minutes and 2 seconds'

        assert formatter(1, 0, 1, 1) == '1 day, 1 minute and 1 second'
        assert formatter(1, 0, 1, 2) == '1 day, 1 minute and 2 seconds'
        assert formatter(1, 0, 2, 1) == '1 day, 2 minutes and 1 second'
        assert formatter(1, 0, 2, 2) == '1 day, 2 minutes and 2 seconds'
        assert formatter(1, 1, 0, 1) == '1 day, 1 hour and 1 second'
        assert formatter(1, 1, 0, 2) == '1 day, 1 hour and 2 seconds'
        assert formatter(1, 1, 1, 0) == '1 day, 1 hour and 1 minute'
        assert formatter(1, 1, 2, 0) == '1 day, 1 hour and 2 minutes'
        assert formatter(1, 2, 0, 1) == '1 day, 2 hours and 1 second'
        assert formatter(1, 2, 0, 2) == '1 day, 2 hours and 2 seconds'
        assert formatter(1, 2, 1, 0) == '1 day, 2 hours and 1 minute'
        assert formatter(1, 2, 2, 0) == '1 day, 2 hours and 2 minutes'
        assert formatter(2, 0, 1, 1) == '2 days, 1 minute and 1 second'
        assert formatter(2, 0, 1, 2) == '2 days, 1 minute and 2 seconds'
        assert formatter(2, 0, 2, 1) == '2 days, 2 minutes and 1 second'
        assert formatter(2, 0, 2, 2) == '2 days, 2 minutes and 2 seconds'
        assert formatter(2, 1, 0, 1) == '2 days, 1 hour and 1 second'
        assert formatter(2, 1, 0, 2) == '2 days, 1 hour and 2 seconds'
        assert formatter(2, 1, 1, 0) == '2 days, 1 hour and 1 minute'
        assert formatter(2, 1, 2, 0) == '2 days, 1 hour and 2 minutes'
        assert formatter(2, 2, 0, 1) == '2 days, 2 hours and 1 second'
        assert formatter(2, 2, 0, 2) == '2 days, 2 hours and 2 seconds'
        assert formatter(2, 2, 1, 0) == '2 days, 2 hours and 1 minute'
        assert formatter(2, 2, 2, 0) == '2 days, 2 hours and 2 minutes'

    def test_quad_combined(self):
        assert formatter(1, 1, 1, 1) == '1 day, 1 hour, 1 minute and 1 second'
        assert formatter(1, 1, 1, 2) == '1 day, 1 hour, 1 minute and 2 seconds'
        assert formatter(1, 1, 2, 1) == '1 day, 1 hour, 2 minutes and 1 second'
        assert formatter(1, 1, 2, 2) == '1 day, 1 hour, 2 minutes and 2 seconds'
        assert formatter(1, 2, 1, 1) == '1 day, 2 hours, 1 minute and 1 second'
        assert formatter(1, 2, 1, 2) == '1 day, 2 hours, 1 minute and 2 seconds'
        assert formatter(1, 2, 2, 1) == '1 day, 2 hours, 2 minutes and 1 second'
        assert formatter(1, 2, 2, 2) == '1 day, 2 hours, 2 minutes and 2 seconds'
        assert formatter(2, 1, 1, 1) == '2 days, 1 hour, 1 minute and 1 second'
        assert formatter(2, 1, 1, 2) == '2 days, 1 hour, 1 minute and 2 seconds'
        assert formatter(2, 1, 2, 1) == '2 days, 1 hour, 2 minutes and 1 second'
        assert formatter(2, 1, 2, 2) == '2 days, 1 hour, 2 minutes and 2 seconds'
        assert formatter(2, 2, 1, 1) == '2 days, 2 hours, 1 minute and 1 second'
        assert formatter(2, 2, 1, 2) == '2 days, 2 hours, 1 minute and 2 seconds'
        assert formatter(2, 2, 2, 1) == '2 days, 2 hours, 2 minutes and 1 second'
        assert formatter(2, 2, 2, 2) == '2 days, 2 hours, 2 minutes and 2 seconds'
