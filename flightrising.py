import re

import aiohttp
import lxml.html

from constants import Constants


async def _get_web_data(link):  # Get web data from link
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
