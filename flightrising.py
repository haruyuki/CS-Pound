import re
from urllib.parse import urlparse, parse_qsl, urlencode

import aiohttp
import lxml.html

from constants import Constants, FlightRisingC


async def _get_web_data(link: str):  # Get web data from link
    success = False
    dom = None

    headers = {  # HTTP request headers
        'User-Agent': 'CS Pound Discord Bot Agent ' + Constants.version,  # Connecting User-Agent
        'From':  Constants.contact_email
    }

    async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
        async with session.get(link, headers=headers) as response:  # POST the variables to the base php link
            if response.status == 200:  # If received response is OK
                success = True
                connection = await response.text()  # Get text HTML of site
                connection = re.sub(r'\t', '', connection)
                connection = re.sub(r'\n', '', connection)
                connection = re.sub(r'\r', '', connection)
                connection = re.sub(r'<script[\s\S]*?>[\s\S]*?<\/script>', '', connection)
                connection = re.sub(r'<style[\s\S]*?>[\s\S]*?<\/style>', '', connection)
                dom = lxml.html.fromstring(connection)  # Convert into DOM
                dom.make_links_absolute('http://flightrising.com')
    return success, dom


def extract_dragon_id(link):
    components = urlparse(link)
    if components.query:
        parameters = dict(parse_qsl(components.query, keep_blank_values=True))
    else:
        return None

    dragon_id = parameters['did']
    return dragon_id


async def get_progeny(dragon_id1, dragon_id2, multiplier):
    parameters = {'id1': dragon_id1, 'id2': dragon_id2}
    link = FlightRisingC.progeny_url + '?' + urlencode(parameters)

    outcomes = []
    for i in range(multiplier):
        data = await _get_web_data(link)
        if data[0]:
            image_links = data[1].xpath('//img/@src')
            outcomes.extend(image_links)
        else:
            pass

    return outcomes
