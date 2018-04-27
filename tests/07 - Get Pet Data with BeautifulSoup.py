values = soup.find_all(True,'r')
given = ''
for i in range(len(values)):
	if i == 0:
		print('i has equaled 0')
		value0 = '[' + soup.find_all(True,'r')[0].a.string + ']' + '(' + 'http://www.chickensmoothie.com/' + soup.find_all(True,'r')[0].a.get('href') + ')'
	elif len(values) - i == 2 or len(values) - i == 1:
		print('Value of i is currently' + str(i))
		exec('temp = title' + str(i))
		if temp == 'Growth:' or given == 'False': # No given
			print('There is no given')
			given = 'False'
			if len(values) - i == 2:
				exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].string + '"')
			elif len(values) - i == 1:
				exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].img.get('alt') + '"')
		elif temp == 'Rarity:' or given == 'True': # Is given
			print('There is a given')
			given = 'True'
			if len(values) - i == 2:
				exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].img.get('alt') + '"')
			elif len(values) - i == 1:
				exec('value' + str(i) + '=' + '"' + '[' + soup.find_all(True,'r')[i].a.string + ']' + '(' + 'http://www.chickensmoothie.com/' + soup.find_all(True,'r')[i].a.get('href') + ')' + '"')
	else:
		print('It doesn\'t apply to anything')
		exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].string + '"')