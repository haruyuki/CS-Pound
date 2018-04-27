
url = 'http://www.chickensmoothie.com/viewpet.php?id=179904346'
soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
petimg = soup.find(id='petimg').get('src')
titles = soup.find_all(True,'l')
values = soup.find_all(True,'r')
tables = len(titles)
given = ''
temp = ''

for i in range(tables):
    print('ran')
    exec('title' + str(i) + '=' + '"' + str(titles[i].string.replace('\t','').replace('\n','')) + '"')
    exec('print(title' + str(i) + ')')

for i in range(tables):
    if i == 0:
        value0 = '[' + soup.find_all(True,'r')[0].a.string + ']' + '(' + 'http://www.chickensmoothie.com/' + soup.find_all(True,'r')[0].a.get('href') + ')'
    elif len(values) - i == 2 or len(values) - i == 1:
        exec('temp = title' + str(i))
        if temp == 'Growth:' or given == 'False':
            given = 'False'
            if len(values) - i == 2:
                exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].string + '"')
            elif len(values) - i == 1:
                exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].img.get('alt') + '"')
        elif temp == 'Rarity:' or given == 'True':
            given = 'True'
            if len(values) - i == 2:
                exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].img.get('alt') + '"')
            elif len(values) - i == 1:
                exec('value' + str(i) + '=' + '"' + '[' + soup.find_all(True,'r')[i].a.string + ']' + '(' + 'http://www.chickensmoothie.com/' + soup.find_all(True,'r')[i].a.get('href') + ')' + '"')
    else:
        exec('value' + str(i) + '=' + '"' + soup.find_all(True,'r')[i].string + '"')