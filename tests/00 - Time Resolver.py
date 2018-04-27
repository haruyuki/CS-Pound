import unittest

def resolver(hour, minute, second):
    hour_section = minute_section = second_section = ''

    def pluralise(string, value, and_placement=''):
        if value == 0:
            return ''
        else:
            temp = (' and ' if and_placement == 'pre' else '') + str(value) + ' ' + string + ('s' if value > 1 else '') + (' and ' if and_placement == 'suf' else (', ' if and_placement == 'com' else ''))
            return temp

    if (minute == 0 and second == 0) or (minute == 0 and second != 0):
        hour_section = pluralise('hour', hour)
    elif minute != 0 and second == 0:
        hour_section = pluralise('hour', hour, 'suf')
    else:
        hour_section = pluralise('hour', hour, 'com')

    minute_section = pluralise('minute', minute)

    if minute >= 1 or hour >= 1:
        second_section = pluralise('second', second, 'pre')
    else:
        second_section = pluralise('second', second)
    return hour_section + minute_section + second_section

#     time(hour,minute,second)

# def time(hour,minute,second):
#     time = '{}{}{}{}{}{}{}{}'.format(hour if hour != 0 else '', (' hours' if hour > 1 else ' hour') if hour != 0 else '','' if hour ==0 or (second==0 and minute==0) else(', ' if second !=0 and minute !=0 else ' and '), minute if minute !=0 else '', (' minutes' if minute >1 else ' minute') if minute !=0 else '',('' if hour ==0 and minute ==0 else ' and ') if second !=0 else '',second if second !=0 else '', (' seconds' if second > 1 else ' second') if second !=0 else '')
#     return time


class testStuff(unittest.TestCase):
    def test(self):
        self.assertEqual(time(0, 0, 1),'1 second')
        self.assertEqual(time(0, 0, 2),'2 seconds')
        self.assertEqual(time(0, 1, 0),'1 minute')
        self.assertEqual(time(0, 1, 1),'1 minute and 1 second')
        self.assertEqual(time(0, 1, 2),'1 minute and 2 seconds')
        self.assertEqual(time(0, 2, 0),'2 minutes')
        self.assertEqual(time(0, 2, 1),'2 minutes and 1 second')
        self.assertEqual(time(0, 2, 2),'2 minutes and 2 seconds')
        self.assertEqual(time(1, 0, 0),'1 hour')
        self.assertEqual(time(1, 0, 1),'1 hour and 1 second')
        self.assertEqual(time(1, 0, 2),'1 hour and 2 seconds')
        self.assertEqual(time(1, 1, 0),'1 hour and 1 minute')
        self.assertEqual(time(1, 1, 1),'1 hour, 1 minute and 1 second')
        self.assertEqual(time(1, 1, 2),'1 hour, 1 minute and 2 seconds')
        self.assertEqual(time(1, 2, 0),'1 hour and 2 minutes')
        self.assertEqual(time(1, 2, 1),'1 hour, 2 minutes and 1 second')
        self.assertEqual(time(1, 2, 2),'1 hour, 2 minutes and 2 seconds')
        self.assertEqual(time(2, 0, 0),'2 hours')
        self.assertEqual(time(2, 0, 1),'2 hours and 1 second')
        self.assertEqual(time(2, 0, 2),'2 hours and 2 seconds')
        self.assertEqual(time(2, 1, 0),'2 hours and 1 minute')
        self.assertEqual(time(2, 1, 1),'2 hours, 1 minute and 1 second')
        self.assertEqual(time(2, 1, 2),'2 hours, 1 minute and 2 seconds')
        self.assertEqual(time(2, 2, 0),'2 hours and 2 minutes')
        self.assertEqual(time(2, 2, 1),'2 hours, 2 minutes and 1 second')
        self.assertEqual(time(2, 2, 2),'2 hours, 2 minutes and 2 seconds')

# class language():

#     @staticMethod
#     def parser(string):
#         if string[0:8]


if __name__ == '__main__':
    unittest.main()
