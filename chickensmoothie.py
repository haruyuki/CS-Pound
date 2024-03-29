import io
import math
import textwrap
from urllib.parse import urlparse, parse_qs, parse_qsl

import aiohttp
import lxml.html
from PIL import Image, ImageFont, ImageDraw

from classes.pet import Pet
from constants import Constants
import library


async def _get_web_data(link):  # Get web data from link
    success = False
    dom = None

    if "static" in link:  # If user provided direct link to pet image
        return success

    headers = {  # HTTP request headers
        "User-Agent": "CS Pound Discord Bot Agent "
        + Constants.version,  # Connecting User-Agent
        "From": Constants.contact_email,
    }
    parameters = {}
    components = urlparse(link)
    if components.query:
        parameters = dict(parse_qsl(components.query, keep_blank_values=True))

    base_link = f"{components.scheme}://{components.hostname}{components.path}"
    async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
        async with session.post(
            base_link, data=parameters, headers=headers
        ) as response:  # POST the variables to the base php link
            if response.status == 200:  # If received response is OK
                success = True
                connection = await response.text()  # Get text HTML of site
                dom = lxml.html.fromstring(connection)  # Convert into DOM
                dom.make_links_absolute("https://www.chickensmoothie.com")
    return success, dom


async def pet(link):
    data = await _get_web_data(link)
    if data[0]:
        return Pet(data[1])
    else:
        return None


async def image(link):
    pet_class = await pet(link)
    if pet_class is not None:
        information = {
            "name": pet_class.name,
            "adopted": pet_class.adoption_date,
            "rarity_link": pet_class.rarity_link(),
        }

        if (
            "trans" in pet_class.image_url
        ):  # If pet image is transparent (i.e. Pet has items)
            transparent = True
            rgba = (225, 246, 179, 255)
        else:
            hex_colour = parse_qs(pet_class.image_url)["bg"][0]
            rgb = [int(hex_colour[i : i + 2], 16) for i in (0, 2, 4)]
            rgb.append(255)
            rgba = tuple(rgb)
            transparent = False

        async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
            async with session.get(
                pet_class.image_url
            ) as response:  # GET HTTP response of pet image link
                connection = await response.read()  # Read the response content
                pet_image = io.BytesIO(connection)  # Convert the content into bytes

        image_files = [pet_image, information["rarity_link"]]
        font = ImageFont.truetype("Verdana.ttf", 12)  # Verdana font size 15

        images = map(Image.open, image_files)  # Map the image files
        widths, heights = zip(
            *(i.size for i in images)
        )  # Tuple of widths and heights of both images
        images = list(map(Image.open, image_files))  # List of image file name

        temp_draw = ImageDraw.Draw(
            Image.new("RGBA", (0, 0))
        )  # Temporary drawing canvas to calculate text sizes
        max_width = max(widths)  # Max width of images
        total_height = sum(heights) + (15 * len(information))  # Total height of images
        current_width = 0

        for _, value in information.items():  # For each item in information
            try:
                if "rarities/" in value:
                    temp_width = 106
                else:
                    temp_width = temp_draw.textsize(value, font=font)[
                        0
                    ]  # Width of text
            except TypeError:
                continue

            if (
                current_width < temp_width
            ):  # If current width is less than width of texts
                current_width = temp_width

        if max_width < current_width:
            max_width = current_width * 2

        canvas = Image.new(
            "RGBA", (max_width, total_height), rgba
        )  # Create an RGBA image of max_width x total_height
        draw = ImageDraw.Draw(canvas)  # Draw the image to PIL

        y_offset = 0  # Offset for vertically stacking images
        if transparent:  # If pet has items
            canvas.paste(
                images[0],
                (math.floor((max_width - images[0].size[0]) / 2), y_offset),
                images[0],
            )  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[0]
        else:  # If pet doesn't have items
            canvas.paste(
                images[0], (math.floor((max_width - images[0].size[0]) / 2), y_offset)
            )  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2)
        y_offset += images[0].size[1]  # Add height of image + 10 to offset

        if information["name"]:
            draw.text(
                (
                    math.floor(
                        (
                            (
                                max_width
                                - math.floor(
                                    draw.textsize(information["name"], font=font)[0]
                                )
                            )
                            / 2
                        )
                    ),
                    y_offset,
                ),
                information["name"],
                fill=(0, 0, 0),
                font=font,
            )  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
            y_offset += 15  # Add offset of 15

        draw.text(
            (
                math.floor(
                    (
                        (
                            max_width
                            - math.floor(
                                draw.textsize(information["adopted"], font=font)[0]
                            )
                        )
                        / 2
                    )
                ),
                y_offset,
            ),
            information["adopted"],
            fill=(0, 0, 0),
            font=font,
        )  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
        y_offset += 15  # Add offset of 15

        canvas.paste(
            images[1],
            (math.floor((max_width - images[1].size[0]) / 2), y_offset),
            images[1],
        )  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[1]

        output_buffer = io.BytesIO()  # Convert the PIL output into bytes
        canvas.save(output_buffer, "png")  # Save the bytes as a PNG format
        output_buffer.seek(0)  # Move the 'cursor' back to the start

        return output_buffer
    else:
        return None


async def get_pound_string():
    data = await _get_web_data(
        "https://www.chickensmoothie.com/poundandlostandfound.php"
    )  # Get web data
    if data[0]:  # If the data is valid
        text = data[1].xpath("//h2/text()")  # Get all H2 elements in the data
        if text[0] == "Pound & Lost and Found":
            pound_type = text[0]
            text = f"Sorry, both the {pound_type} are closed at the moment."
        else:
            pound_type = text[0][4:]
            try:
                text = (
                    library.multi_replace(
                        text[1],
                        {
                            "Sorry, the pound is closed at the moment.": "",
                            "Sorry, the Lost and Found is closed at the moment.": "",
                            "\n": "",
                            "\t": "",
                        },
                    )
                    + "."
                )  # Get opening text and remove extra formatting
            except IndexError:  # If there isn't any pound opening text
                text = f"""\
                {pound_type} is currently open!
                [Go {"claim an item" if pound_type == "Lost and Found" else "adopt a pet"} from the {pound_type}!](https://www.chickensmoothie.com/poundandlostandfound.php)"""
                text = textwrap.dedent(text)

        return pound_type, text


def get_pound_time(string):
    to_parse = ""
    times = [n for n in string.split() if n.isdigit()]  # Extract numbers from string
    if times:  # If numbers in string
        if "hour" in string:
            hours = times[0]
            to_parse = f"{hours}h"

        if "minute" in string:
            try:  # Assume string contains hours and minutes
                minutes = times[1]
            except IndexError:  # Otherwise minute only
                minutes = times[0]
            to_parse += f"{minutes}m"

    sleep_amount = library.parse_time(to_parse)
    return sleep_amount


async def get_announcements():
    data = await _get_web_data("https://www.chickensmoothie.com/news/news.php")
    if data[0]:
        news_articles = data[1].xpath('//div[@class="newsitem"]')
        for article in news_articles:
            index = news_articles.index(article)
            news_articles[index] = article.xpath('div[@class="newscontent"]/p')[0]
        return news_articles
