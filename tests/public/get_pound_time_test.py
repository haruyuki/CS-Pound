from chickensmoothie import get_pound_time


class TestClass:
    def test_hour_only_strings(self):
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open within 6 hours') == 21600
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open within 5 hours') == 18000
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open within 4 hours') == 14400
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open within 3 hours') == 10800
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 2 hours') == 7200
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour') == 3600

    def test_minute_only_strings(self):
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 60 minutes') == 3600
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 59 minutes') == 3540
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 58 minutes') == 3480
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 57 minutes') == 3420
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 56 minutes') == 3360
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 55 minutes') == 3300
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 54 minutes') == 3240
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 53 minutes') == 3180
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 52 minutes') == 3120
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 51 minutes') == 3060
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 50 minutes') == 3000
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 49 minutes') == 2940
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 48 minutes') == 2880
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 47 minutes') == 2820
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 46 minutes') == 2760
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 45 minutes') == 2700
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 44 minutes') == 2640
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 43 minutes') == 2580
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 42 minutes') == 2520
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 41 minutes') == 2460
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 40 minutes') == 2400
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 39 minutes') == 2340
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 38 minutes') == 2280
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 37 minutes') == 2220
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 36 minutes') == 2160
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 35 minutes') == 2100
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 34 minutes') == 2040
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 33 minutes') == 1980
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 32 minutes') == 1920
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 31 minutes') == 1860
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 30 minutes') == 1800
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 29 minutes') == 1740
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 28 minutes') == 1680
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 27 minutes') == 1620
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 26 minutes') == 1560
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 25 minutes') == 1500
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 24 minutes') == 1440
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 23 minutes') == 1380
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 22 minutes') == 1320
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 21 minutes') == 1260
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 20 minutes') == 1200
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 19 minutes') == 1140
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 18 minutes') == 1080
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 17 minutes') == 1020
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 16 minutes') == 960
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 15 minutes') == 900
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 14 minutes') == 840
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 13 minutes') == 780
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 12 minutes') == 720
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 11 minutes') == 660
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 10 minutes') == 600
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 9 minutes') == 540
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 8 minutes') == 480
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 7 minutes') == 420
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 6 minutes') == 360
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 5 minutes') == 300
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 4 minutes') == 240
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 3 minutes') == 180
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 2 minutes') == 120
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will in: 1 minute') == 60

    def test_hour_and_minute_strings(self):
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 60 minutes') == 7200
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 59 minutes') == 7140
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 58 minutes') == 7080
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 57 minutes') == 7020
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 56 minutes') == 6960
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 55 minutes') == 6900
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 54 minutes') == 6840
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 53 minutes') == 6780
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 52 minutes') == 6720
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 51 minutes') == 6660
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 50 minutes') == 6600
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 49 minutes') == 6540
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 48 minutes') == 6480
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 47 minutes') == 6420
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 46 minutes') == 6360
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 45 minutes') == 6300
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 44 minutes') == 6240
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 43 minutes') == 6180
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 42 minutes') == 6120
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 41 minutes') == 6060
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 40 minutes') == 6000
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 39 minutes') == 5940
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 38 minutes') == 5880
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 37 minutes') == 5820
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 36 minutes') == 5760
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 35 minutes') == 5700
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 34 minutes') == 5640
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 33 minutes') == 5580
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 32 minutes') == 5520
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 31 minutes') == 5460
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 30 minutes') == 5400
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 29 minutes') == 5340
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 28 minutes') == 5280
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 27 minutes') == 5220
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 26 minutes') == 5160
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 25 minutes') == 5100
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 24 minutes') == 5040
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 23 minutes') == 4980
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 22 minutes') == 4920
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 21 minutes') == 4860
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 20 minutes') == 4800
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 19 minutes') == 4740
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 18 minutes') == 4680
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 17 minutes') == 4620
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 16 minutes') == 4560
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 15 minutes') == 4500
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 14 minutes') == 4440
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 13 minutes') == 4380
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 12 minutes') == 4320
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 11 minutes') == 4260
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 10 minutes') == 4200
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 9 minutes') == 4140
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 8 minutes') == 4080
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 7 minutes') == 4020
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 6 minutes') == 3960
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 5 minutes') == 3900
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 4 minutes') == 3840
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 3 minutes') == 3780
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 2 minutes') == 3720
        assert get_pound_time('Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 1 minute') == 3660

    def test_no_times(self):
        assert get_pound_time('Sorry, the pound is closed at the moment.The pound closed less than three hours ago! The pound opens at totally random times of day, so check back later to try again :)') == 0
        assert get_pound_time('Sorry, the pound is closed at the moment.The pound closed less than two hours ago! The pound opens at totally random times of day, so check back later to try again :)') == 0
        assert get_pound_time('Sorry, the pound is closed at the moment.The pound closed less than one hour ago! The pound opens at totally random times of day, so check back later to try again :)') == 0
