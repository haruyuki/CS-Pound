import io
import math
import re
from urllib.parse import urlparse, parse_qs, parse_qsl

import aiohttp
import discord
import lxml.html
from PIL import Image, ImageFont, ImageDraw

from constants import Constants


async def _get_web_data(link):  # Get web data from link
    success = False
    dom = ''
    connection = ''

    if 'static' in link:
        return success

    headers = {  # HTTP request headers
        'User-Agent': 'CS Pound Discord Bot Agent ' + Constants.version,  # Connecting User-Agent
        'From': 'jumpy12359@gmail.com'  # Contact email
    }
    parameters = {}
    components = urlparse(link)
    if components.query:
        parameters = dict(parse_qsl(components.query, keep_blank_values=True))

    base_link = f'{components.scheme}://{components.hostname}{components.path}'
    async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
        async with session.post(base_link, data=parameters, headers=headers) as response:  # POST the variables to the base php link
            if response.status == 200:
                success = True
                connection = await response.text()  # Request HTML page data
                dom = lxml.html.fromstring(connection)  # Extract HTML from site
    return success, dom, connection  # Return whether connection was successful and DOM data


async def pet(link):
    def key_process(string):
        string = string.lower()
        replacements = {
            ':': '',
            'pet ': '',
            'pet\'s ': '',
            '\t': '',
            '\n': ''
        }

        substrs = sorted(replacements, key=len, reverse=True)
        regexp = re.compile('|'.join(map(re.escape, substrs)))

        return regexp.sub(lambda match: replacements[match.group(0)], string)

    data = await _get_web_data(link)
    if data[0]:
        pet_data = {
            'pps': False,
            'image': '',
            'owner': '',
            'owner_link': '',
            'id': 0,
            'name': '',
            'adopted': '',
            'age': 0,
            'growth': '',
            'rarity': '',
            'given': '',
            'given_link': ''
        }

        table = data[1].xpath('//table[@class="spine"]/tr')
        for i in range(len(table)):
            if i == 0:
                pet_data['image'] = table[i].xpath('td/img/@src')[0]

            else:
                value = ''
                key = key_process(table[i].xpath('td[1]/text()')[0])
                if i == 1:
                    if 'PPS' in data[2]:
                        pet_data['pps'] = True
                        i += 1
                    value = table[i].xpath('td[2]/a/text()')[0]
                    link = 'https://www.chickensmoothie.com/' + table[i].xpath('td[2]/a/@href')[0]
                    pet_data['owner_link'] = link
                elif len(table) - i == 2 or len(table) - i == 1:
                    if key == 'rarity':
                        value = table[i].xpath('td[2]/img/@alt')[0]
                    if 'given' in key:
                        key = 'given'
                        value = table[i].xpath('td[2]/a/text()')[0]
                        pet_data[key] = value
                        key = 'given_link'
                        value = 'https://www.chickensmoothie.com/' + table[i].xpath('td[2]/a/@href')[0]
                else:
                    value = table[i].xpath('td[2]/text()')[0]
                    if key == 'owner':
                        value = table[i].xpath('td[2]/a/text()')[0]
                    elif key == 'id':
                        value = int(value)
                    elif key == 'age':
                        value = int(value[:-5])
                pet_data[key] = value
        return pet_data

    else:
        return None


async def image(link):
    data = await _get_web_data(link)
    if data[0]:
        information = {}
        titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
        values = data[1].xpath('//td[@class="r"]')  # Values of pet information

        pet_image = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
        if 'trans' in pet_image:  # If pet image is transparent (i.e. Pet has items)
            pet_image = 'http://www.chickensmoothie.com' + pet_image  # Pet image link
            transparent = True
            rgba = (225, 246, 179, 255)
        else:
            hex_colour = parse_qs(pet_image)['bg'][0]
            rgb = [int(hex_colour[i:i + 2], 16) for i in (0, 2, 4)]
            rgb.append(255)
            rgba = tuple(rgb)
            transparent = False

        if titles[0] == 'PPS':  # If pet is PPS
            pps = True
        else:  # If pet is not PPS
            pps = False

        if len(titles) + len(values) < 16:  # If the amount of titles and values don't add up
            no_name = True
        else:  # If they add up
            no_name = False

        if no_name:  # If pet has no name
            case1 = 'Pet\'s name:'
            case2 = 'Adopted:'
            if pps:  # If pet has no name and is PPS
                case1 = 'Pet\'s name:'
                case2 = 'Pet ID:'
        elif pps:  # If pet has a name and is PPS
            case1 = 'Pet ID:'
            case2 = 'Pet\'s name:'
        else:  # If pet has a name but is not PPS
            case1 = 'Pet\'s name:'
            case2 = 'Adopted:'

        temp = len(titles) - 1 if pps else len(titles)  # Is pet is PPS, remove one title, else all titles
        for i in range(temp):  # For each title in titles
            if titles[i] == case1:
                information['Name'] = values[i].xpath('text()')[0]  # Add pet name to information dictionary
            elif titles[i] == case2:
                information['Adopted'] = values[i].xpath('text()')[0]  # Add pet adoption date to information dictionary
            elif titles[i] == ('Growth:' if pps else 'Rarity:'):  # If pet is PPS, if titles[i] matches 'Growth:', otherwise if not PPS, if titles[i] matches with 'Rarity:'
                information['Rarity'] = 'rarities/' + values[i].xpath('img/@src')[0][12:]  # Local link to rarity image

        async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
            async with session.get(pet_image) as response:  # GET HTTP response of pet image link
                connection = await response.read()  # Read the response content
                pet_image = io.BytesIO(connection)  # Convert the content into bytes

        image_files = [pet_image, information['Rarity']]
        font = ImageFont.truetype('Verdana.ttf', 12)  # Verdana font size 15

        images = map(Image.open, image_files)  # Map the image files
        widths, heights = zip(*(i.size for i in images))  # Tuple of widths and heights of both images
        images = list(map(Image.open, image_files))  # List of image file name

        temp_draw = ImageDraw.Draw(Image.new('RGBA', (0, 0)))  # Temporary drawing canvas to calculate text sizes
        max_width = max(widths)  # Max width of images
        total_height = sum(heights) + (15 * len(information))  # Total height of images
        current_width = 0

        for key, value in information.items():  # For each item in information
            if 'rarities/' in value:
                temp_width = 106
            else:
                temp_width = temp_draw.textsize(value, font=font)[0]  # Width of text

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

        try:
            draw.text((math.floor(((max_width - math.floor(draw.textsize(information['Name'], font=font)[0])) / 2)), y_offset), information['Name'], fill=(0, 0, 0), font=font)  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
            y_offset += 15  # Add offset of 15
        except KeyError:
            pass

        try:
            draw.text((math.floor(((max_width - math.floor(draw.textsize(information['Adopted'], font=font)[0])) / 2)), y_offset), information['Adopted'], fill=(0, 0, 0), font=font)  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
            y_offset += 15  # Add offset of 15
        except KeyError:
            pass

        canvas.paste(images[1], (math.floor((max_width - images[1].size[0]) / 2), y_offset), images[1])  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[1]

        output_buffer = io.BytesIO()  # Convert the PIL output into bytes
        canvas.save(output_buffer, 'png')  # Save the bytes as a PNG format
        output_buffer.seek(0)  # Move the 'cursor' back to the start

        return output_buffer
    else:
        embed = discord.Embed(title="Image", description="That is not a valid pet link!", colour=0xff5252)
        return embed


async def pound_text():
    data = await _get_web_data('https://www.chickensmoothie.com/pound.php')  # Get web data
    if data[0]:  # If the data is valid
        text = data[1].xpath('//h2/text()')  # Get all H2 elements in the data
        try:
            text = text[1]  # Try and get pound opening text
            text = text.replace('Sorry, the pound is closed at the moment.', '').replace('\n', '').replace('\t', '') + '.'  # Remove extra formatting from text
        except IndexError:  # If there isn't any pound opening text
            text = 'Pound is currently open!'

        return text
    else:
        return None
