import asyncio
import base64
import datetime
import io
import math

import aiohttp
import discord
from discord.ext import commands
import lxml.html
import motor.motor_asyncio as amotor
from PIL import Image, ImageFont, ImageDraw
from urllib.parse import urlparse, parse_qs

import chickensmoothie as cs
from constants import Constants

mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client[Constants.database_name]
collection = database[Constants.other_collection_name]


class PoundPets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.generating_image = False
        self.all_rare_pets = 0
        self.parsed_pets = 0
        self.stage = 1

    @commands.group(aliases=['ppets', 'pound-pets'])
    @commands.guild_only()
    async def pound_pets(self, ctx):
        if ctx.invoked_subcommand is None:
            if Constants.image_exists:
                cursor = collection.find({'generated': True})  # Try to get document of generated image
                document = await cursor.to_list(length=1)
                document = document[0]
                base64_string = base64.b64decode(document['image_base64'])
                output_buffer = io.BytesIO(base64_string)
                await ctx.send(file=discord.File(fp=output_buffer, filename='poundpets.png'))
            else:
                await ctx.send('No image has been generated yet! Type `,ppets get` to start generating')

    @pound_pets.command(aliases=['generate', 'gen'])
    @commands.guild_only()
    async def get(self, ctx):
        if not self.generating_image:
            pound_data = await cs.get_pound_string()
            if pound_data[0] == 'Lost and Found' or pound_data[0] == 'Pound & Lost and Found':
                await ctx.send('The next opening is not the Pound!')

            elif pound_data[0] == 'Pound' and 'Pound is currently open!' in pound_data[1]:
                await ctx.send('An image cannot be generated while the pound is still open!')

            elif Constants.image_exists:
                await ctx.send('An image has already been created! Use `,ppets` to display it!')

            else:
                await ctx.send('Generating image... Enter the command again to view the progress')
                self.generating_image = True
                headers = {  # HTTP request headers
                    'User-Agent': 'CS Pound Discord Bot Agent ' + Constants.version,  # Connecting User-Agent
                    'From': Constants.contact_email
                }
                login_url = 'https://www.chickensmoothie.com/Forum/ucp.php?mode=login'
                payload = {
                    'username': Constants.username,
                    'password': Constants.password,
                    'redirect': 'index.php',
                    'sid': '',
                    'login': 'Login'
                }

                self.session = aiohttp.ClientSession(headers=headers)
                await self.session.post(login_url, data=payload)

                pound_account = Constants.pound_pets_group
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(pound_account) as response:
                        if response.status == 200:
                            connection = await response.text()
                            dom = lxml.html.fromstring(connection)
                            dom.make_links_absolute('https://www.chickensmoothie.com')

                self.stage = 1
                last_page = dom.xpath('//div[@class="pages"]')[0].xpath('a/@href')[-2]
                pet_count = int(parse_qs(urlparse(last_page).query)['pageStart'][0])
                all_pets = []

                for i in range(30):
                    page_start = pet_count - (20 * i)
                    url = pound_account + '&pageStart=' + str(page_start)
                    async with self.session.get(url) as response:  # POST the variables to the base php link
                        if response.status == 200:  # If received response is OK
                            connection = await response.text()  # Get text HTML of site
                            await asyncio.sleep(0.5)
                            dom = lxml.html.fromstring(connection)  # Convert into DOM
                    pets = dom.xpath('//dl[@class="pet"]')
                    all_pets.extend(pets)

                self.all_rare_pets = 0
                rare_plus_pets = []
                for pet in all_pets:
                    image_url = pet.xpath('dt//img/@src')[0]
                    rarity = pet.xpath('dd[last()]//img/@alt')[0]
                    try:
                        adoption_date = pet.xpath('dd/span/span/text()')[0]
                    except IndexError:
                        print("RAN INTO ERROR")
                        adoption_date = ""
                    if rarity == 'Rare' or rarity == 'Very rare' or rarity == 'OMG so rare!':
                        rare_plus_pets.append((image_url, rarity, adoption_date))
                self.all_rare_pets = len(rare_plus_pets)

                self.stage = 2
                self.parsed_pets = 0
                image_data = []
                async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
                    for (image, _, _) in rare_plus_pets:
                        async with session.get(image, headers=headers) as response:
                            if response.status == 200:
                                content = await response.read()
                        content = io.BytesIO(content)
                        image_data.append(content)
                        self.parsed_pets += 1
                        await asyncio.sleep(0.5)

                self.stage = 3
                _, max_height = generate_image(1920, 1080, image_data, rare_plus_pets)
                canvas, _ = generate_image(1920, max_height, image_data, rare_plus_pets)

                output_buffer = io.BytesIO()  # Convert the PIL output into bytes
                canvas.save(output_buffer, 'png')  # Save the bytes as a PNG format
                base64_string = base64.b64encode(output_buffer.getvalue())
                expiration_date = datetime.datetime.now() + datetime.timedelta(hours=1, seconds=cs.get_pound_time(pound_data[1]))
                await collection.insert_one({'generated': True, 'image_base64': base64_string, 'expiration_date': expiration_date})
                self.generating_image = False
                self.stage = 0
                Constants.image_exists = True

        else:  # The command is currently generating the image
            message = 'Another user already ran this command!\nCurrent status: '
            if self.stage == 1:
                message += 'Collecting pets to check...'
            elif self.stage == 2:
                message += f'Checking pets... ({self.parsed_pets}/{self.all_rare_pets} pets checked)'
            elif self.stage == 3:
                message += 'Generating image...'
            await ctx.send(message)


def setup(bot):
    bot.add_cog(PoundPets(bot))
    bot.loop.create_task(image_expiration_check(bot))


def generate_image(width, height, image_data, rare_plus_pets):
    hex_colour = 'e0f6b2'
    rgb = [int(hex_colour[i:i + 2], 16) for i in (0, 2, 4)]
    rgb.append(255)
    rgba = tuple(rgb)

    pil_images = list(map(Image.open, image_data))
    max_width = width
    font = ImageFont.truetype('Verdana.ttf', 12)  # Verdana font size 15
    canvas = Image.new('RGBA', (max_width, height), rgba)
    draw = ImageDraw.Draw(canvas)  # Draw the image to PIL

    rare = Image.open('rarities/rare.png')
    very_rare = Image.open('rarities/veryrare.png')
    omg_so_rare = Image.open('rarities/omgsorare.png')

    current_width = 0
    current_max_height = 0
    y_offset = 0
    for i in pil_images:
        if current_width + i.width >= max_width:  # If pasting an image will cause it to go off canvas
            current_width = 0
            y_offset += current_max_height + 31 + 15
            current_max_height = 0

        if i.height > current_max_height:  # If pet is taller than current top height in row
            current_max_height = i.height

        if i.width < 106:
            paste_width = 106
            canvas.paste(i, (math.floor(current_width + ((106 - i.width) / 2)), y_offset))

            text_centre_offset_x = math.floor((106 - draw.textsize(rare_plus_pets[pil_images.index(i)][2], font=font)[0]) / 2)
            draw.text((current_width + text_centre_offset_x, i.height + y_offset), rare_plus_pets[pil_images.index(i)][2], fill=(0, 0, 0), font=font)
            pet_rarity = rare_plus_pets[pil_images.index(i)][1]
            if pet_rarity == 'Rare':
                canvas.paste(rare, (current_width, i.height + y_offset + 15), rare)
            elif pet_rarity == 'Very rare':
                canvas.paste(very_rare, (current_width, i.height + y_offset + 15), very_rare)
            elif pet_rarity == 'OMG so rare!':
                canvas.paste(omg_so_rare, (current_width, i.height + y_offset + 15), omg_so_rare)
        else:
            paste_width = i.width
            canvas.paste(i, (current_width, y_offset))

            pet_rarity = rare_plus_pets[pil_images.index(i)][1]
            pasting_width = math.floor((i.width - 106) / 2)
            text_centre_offset_x = math.floor((106 - draw.textsize(rare_plus_pets[pil_images.index(i)][2], font=font)[0]) / 2)
            draw.text((current_width + pasting_width + text_centre_offset_x, i.height + y_offset), rare_plus_pets[pil_images.index(i)][2], fill=(0, 0, 0), font=font)
            if pet_rarity == 'Rare':
                canvas.paste(rare, (current_width + pasting_width, i.height + y_offset + 15), rare)
            elif pet_rarity == 'Very rare':
                canvas.paste(very_rare, (current_width + pasting_width, i.height + y_offset + 15), very_rare)
            elif pet_rarity == 'OMG so rare!':
                canvas.paste(omg_so_rare, (current_width + pasting_width, i.height + y_offset + 15), omg_so_rare)

        current_width += paste_width
    total_height = y_offset + current_max_height + 31 + 15 + 30 + 50
    return canvas, total_height


async def image_expiration_check(bot):
    await bot.wait_until_ready()  # Wait until bot has loaded before starting background task
    while not bot.is_closed():  # While bot is still running
        cursor = collection.find({'generated': True})  # Try to get document of generated image
        document_data = await cursor.to_list(length=1)

        if len(document_data) == 0:
            pass
        else:
            object_id = document_data[0]['_id']
            if document_data[0]['expiration_date'] < datetime.datetime.now():
                await collection.delete_one({'_id': object_id})
                Constants.image_exists = False
            else:
                Constants.image_exists = True

        await asyncio.sleep(3600)  # Sleep for 1 hour
