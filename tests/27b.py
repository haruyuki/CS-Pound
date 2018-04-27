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
    
    if hour != 0 or minute != 0:  # If there are 1 or more hour or minute
        second_section = pluralise('second', second, 'pre')
    else:  # If there are no hours or minutes
        second_section = pluralise('second', second)
    return day_section + hour_section + minute_section + second_section

print(resolver(10,22,0,30))