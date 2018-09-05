import re

prefix = '.'
version = '2.12'


# -------------------- FUNCTIONS --------------------
def parse_short_time(time):
    timestr = time.lower()
    if not re.findall('\\d{1,8}[smhd]', timestr):
        return -1
    multiplier = 1
    for i in range(len(timestr)):
        if timestr[i] == 'd':
            multiplier *= 86400
        elif timestr[i] == 'h':
            multiplier *= 3600
        elif timestr[i] == 'm':
            multiplier *= 60
        elif timestr[i] == 's':
            timestr = timestr[:-1]
    return multiplier * int(''.join([x for x in timestr if x.isdigit()]))


def time_extractor(time):  # Convert given time into seconds
    time = time.lower()  # Change all letters to lowercase
    htotal = 0
    mtotal = 0
    stotal = 0
    if 'h' not in time and 'm' not in time and 's' not in time:  # If there is no time at all
        pass
    elif 'h' in time or 'hr' in time:  # If hours in input
        htotal = time.split('h')[0]  # Split input and get number of hours
        if 'm' in time:  # If minutes in input
            temp = time.split('h')[1]  # Split input and get leftover time (minutes and seconds)
            mtotal = temp.split('m')[0]  # Split temp and get number of minutes
            if 's' in time:  # If seconds in input
                temp = time.split('h')[1]  # Split input and get leftover time (minutes and seconds)
                temp2 = temp.split('m')[1]  # Split temp and get leftover time (seconds)
                stotal = temp2.split('s')[0]  # Split temp2 and get number of seconds
        else:  # If no minutes in input
            if 's' in time:  # If seconds in input
                temp = time.split('h')[1]  # Split input and get leftover time (seconds)
                stotal = temp.split('s')[0]  # Split temp and get number of seconds
    else:  # If no hours in input
        if 'm' in time:  # If minutes in input
            mtotal = time.split('m')[0]  # Split input and get number of minutes
            if 's' in time:  # If seconds in input
                temp = time.split('m')[1]  # Split input and get leftover time (seconds)
                stotal = temp.split('s')[0]  # Split temp and get number of seconds
        else:  # If no minutes in input
            if 's' in time:  # If seconds in input
                stotal = time.split('s')[0]  # Split input and get number of seconds
    htotal = int(htotal)  # Convert 'htotal' into integer
    mtotal = int(mtotal)  # Convert 'mtotal' into integer
    stotal = int(stotal)  # Convert 'stotal' into integer
    if htotal == 0 and mtotal == 0 and stotal == 0:  # If hours, minutes and seconds is 0
        finaltotal = 0
    else:  # If values in hours, minutes or seconds
        finaltotal = int((htotal * 60 * 60) + (mtotal * 60) + stotal)  # Total time in seconds
    return finaltotal, htotal, mtotal, stotal  # Return a tuple


def resolver(day, hour, minute, second):  # Pretty format time layout given days, hours, minutes and seconds
    day_section = ''

    def pluralise(string, value, and_placement=''):  # Correctly prefix or suffix ',' or 'and' placements
        if value == 0:  # If given time has no value
            return ''
        else:  # If given time has value
            return (' and ' if and_placement == 'pre' else '') + str(value) + ' ' + string + ('s' if value > 1 else '') + (' and ' if and_placement == 'suf' else (', ' if and_placement == 'com' else ''))
            # If 'and_placement' is set to prefix add 'and' otherwise leave blank
            # The value of the time
            # The type of time (day, hour, minute, second)
            # If value is larger than 1 then pluralise the time
            # If 'and_placement' is set to suffix add 'and' otherwise add a ',' instead if 'and_placement' is set to comma otherwise leave blank

    if day != 0 and ((hour == 0 and minute == 0) or (hour == 0 and second == 0) or (minute == 0 and second == 0)):
        # If there are day(s) but:
        # No hours or minutes
        # No hours or seconds
        # No minutes or seconds
        day_section = pluralise('day', day, 'suf')  # Pluralise the day section with a suffixed 'and' placement
    elif day != 0 and ((hour != 0 and minute != 0 and second != 0) or (hour != 0 and minute == 0) or (hour != 0 and second == 0) or (minute != 0 and second == 0) or (hour == 0 and minute != 0) or (hour == 0 and second != 0) or (minute == 0 and second != 0)):
        # If there are day(s) but:
        # There are hour(s) and minute(s) and second(s)
        # There are hour(s) but no minutes
        # There are hour(s) but no seconds
        # There are minute(s) but no hours
        # There are minute(s) but no seconds
        # There are second(s) but no hours
        # There are second(s) but no minutes
        day_section = pluralise('day', day, 'com')  # Pluralise the day section with a suffixed ',' placement

    if minute == 0:  # If there are no minutes
        hour_section = pluralise('hour', hour)  # Pluralise the hour section
    elif minute != 0 and second == 0:  # If there are minute(s) but no seconds
        hour_section = pluralise('hour', hour, 'suf')  # Pluralise the hour section with a suffixed 'and' placement
    else:  # If there are minute(s) and second(s)
        hour_section = pluralise('hour', hour, 'com')  # Pluralise the hour section with a suffixed ',' placement

    minute_section = pluralise('minute', minute)  # Pluralise the minute section

    if hour != 0 or minute != 0:  # If there are hour(s) or minute(s)
        second_section = pluralise('second', second, 'pre')  # Pluralise the second section with a prefixed 'and' placement
    else:  # If there are no hours or minutes
        second_section = pluralise('second', second)  # Pluralise the second section
    return day_section + hour_section + minute_section + second_section  # Return the formatted text
