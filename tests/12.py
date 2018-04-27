import urllib.request
import html5lib
import lxml.html

url = 'http://www.chickensmoothie.com/viewpet.php?id=258399994'

connection = urllib.request.urlopen(url)
dom = lxml.html.fromstring(connection.read())

petimg = dom.xpath('//img[@id="petimg"]/@src')[0]
titles = dom.xpath('//td[@class="l"]/text()')
values = dom.xpath('//td[@class="r"]/text()') 
tables = len(titles)
given = True
value_list = []

embed = discord.Embed(title='Pet', colour=0x4ba139)
embed.set_image(url=petimg)
for i in range(tables):
    title_list.append(titles[i].string.replace('\t', '').replace('\n', ''))
    if i == 0:
        value_list.append('[' + dom.xpath('//td[@class="r"]/a/text()')[0] + ']' + '(' + 'http://www.chickensmoothie.com/' + dom.xpath('//td[@class="r"]/a/@href')[0] + ')')
    elif len(values) - i == 2 or len(values) - i == 1:
        if title_list[i] == 'Growth:' or not given:
            given = False
            if len(values) - i == 2:
                value_list.append(dom.xpath('//td[@class="r"]')[i].xpath('text()')[0])
            elif len(values) - i == 1:
                value_list.append(dom.xpath('//td[@class="r"]')[i].xpath('img/@alt'))
        elif title_list[i] == 'Rarity:' or given:
            given = True
            if len(values) - i == 2:
                value_list.append(dom.xpath('//td[@class="r"]')[i].xpath('img/@alt'))
            elif len(values) - i == 1:
                value_list.append('[' + dom.xpath('//td[@class="r"]/a/text()')[1] + ']' + '(' + 'http://www.chickensmoothie.com/' + dom.xpath('//td[@class="r"]/a/@href')[1] + ')')
    else:
        value_list.append(dom.xpath('//td[@class="r"]')[i].xpath('text()')[0])

    if i == 0:
        embed.add_field(name=title_list[i], value=value_list[i], inline=False)
    else:
        embed.add_field(name=title_list[i], value=value_list[i], inline=True)

await client.say(embed=embed)
