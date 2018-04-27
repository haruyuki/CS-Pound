# Sorry, the pound is closed at the moment. The pound will open in: 8 minutes
# Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 29 minutes
# Sorry, the pound is closed at the moment. The pound will open in: 1 hour, 1 minute
test2 = 'Sorry, the pound is closed at the moment. The pound will open within 4 hours'
test1 = 'Sorry, the pound is closed at the moment. The pound closed less than three hours ago! The pound opens at totally random times of the day, so check back later to try again :)'

print(test[46:])

if ':)' not in test:
	print('ok')
else:
	print('none')


try:
    val = ':as'[10]
    if ':)' not in val:
        val += '.'
except IndexError:
    val = 'Pound is currently open!'

print(val)