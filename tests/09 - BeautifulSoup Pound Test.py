from bs4 import BeautifulSoup, SoupStrainer
import urllib

data = urllib.request.urlopen('http://www.chickensmoothie.com/pound.php')
t = data.read()
dom = html5lib.parse(t, treebuilder='dom')
h2list = dom.getElementsByTagName('h2')
try:
    val = h2list[1].childNodes[0].nodeValue[46:]
    if ':)' not in val:
        val += '.'
except IndexError:
    val = 'Pound is currently open!'
embed = discord.Embed(title='Time', description=val, colour=0x4ba139)
await client.say(embed=embed)



link = 'http://www.chickensmoothie.com/pound.php'
soup = BeautifulSoup(urllib.request.urlopen(link).read(), 'lxml', parse_only=SoupStrainer('h2'))
pound_time = soup.find(True, 'width_limit').text.replace('\t', '').replace('\n', '').replace('Sorry, the pound is closed at the moment.','')
if pound_time is None:
	pound_time = 'The pound is currently open!'
elif ':)' not in pound_time:
	pound_time += '.'
# embed = discord.Embed(title='Time', description=pound_time, colour=0x4ba139)
# await client.say(embed=embed)
values = [int(s) for s in str.split() if s.isdigit()]
