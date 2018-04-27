import urllib.request
import html5lib
import lxml.html

url = 

connection = urllib.request.urlopen('http://www.chickensmoothie.com/pound.php')
dom = lxml.html.fromstring(connection.read())
text = dom.xpath('//h2/text()')
output = ''

try:
    if ':)' in text:
        output = text[1][:-85].replace('\n', r'').replace('\t', r'') + ' The pound opens at totally random times of day, so check back later to try again :)'
    else:
        output = text[1].replace('Sorry, the pound is closed at the moment.', '').replace('\n', r'').replace('\t', r'') + '.'
except IndexError:
    output = 'Pound is currently open!'

embed = discord.Embed(title='Time', description=val, colour=0x4ba139)
await client.say(embed=embed)