import timeit

s = '''\
import requests
import lxml.html
link = 'http://www.chickensmoothie.com/viewpet.php?id=258548736'
parameters = link.split('?')[1].split('=')
data = {}
data[parameters[0]] = parameters[1]
response = requests.post('http://www.chickensmoothie.com/viewpet.php', params=data)
dom = lxml.html.fromstring(response.text)'''

t = '''\
import lxml.html
import urllib.request
link = 'http://www.chickensmoothie.com/viewpet.php?id=258548736'
connection = urllib.request.urlopen(link)
dom = lxml.html.fromstring(connection.read())'''

print(timeit.timeit(stmt=s,number=3))  # FASTER
print(timeit.timeit(stmt=t,number=3))