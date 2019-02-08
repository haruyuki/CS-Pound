import aiohttp
import io
import re

import discord
from discord.ext import commands
import html2text
import lxml.html
from PIL import Image

import chickensmoothie as cs


class Announcement:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['announce', 'news'])
    @commands.guild_only()
    async def announcement(self, ctx):
        pass

    @announcement.command()
    @commands.guild_only()
    async def on(self, ctx):
        pass

    @announcement.command()
    @commands.guild_only()
    async def off(self, ctx):
        pass

    @announcement.command()
    @commands.guild_only()
    async def latest(self, ctx):
        # 1) Get the latest news item from the news page
        news_articles = await cs.get_announcements()  # Get the HTML list of all the announcements
        latest = news_articles[0]  # Get the first (latest) announcement

        # 2) Get the article post date
        post_date = latest.getparent().getprevious().text

        # 3) Check for main image, and if exists get link and remove tag. If more than 1, create PIL image
        image_link = None  # Assume announcement has no images
        images = None
        multiple_images = False
        if latest.find('a/img[@alt="Image"]') is not None:  # If announcement has click-able images
            if len(latest.findall('a/img[@alt="Image"]')) <= 1:
                image_tag = latest.find('a/img[@alt="Image"]')  # Get the 'img' tag
                image_link = image_tag.xpath('@src')[0]  # Extract image link for use in embed later
                parent = image_tag.getparent()  # Get parent tag of 'img', which is 'a' tag
                latest.remove(parent)  # Remove the 'a' tag so it won't be converted to Markdown
            else:
                images = latest.findall('a/img[@alt="Image"]')
                multiple_images = True
        elif latest.find('img[@alt="Image"]') is not None:  # If the announcement has static images instead
            if len(latest.findall('img[@alt="Image"]')) <= 1:
                image_tag = latest.find('img[@alt="Image"]')  # Get the 'img' tag
                image_link = image_tag.xpath('@src')[0]  # Extract image link for use in embed later
                latest.remove(image_tag)  # Remove the 'img' tag so it won't be parsed later
            else:
                image_tags = latest.findall('img[@alt="Image"]')
                image_links = [element.xpath('@src')[0] for element in image_tags]
                image_links = [url.replace('//', 'https://') for url in image_links]

                images = []
                async with aiohttp.ClientSession() as session:
                    for link in image_links:
                        async with session.get(link) as response:
                            connection = await response.read()
                            images.append(io.BytesIO(connection))
                multiple_images = True

        if multiple_images:
            pil_images = map(Image.open, images)
            print(pil_images)
            total_rows = 1
            max_width = 550
            base_height = 0
            base_width = 0
            for image in pil_images:
                base_height = image.height
                base_width += image.width
                if base_width >= max_width:
                    current_width = 0
                    total_rows += 1
            print(total_rows)

            offset = 5
            canvas = Image.new('RGBA', (max_width, total_rows * base_height))
            current_width = 0
            current_height = 0
            for image in pil_images:
                canvas.paste(image, current_width)

        # 4) Convert remaining HTML into Markdown
        text = lxml.html.tostring(latest)
        text_decoded = text.decode('utf-8')

        # 6) Check if emoji's exist in news content, and remove them
        emoji_list = re.findall(r'\s*<img[\w\W]+?>', text_decoded)
        if emoji_list:
            for emoji in emoji_list:
                text_decoded = text_decoded.replace(emoji, '')

        # 7) Replace relative links with absolute links
        text_decoded = text_decoded.replace('//', 'https://')
        links = set(re.findall(r'href="(.*?)"', text_decoded))  # Get all href links
        for link in links:
            text_decoded = text_decoded.replace(link, f'https://www.chickensmoothie.com{link}')  # Prepend Chicken Smoothie base URL

        # 8) Convert HTML to Markdown
        content = html2text.html2text(text_decoded)

        # 9) Fix up broken newlines
        newline = '  \n'
        content = content.replace(newline, '$#@')
        content = content.replace('\n', ' ')
        content = content.replace('$#@', '\n')
        content = content.replace('\n\n\n', '\n')

        # 10) Fix broken Markdown links
        links = re.findall(r'\(http[s]*[\w\W]+?\)', content)
        for link in links:
            fixed_link = link.replace(' ', '')
            content = content.replace(link, fixed_link)

        # 11) Send embed
        embed = discord.Embed(title=post_date, description=content, colour=0x4ba139)  # Create embed
        if image_link is not None:  # If image exists in announcement
            embed.set_image(url=f'https:{image_link}')  # Set embed image
        await ctx.send(embed=embed)  # Send message


def setup(bot):
    bot.add_cog(Announcement(bot))
