import sqlite3
import textwrap
from urllib.parse import urlparse, parse_qsl, unquote

from discord.ext import commands

import chickensmoothie as cs

sqlite_database = 'cs_archive.sqlite'
table_name = 'PetDates'
column1 = 'PetID'
column2 = 'ArchiveDate'
months = {'January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December'}


class Identify:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_connection(db_file):
        try:
            connection = sqlite3.connect(db_file)
            return connection
        except Exception as e:
            print(e)
        return None

    @staticmethod
    async def get_system_pet_id(link):
        pet = await cs.pet(link)
        pet_image_link = pet['image']
        components = urlparse(pet_image_link)
        return dict(parse_qsl(components.query))['k']  # Pet ID

    @commands.command()
    async def identify(self, ctx, link: str):
        if 'static' in link:
            components = urlparse(link)
            pet_id = dict(parse_qsl(components.query))['k']
        else:
            pet_id = await self.get_system_pet_id(link)

        conn = self.create_connection(sqlite_database)
        c = conn.cursor()
        c.execute(f'SELECT {column2} FROM {table_name} WHERE {column1}="{pet_id}"')
        try:
            pet_exists = c.fetchone()[0]
            items = pet_exists.split('/')
            items.remove('archive')
            year, event = filter(None, items)
            if event in months:
                message = f'''\
                The pet is a {event} {year} pet!
                Archive Link: https://www.chickensmoothie.com{pet_exists}'''
            else:
                message = f'''\
                The pet is a {year} {unquote(event)} pet!
                Archive Link: https://www.chickensmoothie.com{pet_exists}'''
            message = textwrap.dedent(message)
            await ctx.send(message)
        except TypeError:
            await ctx.send('CS Pound has no data for that pet :frowning:')
        conn.close()

    @identify.error  # On error with identify command
    async def command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):  # If user didn't pass a valid link
            await ctx.send('That is not a valid pet link!')


def setup(bot):
    bot.add_cog(Identify(bot))
