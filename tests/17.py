import unittest

def time_extractor(time):
    time = time.lower()
    if 'h' in time:
        htotal = time.split('h')[0]
    else:
        htotal = 0

    if 'm' in time:
        if 'h' in time:
            temp = time.split('h')[1]
            mtotal = temp.split('m')[0]
        else:
            mtotal = time.split('m')[0]
    else:
        mtotal = 0

    if 's' in time:
        if 'h' in time:
            temp = time.split('h')[1]
            if 'm' in time:
                temp2 = temp.split('m')[1]
                stotal = temp2.split('s')[0]
            else:
                stotal = temp.split('s')[0]
        else:
            stotal = time.split('s')[0]
    else:
        mtotal = 0
    htotal = int(htotal)
    mtotal = int(mtotal)
    stotal = int(stotal)
    if htotal == 0 and mtotal == 0 and stotal == 0:
        finaltotal = 0
    else:
        finaltotal = int((htotal * 60 * 60) + (mtotal * 60) + stotal)
    return finaltotal, htotal, mtotal, stotal

class testStuff(unittest.TestCase):
    def test(self):
        self.assertEqual(time_extractor('1s'), (1, 0, 0, 1))
        self.assertEqual(time_extractor('1m'), (60, 0, 1, 0))
        self.assertEqual(time_extractor('1m1s'), (61, 0, 1, 1))
        self.assertEqual(time_extractor('1h'), (3600, 1, 0, 0))
        self.assertEqual(time_extractor('1h1s'), (3601, 1, 0, 1))
        self.assertEqual(time_extractor('1h1m'), (3660, 1, 1, 0))
        self.assertEqual(time_extractor('1h1m1s'), (3661, 1, 1, 1))

if __name__ == '__main__':
    unittest.main()