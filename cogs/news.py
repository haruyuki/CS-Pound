import aiohttp
import io
import re

import discord
from discord.ext import commands
import html2text
import lxml.html
from PIL import Image

import chickensmoothie as cs


class News:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['announce', 'announcement'])
    @commands.guild_only()
    async def news(self, ctx):
        pass

    @news.command()
    @commands.guild_only()
    async def on(self, ctx):
        pass

    @news.command()
    @commands.guild_only()
    async def off(self, ctx):
        pass

    @news.command()
    @commands.guild_only()
    async def latest(self, ctx):
        news_articles = await cs.get_announcements()  # Get the HTML list of all the news articles
        latest = news_articles[0]  # Get the latest (first) news
        post_date = latest.getparent().getprevious().text  # Get the news post date

        image_link = None
        image_list = None
        multiple_images = False
        canvas = None
        if latest.find('a/img[@alt="Image"]') is not None:  # If news has click-able images
            if len(latest.findall('a/img[@alt="Image"]')) == 1:  # If there is only 1 image
                image_tag = latest.find('a/img[@alt="Image"]')  # Get the 'img' tag
                image_link = image_tag.xpath('@src')[0]  # Extract image link for use in embed later
                parent = image_tag.getparent()  # Get parent tag of 'img', which is 'a' tag
                latest.remove(parent)  # Remove the 'a' tag so it won't be converted to Markdown
            else:  # If there is more than 1 image
                image_list = latest.findall('a/img[@alt="Image"]')  # Get the links to all the images
                multiple_images = True
        elif latest.find('img[@alt="Image"]') is not None:  # If the news has static images instead
            if len(latest.findall('img[@alt="Image"]')) == 1:  # If there is only 1 image
                image_tag = latest.find('img[@alt="Image"]')  # Get the 'img' tag
                image_link = image_tag.xpath('@src')[0]  # Extract image link for use in embed later
                latest.remove(image_tag)  # Remove the 'img' tag so it won't be parsed later
            else:  # If there is more than 1 image
                image_tags = latest.findall('img[@alt="Image"]')  # Get all image tags
                image_links = [element.xpath('@src')[0] for element in image_tags]  # Get the links to the image
                image_links = [url.replace('//', 'https://') for url in image_links]  # Replace relative links with absolute links

                image_list = []
                async with aiohttp.ClientSession() as session:
                    for link in image_links:
                        async with session.get(link) as response:
                            connection = await response.read()
                            image_list.append(io.BytesIO(connection))  # Convert the images into bytes
                multiple_images = True

        if multiple_images:  # If there are multiple images
            pil_images = list(map(Image.open, image_list))  # Open all byte images as PIL images

            current_width = 0
            current_heights = []
            for image in pil_images:
                current_width += image.width
                current_heights.append(image.height)
            max_height = max(current_heights)  # Get the height of the tallest image

            x_offset = 10  # The spacing between images
            canvas_width = current_width + (x_offset * len(pil_images))
            canvas_height = max_height

            canvas = Image.new('RGBA', (canvas_width, canvas_height))  # Create an empty RGBA image
            current_x = 0
            for image in pil_images:
                canvas.paste(image, (current_x, (max_height - image.height)), image)
                current_x += image.width + x_offset

        text = lxml.html.tostring(latest)  # Get the source HTML of the news article
        text_decoded = text.decode('utf-8')  # Decode into UTF-8

        bold_span_tags = re.findall(r'(<span style="font-weight: bold">([\w\W]+?)</span>)', text_decoded)  # Find all <span> tags used to bold text
        if bold_span_tags:  # If there are bolded text
            for tag in bold_span_tags:
                text_decoded = text_decoded.replace(tag[0], f'%@^{tag[1]}%@^')  # Change the <span> tag to a temporary name

        emoji_list = re.findall(r'\s*<img[\w\W]+?>', text_decoded)  # Check if there are emojis in the news article
        if emoji_list:  # If there are emojis
            for emoji in emoji_list:
                text_decoded = text_decoded.replace(emoji, '')  # Remove the emoji

        text_decoded = text_decoded.replace('//', 'https://')  # Replace all relative links to prefix with HTTPS
        links = set(re.findall(r'href="(.*?)"', text_decoded))  # Get all href links
        for link in links:
            text_decoded = text_decoded.replace(link, f'https://www.chickensmoothie.com{link}')  # Prepend Chicken Smoothie base URL

        content = html2text.html2text(text_decoded)  # Convert remaining HTML into Markdown

        content = content.replace('  \n', '$#@')  # Fix up broken newlines
        content = content.replace('\n', ' ')
        content = content.replace('$#@', '\n')
        content = content.replace('%@^', '**')  # Replace temporary span tags to **
        content = content.replace('\n\n\n', '\n')  # Remove duplicate newlines

        links = re.findall(r'\(http[s]*[\w\W]+?\)', content)  # Get all links in the Markdown
        for link in links:
            fixed_link = link.replace(' ', '')  # Remove any spacing in them
            content = content.replace(link, fixed_link)

        # 11) Send embed
        embed = discord.Embed(title=post_date, description=content, colour=0x4ba139)  # Create embed
        if multiple_images:  # If there are multiple images
            output_buffer = io.BytesIO()  # Convert the PIL output into bytes
            canvas.save(output_buffer, 'png')  # Save the bytes as a PNG format
            output_buffer.seek(0)  # Move the 'cursor' back to the start
            await ctx.send(embed=embed, file=discord.File(fp=output_buffer, filename='news.png'))  # Upload the file to the channel where message came from
        elif image_link is not None:  # If image exists in news
            embed.set_image(url=f'https:{image_link}')  # Set embed image
            await ctx.send(embed=embed)  # Send message
        else:
            await ctx.send(embed=embed)  # Send message


def setup(bot):
    bot.add_cog(News(bot))
