owner = soup.find_all('td')[2].a.string
ownerlink = 'http://www.chickensmoothie.com/' + soup.find_all('td')[2].a.get('href')
petid = soup.find_all('td')[4].string
name = soup.find_all('td')[6].string
adopted = soup.find_all('td')[8].string
age = soup.find_all('td')[10].string
growth = soup.find_all('td')[12].string
rarity = soup.find_all('td')[14].img.get('alt')
givenby = soup.find_all('td')[15].string.replace('\t','').replace('\n','')
givenbyname = soup.find_all('td')[16].a.string
givenbylink = 'http://www.chickensmoothie.com/' + soup.find_all('td')[16].a.get('href')









		
