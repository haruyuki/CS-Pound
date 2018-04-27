import unittest

def resolver(day, hour, minute, second):  # Pretty format given hours, minutes and seconds
    day_section = ''
    hour_section = ''
    minute_section = ''
    second_section = ''

    def pluralise(string, value, and_placement=''):  # Add ',' or 'and' into string
        if value == 0:  # If given time has no value
            return ''
        else:  # If given time has value
            return (' and ' if and_placement == 'pre' else '') + str(value) + ' ' + string + ('s' if value > 1 else '') + (' and ' if and_placement == 'suf' else (', ' if and_placement == 'com' else ''))
    

    # If there are seconds but no minute or hour or day (second)
    # If there are seconds and anything else before (second, (day, hour, minute))

    # If there are minutes but no seconds

    # If there are no minutes or seconds (hour), or no minute but seconds (hour,second)
    # If there are minutes but no seconds (hour, minute)
    # If there are 1 or more hour or minute (hour, minute, second)
    # If there are no hours or minutes (second)

    if day != 0 and ((hour == 0 and minute == 0) or (hour == 0 and second == 0) or (minute == 0 and second == 0)):
        day_section = pluralise('day', day, 'suf')
    elif day != 0 and (hour != 0 and minute != 0 and second != 0):
        day_section = pluralise('day', day, 'com')
    elif day != 0 and ((hour != 0 and minute == 0) or (hour != 0 and second == 0) or (minute != 0 and second == 0) or (hour == 0 and minute != 0) or (hour == 0 and second != 0) or (minute == 0 and second != 0)):
        day_section = pluralise('day', day, 'com')

    if (minute == 0 and second == 0) or (minute == 0 and second != 0):  # If there are no minutes or seconds, or no minute but seconds
        hour_section = pluralise('hour', hour)
    elif minute != 0 and second == 0:  # If there are minutes but no seconds
        hour_section = pluralise('hour', hour, 'suf')
    else:  # If there are minutes and seconds
        hour_section = pluralise('hour', hour, 'com')

    minute_section = pluralise('minute', minute)
    
    if hour != 0 or minute != 0 or day != 0:  # If there are 1 or more hour or minute
        second_section = pluralise('second', second, 'pre')
    else:  # If there are no hours or minutes
        second_section = pluralise('second', second)
    return day_section + hour_section + minute_section + second_section


class testStuff(unittest.TestCase):
    def test(self):
        self.assertEqual(resolver(0, 0, 0, 1),'1 second')
        self.assertEqual(resolver(0, 0, 0, 2),'2 seconds')
        self.assertEqual(resolver(0, 0, 1, 0),'1 minute')
        self.assertEqual(resolver(0, 0, 1, 1),'1 minute and 1 second')
        self.assertEqual(resolver(0, 0, 1, 2),'1 minute and 2 seconds')
        self.assertEqual(resolver(0, 0, 2, 0),'2 minutes')
        self.assertEqual(resolver(0, 0, 2, 1),'2 minutes and 1 second')
        self.assertEqual(resolver(0, 0, 2, 2),'2 minutes and 2 seconds')
        self.assertEqual(resolver(0, 1, 0, 0),'1 hour')
        self.assertEqual(resolver(0, 1, 0, 1),'1 hour and 1 second')
        self.assertEqual(resolver(0, 1, 0, 2),'1 hour and 2 seconds')
        self.assertEqual(resolver(0, 1, 1, 0),'1 hour and 1 minute')
        self.assertEqual(resolver(0, 1, 1, 1),'1 hour, 1 minute and 1 second')
        self.assertEqual(resolver(0, 1, 1, 2),'1 hour, 1 minute and 2 seconds')
        self.assertEqual(resolver(0, 1, 2, 0),'1 hour and 2 minutes')
        self.assertEqual(resolver(0, 1, 2, 1),'1 hour, 2 minutes and 1 second')
        self.assertEqual(resolver(0, 1, 2, 2),'1 hour, 2 minutes and 2 seconds')
        self.assertEqual(resolver(0, 2, 0, 0),'2 hours')
        self.assertEqual(resolver(0, 2, 0, 1),'2 hours and 1 second')
        self.assertEqual(resolver(0, 2, 0, 2),'2 hours and 2 seconds')
        self.assertEqual(resolver(0, 2, 1, 0),'2 hours and 1 minute')
        self.assertEqual(resolver(0, 2, 1, 1),'2 hours, 1 minute and 1 second')
        self.assertEqual(resolver(0, 2, 1, 2),'2 hours, 1 minute and 2 seconds')
        self.assertEqual(resolver(0, 2, 2, 0),'2 hours and 2 minutes')
        self.assertEqual(resolver(0, 2, 2, 1),'2 hours, 2 minutes and 1 second')
        self.assertEqual(resolver(0, 2, 2, 2),'2 hours, 2 minutes and 2 seconds')
        self.assertEqual(resolver(1, 0, 0, 1),'1 day and 1 second')
        self.assertEqual(resolver(1, 0, 0, 2),'1 day and 2 seconds')
        self.assertEqual(resolver(1, 0, 1, 0),'1 day and 1 minute')
        self.assertEqual(resolver(1, 0, 1, 1),'1 day, 1 minute and 1 second')
        self.assertEqual(resolver(1, 0, 1, 2),'1 day, 1 minute and 2 seconds')
        self.assertEqual(resolver(1, 0, 2, 0),'1 day and 2 minutes')
        self.assertEqual(resolver(1, 0, 2, 1),'1 day, 2 minutes and 1 second')
        self.assertEqual(resolver(1, 0, 2, 2),'1 day, 2 minutes and 2 seconds')
        self.assertEqual(resolver(1, 1, 0, 0),'1 day and 1 hour')
        self.assertEqual(resolver(1, 1, 0, 1),'1 day, 1 hour and 1 second')
        self.assertEqual(resolver(1, 1, 0, 2),'1 day, 1 hour and 2 seconds')
        self.assertEqual(resolver(1, 1, 1, 0),'1 day, 1 hour and 1 minute')
        self.assertEqual(resolver(1, 1, 1, 1),'1 day, 1 hour, 1 minute and 1 second')
        self.assertEqual(resolver(1, 1, 1, 2),'1 day, 1 hour, 1 minute and 2 seconds')
        self.assertEqual(resolver(1, 1, 2, 0),'1 day, 1 hour and 2 minutes')
        self.assertEqual(resolver(1, 1, 2, 1),'1 day, 1 hour, 2 minutes and 1 second')
        self.assertEqual(resolver(1, 1, 2, 2),'1 day, 1 hour, 2 minutes and 2 seconds')
        self.assertEqual(resolver(1, 2, 0, 0),'1 day and 2 hours')
        self.assertEqual(resolver(1, 2, 0, 1),'1 day, 2 hours and 1 second')
        self.assertEqual(resolver(1, 2, 0, 2),'1 day, 2 hours and 2 seconds')
        self.assertEqual(resolver(1, 2, 1, 0),'1 day, 2 hours and 1 minute')
        self.assertEqual(resolver(1, 2, 1, 1),'1 day, 2 hours, 1 minute and 1 second')
        self.assertEqual(resolver(1, 2, 1, 2),'1 day, 2 hours, 1 minute and 2 seconds')
        self.assertEqual(resolver(1, 2, 2, 0),'1 day, 2 hours and 2 minutes')
        self.assertEqual(resolver(1, 2, 2, 1),'1 day, 2 hours, 2 minutes and 1 second')
        self.assertEqual(resolver(1, 2, 2, 2),'1 day, 2 hours, 2 minutes and 2 seconds')
        self.assertEqual(resolver(2, 0, 0, 1),'2 days and 1 second')
        self.assertEqual(resolver(2, 0, 0, 2),'2 days and 2 seconds')
        self.assertEqual(resolver(2, 0, 1, 0),'2 days and 1 minute')
        self.assertEqual(resolver(2, 0, 1, 1),'2 days, 1 minute and 1 second')
        self.assertEqual(resolver(2, 0, 1, 2),'2 days, 1 minute and 2 seconds')
        self.assertEqual(resolver(2, 0, 2, 0),'2 days and 2 minutes')
        self.assertEqual(resolver(2, 0, 2, 1),'2 days, 2 minutes and 1 second')
        self.assertEqual(resolver(2, 0, 2, 2),'2 days, 2 minutes and 2 seconds')
        self.assertEqual(resolver(2, 1, 0, 0),'2 days and 1 hour')
        self.assertEqual(resolver(2, 1, 0, 1),'2 days, 1 hour and 1 second')
        self.assertEqual(resolver(2, 1, 0, 2),'2 days, 1 hour and 2 seconds')
        self.assertEqual(resolver(2, 1, 1, 0),'2 days, 1 hour and 1 minute')
        self.assertEqual(resolver(2, 1, 1, 1),'2 days, 1 hour, 1 minute and 1 second')
        self.assertEqual(resolver(2, 1, 1, 2),'2 days, 1 hour, 1 minute and 2 seconds')
        self.assertEqual(resolver(2, 1, 2, 0),'2 days, 1 hour and 2 minutes')
        self.assertEqual(resolver(2, 1, 2, 1),'2 days, 1 hour, 2 minutes and 1 second')
        self.assertEqual(resolver(2, 1, 2, 2),'2 days, 1 hour, 2 minutes and 2 seconds')
        self.assertEqual(resolver(2, 2, 0, 0),'2 days and 2 hours')
        self.assertEqual(resolver(2, 2, 0, 1),'2 days, 2 hours and 1 second')
        self.assertEqual(resolver(2, 2, 0, 2),'2 days, 2 hours and 2 seconds')
        self.assertEqual(resolver(2, 2, 1, 0),'2 days, 2 hours and 1 minute')
        self.assertEqual(resolver(2, 2, 1, 1),'2 days, 2 hours, 1 minute and 1 second')
        self.assertEqual(resolver(2, 2, 1, 2),'2 days, 2 hours, 1 minute and 2 seconds')
        self.assertEqual(resolver(2, 2, 2, 0),'2 days, 2 hours and 2 minutes')
        self.assertEqual(resolver(2, 2, 2, 1),'2 days, 2 hours, 2 minutes and 1 second')
        self.assertEqual(resolver(2, 2, 2, 2),'2 days, 2 hours, 2 minutes and 2 seconds')

# class language():

#     @staticMethod
#     def parser(string):
#         if string[0:8]


if __name__ == '__main__':
    unittest.main()
