import io
import math
import re
import textwrap
from urllib.parse import urlparse, parse_qs, parse_qsl

import aiohttp
import lxml.html
from PIL import Image, ImageFont, ImageDraw

from classes.pet import Pet
from constants import Constants, Strings
import library


async def _get_web_data(link):  # Get web data from link
    success = False
    dom = None

    if 'static' in link:  # If user provided direct link to pet image
        return success

    headers = {  # HTTP request headers
        'User-Agent': 'CS Pound Discord Bot Agent ' + Constants.version,  # Connecting User-Agent
        'From':  Constants.contact_email
    }
    parameters = {}
    components = urlparse(link)
    if components.query:
        parameters = dict(parse_qsl(components.query, keep_blank_values=True))

    base_link = f'{components.scheme}://{components.hostname}{components.path}'
    async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
        async with session.post(base_link, data=parameters, headers=headers) as response:  # POST the variables to the base php link
            if response.status == 200:  # If received response is OK
                success = True
                connection = await response.text()  # Get text HTML of site
                dom = lxml.html.fromstring(connection)  # Convert into DOM
    return success, dom


async def pet(link):
    pet_class = Pet()

    def key_process(string):
        string = string.lower()
        replacements = {
            ':': '',
            'pet ': '',
            'pet\'s ': '',
            '\t': '',
            '\n': ''
        }

        sub_strings = sorted(replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, sub_strings)))

        return regexp.sub(lambda match: replacements[match.group(0)], string)

    data = await _get_web_data(link)
    if data[0]:
        pet_data = {
            'pps': False,
            'store_pet': False,
            'image': '',
            'owner': '',
            'owner_link': '',
            'id': 0,
            'name': None,
            'adopted': '',
            'age': 0,
            'growth': '',
            'rarity': '',
            'given': None,
            'given_link': None
        }

        table = data[1].xpath('//table[@class="spine"]/tr')
        keys = []
        for element in table:
            temp = element.xpath('td[1]/text()')
            if temp:
                keys.append(temp[0])
        keys = ' '.join(keys)

        for index, row in enumerate(table):
            if index == 0:
                pet_data['image'] = row.xpath('td/img/@src')[0]
                if 'trans' in pet_data['image']:
                    pet_data['image'] = 'https://www.chickensmoothie.com' + pet_data['image']

            else:
                value = ''
                key = key_process(row.xpath('td[1]/text()')[0])
                if index == 1:
                    if 'PPS' in keys:
                        index += 1
                    if 'Store' in keys:
                        index += 1
                    value = table[index].xpath('td[2]/a/text()')[0]
                    link = 'https://www.chickensmoothie.com/' + table[index].xpath('td[2]/a/@href')[0]
                    pet_data['owner_link'] = link

                elif len(table) - index == 2 or len(table) - index == 1:
                    if key == 'rarity':
                        value = row.xpath('td[2]/img/@alt')[0]
                    if key == 'growth':
                        value = row.xpath('td[2]/text()')[0]
                    if 'given' in key:
                        key = 'given'
                        value = row.xpath('td[2]/a/text()')[0]
                        pet_data[key] = value
                        key = 'given_link'
                        value = 'https://www.chickensmoothie.com/' + row.xpath('td[2]/a/@href')[0]
                else:
                    if index == 2 and 'Store' in keys:
                        continue
                    value = row.xpath('td[2]/text()')[0]
                    if key == 'owner':
                        value = row.xpath('td[2]/a/text()')[0]
                    elif key == 'id':
                        value = int(value)
                    elif key == 'age':
                        try:
                            value = int(re.findall(r'(\d*) days?', value)[0])  # Extract the age number
                        except (ValueError, IndexError):  # If no number found (i.e Pet is less than a day old)
                            value = 0

                pet_data[key] = value
        if 'PPS' in keys:
            pet_data['pps'] = True
        if 'Store' in keys:
            pet_data['store_pet'] = True

        pet_class.pps = pet_data['pps']
        pet_class.store_pet = pet_data['store_pet']
        pet_class.image = pet_data['image']
        pet_class.owner_name = pet_data['owner']
        pet_class.owner_link = pet_data['owner_link']
        pet_class.id = pet_data['id']
        pet_class.name = pet_data['name']
        pet_class.adoption_date = pet_data['adopted']
        pet_class.age = pet_data['age']
        pet_class.growth = pet_data['growth']
        pet_class.rarity = pet_data['rarity']
        pet_class.given_name = pet_data['given']
        pet_class.given_url = pet_data['given_link']

        return pet_class

    else:
        return None


async def image(link):
    pet_class = await pet(link)
    if pet_class is not None:
        information = {
            'name': pet_class.name,
            'adopted': pet_class.adoption_date,
            'rarity_link': pet_class.rarity_link()
        }

        if 'trans' in pet_class.image:  # If pet image is transparent (i.e. Pet has items)
            transparent = True
            rgba = (225, 246, 179, 255)
        else:
            hex_colour = parse_qs(pet_class.image)['bg'][0]
            rgb = [int(hex_colour[i:i + 2], 16) for i in (0, 2, 4)]
            rgb.append(255)
            rgba = tuple(rgb)
            transparent = False

        async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
            async with session.get(pet_class.image) as response:  # GET HTTP response of pet image link
                connection = await response.read()  # Read the response content
                pet_image = io.BytesIO(connection)  # Convert the content into bytes

        image_files = [pet_image, information['rarity_link']]
        font = ImageFont.truetype('Verdana.ttf', 12)  # Verdana font size 15

        images = map(Image.open, image_files)  # Map the image files
        widths, heights = zip(*(i.size for i in images))  # Tuple of widths and heights of both images
        images = list(map(Image.open, image_files))  # List of image file name

        temp_draw = ImageDraw.Draw(Image.new('RGBA', (0, 0)))  # Temporary drawing canvas to calculate text sizes
        max_width = max(widths)  # Max width of images
        total_height = sum(heights) + (15 * len(information))  # Total height of images
        current_width = 0

        for _, value in information.items():  # For each item in information
            try:
                if 'rarities/' in value:
                    temp_width = 106
                else:
                    temp_width = temp_draw.textsize(value, font=font)[0]  # Width of text
            except TypeError:
                continue

            if current_width < temp_width:  # If current width is less than width of texts
                current_width = temp_width

        if max_width < current_width:
            max_width = current_width * 2

        canvas = Image.new('RGBA', (max_width, total_height), rgba)  # Create an RGBA image of max_width x total_height
        draw = ImageDraw.Draw(canvas)  # Draw the image to PIL

        y_offset = 0  # Offset for vertically stacking images
        if transparent:  # If pet has items
            canvas.paste(images[0], (math.floor((max_width - images[0].size[0]) / 2), y_offset), images[0])  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[0]
        else:  # If pet doesn't have items
            canvas.paste(images[0], (math.floor((max_width - images[0].size[0]) / 2), y_offset))  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2)
        y_offset += images[0].size[1]  # Add height of image + 10 to offset

        if information['name']:
            draw.text((math.floor(((max_width - math.floor(draw.textsize(information['name'], font=font)[0])) / 2)), y_offset), information['name'], fill=(0, 0, 0), font=font)  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
            y_offset += 15  # Add offset of 15

        draw.text((math.floor(((max_width - math.floor(draw.textsize(information['adopted'], font=font)[0])) / 2)), y_offset), information['adopted'], fill=(0, 0, 0), font=font)  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
        y_offset += 15  # Add offset of 15

        canvas.paste(images[1], (math.floor((max_width - images[1].size[0]) / 2), y_offset), images[1])  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[1]

        output_buffer = io.BytesIO()  # Convert the PIL output into bytes
        canvas.save(output_buffer, 'png')  # Save the bytes as a PNG format
        output_buffer.seek(0)  # Move the 'cursor' back to the start

        return output_buffer
    else:
        return None


async def get_pound_string():
    data = await _get_web_data('https://www.chickensmoothie.com/poundandlostandfound.php')  # Get web data
    if data[0]:  # If the data is valid
        text = data[1].xpath('//h2/text()')  # Get all H2 elements in the data
        if text[0] == "Pound & Lost and Found":
            pound_type = text[0]
            text = f'Sorry, both the {pound_type} is closed at the moment.'
        else:
            pound_type = text[0][4:]
            try:
                text = text[1]  # Try and get pound opening text
                text = text.replace(f'Sorry, the {pound_type} is closed at the moment.', '').replace('\n', '').replace('\t', '') + '.'  # Remove extra formatting from text
            except IndexError:  # If there isn't any pound opening text
                text = f'''\
                {pound_type} is currently open!
                [Go {"claim an item" if pound_type == "Lost and Found" else "adopt a pet"} from the {pound_type} now!]((https://www.chickensmoothie.com/poundandlostandfound.php))'''
                text = textwrap.dedent(text)

        return pound_type, text


def get_pound_time(string):
    to_parse = ''
    times = [n for n in string.split() if n.isdigit()]  # Extract numbers from string
    if times:  # If numbers in string
        if 'hour' in string:
            hours = times[0]
            to_parse = f'{hours}h'

        if 'minute' in string:
            try:  # Assume string contains hours and minutes
                minutes = times[1]
            except IndexError:  # Otherwise minute only
                minutes = times[0]
            to_parse += f'{minutes}m'

    sleep_amount = library.parse_time(to_parse)
    return sleep_amount


async def get_announcements():
    data = await _get_web_data('https://www.chickensmoothie.com/news/news.php')
    if data[0]:
        news_articles = data[1].xpath('//div[@class="newsitem"]')
        for article in news_articles:
            index = news_articles.index(article)
            news_articles[index] = article.xpath('div[@class="newscontent"]/p')[0]
        return news_articles
