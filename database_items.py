import argparse
import re
import sqlite3
from urllib.parse import urlparse, parse_qsl, unquote, quote

import lxml.html
import requests


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Exception as e:
        print(e)

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', help='Year to be processed', default='2008')  # Defaults to the oldest year
    args = parser.parse_args()

    if args.year:
        year = args.year

    parse_link = f'https://www.chickensmoothie.com/archive/{year}/Items/'
    print(f'Parsing: "{parse_link}"')

    response = requests.get(parse_link)
    dom = lxml.html.fromstring(response.text)
    event_links = dom.xpath('//li[@class="event active"]/a/@href') + dom.xpath('//li[@class="event "]/a/@href')  # Get the links to all the monthlies and special pets

    for event in event_links:  # For each event
        event = quote(event)
        base_link = f'https://www.chickensmoothie.com{event}'  # The link to the event archive
        response = requests.get(base_link)  # Get the HTML
        dom = lxml.html.fromstring(response.text)

        event_title = unquote(event[14:-7])
        print(f'Finding pets from {event_title} Event')

        if len(dom.xpath('//div[@class="pages"]')) == 0:  # If there is only the current page
            pages = 1
        else:  # If there are other pages of pets
            pages = len(dom.xpath('//div[@class="pages"][1]/a'))  # Get the number of pages
        print(f'{pages} page(s) found')

        for page in range(pages):  # For each page
            if page == 0:
                link = base_link
            else:
                current_page = page * 10
                link = f'{base_link}?pageStart={current_page}'
                response = requests.get(link)
                dom = lxml.html.fromstring(response.text)
            print(f'Finding items from "{link}" page')

            image_links = dom.xpath('//img[@alt="item"]/@src')

            item_ids = set()
            for image_link in image_links:
                components = urlparse(image_link)
                path = components.path[6:].split('&')
                left = int(path[0])
                right = [int(s) for s in re.findall(r'\b\d+\b', path[1])][0]
                item_ids.add((left, right))

            conn = create_connection('cs_item_archive.sqlite3')
            c = conn.cursor()
            counter = 0
            for item_id in item_ids:
                try:
                    c.execute('INSERT INTO ChickenSmoothie_Archive (ItemL_ID, ItemR_ID, Year, Event, Archive_Link) VALUES (?, ?, ?, ?, ?)', (item_id[0], item_id[1], year, event_title, link))
                    counter += 1
                except sqlite3.IntegrityError:
                    print(f'WARNING: Item ID combination {item_id} already exists in database.')

            print(f'Inserted {counter} row(s)')

            conn.commit()
            conn.close()
        print('\n')

    conn = create_connection('cs_item_archive.sqlite3')
    c = conn.cursor()
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/Valentine%27s%20Day/Items/', f'https://www.chickensmoothie.com/archive/{year}/Valentine%2527s%20Day/Items/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/Valentine%27s/Items/', f'https://www.chickensmoothie.com/archive/{year}/Valentine%2527s/Items/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/April%20Fool%27s/Items/', f'https://www.chickensmoothie.com/archive/{year}/April%20Fool%2527s/Items/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/St.%20Patrick%27s%20Day/Items/', f'https://www.chickensmoothie.com/archive/{year}/St.%20Patrick%2527s%20Day/Items/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("April Fool's", 'April Fool%27s'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("Valentine's Day", 'Valentine%27s Day'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("Valentine's", 'Valentine%27s'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("St. Patrick's Day", 'St. Patrick%27s Day'))
    conn.commit()
    conn.close()
