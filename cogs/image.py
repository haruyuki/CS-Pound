import aiohttp
import discord
from discord.ext import commands
import io
from library import get_web_data
import math
from PIL import Image, ImageFont, ImageDraw


class PetImage:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['img'])
    #@commands.guild_only()
    async def image(self, ctx, link: str = ''):
        data = await get_web_data(link, 'pet')  # Get pet data
        if data[0]:  # If data is valid
            information = {}
            owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet
            titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
            values = data[1].xpath('//td[@class="r"]')  # Values of pet information

            pet_image = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
            if 'trans' in pet_image:  # If pet image is transparent (i.e. Pet has items)
                pet_image = 'http://www.chickensmoothie.com' + pet_image  # Pet image link
                transparent = True
            else:
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
                case3 = 1
                case4 = 1
                if pps:  # If pet has no name and is PPS
                    case1 = 'Pet\'s name:'
                    case2 = 'Pet ID:'
                    case3 = 2
                    case4 = 1
            elif pps:  # If pet has a name and is PPS
                case1 = 'Pet ID:'
                case2 = 'Pet\'s name:'
                case3 = 2
                case4 = 1
            else:  # If pet has a name but is not PPS
                case1 = 'Pet\'s name:'
                case2 = 'Adopted:'
                case3 = 1
                case4 = 1

            temp = len(titles) - 1 if pps else len(titles)  # Is pet is PPS, remove one title, else all titles
            for i in range(temp):  # For each title in titles
                if titles[i] == (case1):
                    information['Name'] = values[i].xpath('text()')[0]  # Add pet name to information dictionary
                elif titles[i] == (case2):
                    information['Adopted'] = values[i].xpath('text()')[0]  # Add pet adoption date to information dictionary
                elif titles[i] == ('Growth:' if pps else 'Rarity:'):  # If pet is PPS, if titles[i] matches 'Growth:', otherwise if not PPS, if titles[i] matches with 'Rarity:'
                    information['Rarity'] = 'rarities/' + values[i].xpath('img/@src')[0][12:]  # Local link to rarity image

            if titles[case3] == 'Pet ID:':
                filename = values[case4].xpath('text()')[0]  # Get pet ID
            else:  # If ID cannot be found
                filename = 'pet'

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

            image = Image.new('RGBA', (max_width, total_height), (225, 246, 179, 255))  # Create an RGBA image of max_width x total_height, with colour 225, 246, 179
            pil_image = ImageDraw.Draw(image)  # Draw the image to PIL

            y_offset = 0  # Offset for vertically stacking images
            if transparent:  # If pet has items
                image.paste(images[0], (math.floor((max_width - images[0].size[0])/2), y_offset), images[0])  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[0]
            else:  # If pet doesn't have items
                image.paste(images[0], (math.floor((max_width - images[0].size[0])/2), y_offset))  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2)
            y_offset += images[0].size[1]  # Add height of image + 10 to offset

            try:
                pil_image.text((math.floor(((max_width - math.floor(pil_image.textsize(information['Name'], font=font)[0]))/2)), y_offset), information['Name'], fill=(0, 0, 0), font=font)  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
                y_offset += 15  # Add offset of 15
            except KeyError:
                pass

            try:
                pil_image.text((math.floor(((max_width - math.floor(pil_image.textsize(information['Adopted'], font=font)[0]))/2)), y_offset), information['Adopted'], fill=(0, 0, 0), font=font)  # Paste text at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset) with colour (0, 0, 0) and font
                y_offset += 15  # Add offset of 15
            except KeyError:
                pass

            image.paste(images[1], (math.floor((max_width - images[1].size[0])/2), y_offset), images[1])  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2) using the mask from images[1]

            output_buffer = io.BytesIO()  # Convert the PIL output into bytes
            image.save(output_buffer, 'png')  # Save the bytes as a PNG format
            output_buffer.seek(0)  # Move the 'cursor' back to the start

            filename += '.png'  # Set filename as (Pet ID).png

            await ctx.send(file=discord.File(fp=output_buffer, filename=filename))  # Upload the file to the channel where message came from
        else:  # If data is invalid
            await ctx.send(embed=data[1])  # Send embed


def setup(bot):
    bot.add_cog(PetImage(bot))
