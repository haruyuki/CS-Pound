from bs4 import BeautifulSoup, SoupStrainer
import urllib

link = 'http://www.chickensmoothie.com/viewpet.php?id=256666666'
soup = BeautifulSoup(urllib.request.urlopen(link).read(), 'lxml', parse_only=SoupStrainer('table'))

petimg = soup.find(id='petimg').get('src')
titles = soup.find_all(True, 'l')
values = soup.find_all(True, 'r')
tables = len(titles)
given = True
title_list = []
value_list = []

for i in range(tables):
    title_list.append(titles[i].string.replace('\t', '').replace('\n', ''))
    if i == 0:
        value_list.append('[' + soup.find_all(True, 'r')[0].a.string + ']' + '(' + 'http://www.chickensmoothie.com/' + soup.find_all(True, 'r')[0].a.get('href') + ')')
    elif len(values) - i == 2 or len(values) - i == 1:
        if title_list[i] == 'Growth:' or not given:
            given = False
            if len(values) - i == 2:
                value_list.append(soup.find_all(True, 'r')[i].string)
            elif len(values) - i == 1:
                value_list.append(soup.find_all(True, 'r')[i].img.get('alt'))
        elif title_list[i] == 'Rarity:' or given:
            given = True
            if len(values) - i == 2:
                value_list.append(soup.find_all(True, 'r')[i].img.get('alt'))
            elif len(values) - i == 1:
                value_list.append('[' + soup.find_all(True, 'r')[i].a.string + ']' + '(' + 'http://www.chickensmoothie.com/' + soup.find_all(True, 'r')[i].a.get('href') + ')')
    else:
        value_list.append(soup.find_all(True, 'r')[i].string)

print(title_list)
print(value_list)