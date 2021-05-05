import argparse
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

    exceptions = {'3B46301A6C8B850D87A730DA365B0960', 'E5FEFE44A3070BC9FC176503EC1A603F', '0C1AFF9AEAA0953F1B1F9B818C2771C9', '7C912BA5616D2E24E9F700D90E4BA2B6', '905BB7DE4BC4E29D7FD2D1969667B568', '773B14EEB416FA762C443D909FFED344', '1C0DB4785FC78DF4395263D40261C614', '5066110701B0AE95948A158F0B262EBB', '5651A6C10C4D375A1901142C49C5C70C', '8BED72498D055E55ABCA7AD29B180BF4'}

    parse_link = f'https://www.chickensmoothie.com/archive/{year}/'
    print(f'Parsing: "{parse_link}"')

    response = requests.get(parse_link)
    dom = lxml.html.fromstring(response.text)
    event_links = dom.xpath('//li[@class="event active"]/a/@href') + dom.xpath('//li[@class="event "]/a/@href')  # Get the links to all the monthlies and special pets

    for event in event_links:  # For each event
        event = quote(event)
        base_link = f'https://www.chickensmoothie.com{event}'  # The link to the event archive
        response = requests.get(base_link)  # Get the HTML
        dom = lxml.html.fromstring(response.text)

        event_title = unquote(event[14:-1])
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
                current_page = page * 7
                link = f'{base_link}?pageStart={current_page}'
                response = requests.get(link)
                dom = lxml.html.fromstring(response.text)
            print(f'Finding pets from "{link}" page')

            image_links = dom.xpath('//img[@alt="Pet"]/@src')

            pet_ids = set()
            for image_link in image_links:
                components = urlparse(image_link)
                parameters = dict(parse_qsl(components.query))
                if parameters['k'] not in exceptions:
                    pet_ids.add(parameters['k'])

            conn = create_connection('cs_archive.sqlite3')
            c = conn.cursor()
            counter = 0
            for pet_id in pet_ids:
                try:
                    c.execute('INSERT INTO ChickenSmoothie_Archive (Pet_ID, Year, Event, Archive_Link) VALUES (?, ?, ?, ?)', (pet_id, year, event_title, link))
                    counter += 1
                except sqlite3.IntegrityError:
                    print(f'WARNING: Pet ID {pet_id} already exists in database.')

            print(f'Inserted {counter} row(s)')

            conn.commit()
            conn.close()
        print('\n')

    conn = create_connection('cs_archive.sqlite3')
    c = conn.cursor()
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/Valentine%27s%20Day/', f'https://www.chickensmoothie.com/archive/{year}/Valentine%2527s%20Day/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/Valentine%27s/', f'https://www.chickensmoothie.com/archive/{year}/Valentine%2527s/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/St.%20Patrick%27s%20Day/', f'https://www.chickensmoothie.com/archive/{year}/St.%20Patrick%2527s%20Day/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Archive_Link=? WHERE Archive_Link=?', (f'https://www.chickensmoothie.com/archive/{year}/April%20Fool%27s/', f'https://www.chickensmoothie.com/archive/{year}/April%20Fool%2527s/'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("Valentine's Day", 'Valentine%27s Day'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("Valentine's", 'Valentine%27s'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("St. Patrick's Day", 'St. Patrick%27s Day'))
    c.execute('UPDATE ChickenSmoothie_Archive SET Event=? WHERE Event=?', ("April Fool's", 'April Fool%27s'))
    conn.commit()
    conn.close()
