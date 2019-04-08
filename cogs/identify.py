import sqlite3
import textwrap
from urllib.parse import urlparse, parse_qsl

from discord.ext import commands

import chickensmoothie as cs

sqlite_database = 'cs_archive.sqlite3'
months = {'January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December'}
exceptions = {'3B46301A6C8B850D87A730DA365B0960', 'E5FEFE44A3070BC9FC176503EC1A603F',
              '0C1AFF9AEAA0953F1B1F9B818C2771C9', '7C912BA5616D2E24E9F700D90E4BA2B6',
              '905BB7DE4BC4E29D7FD2D1969667B568', '773B14EEB416FA762C443D909FFED344',
              '1C0DB4785FC78DF4395263D40261C614', '5066110701B0AE95948A158F0B262EBB',
              '5651A6C10C4D375A1901142C49C5C70C', '8BED72498D055E55ABCA7AD29B180BF4'}


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
        try:
            return dict(parse_qsl(components.query))['k']  # Pet ID
        except KeyError:
            if 'trans' in pet_image_link:
                return 'trans'
            else:
                return None

    @commands.command(aliases=['id'])
    async def identify(self, ctx, link: str):
        if 'static' in link:
            components = urlparse(link)
            try:
                pet_id = dict(parse_qsl(components.query))['k']
            except KeyError:
                return None
        else:
            pet_id = await self.get_system_pet_id(link)

        conn = self.create_connection(sqlite_database)
        c = conn.cursor()
        c.execute('SELECT Year, Event, Archive_Link FROM ChickenSmoothie_Archive WHERE Pet_ID=?', (pet_id,))
        if pet_id in exceptions:
            await ctx.send('That pet is not identifiable at this growth stage :frowning:')
        elif pet_id == 'trans':
            await ctx.send('Pets with items are unable to be identified :frowning:')
        elif pet_id is None:
            await ctx.send('That pet cannot be identified :frowning:')
        else:
            try:
                data = c.fetchone()
                year = data[0]
                event = data[1]
                archive_link = data[2]
                if event in months:
                    message = f'''\
                    The pet is a {event} {year} pet!
                    Archive Link: {archive_link}'''
                else:
                    message = f'''\
                    The pet is a {year} {event} pet!
                    Archive Link: {archive_link}'''
                message = textwrap.dedent(message)
                await ctx.send(message)
            except TypeError:
                await ctx.send('There is no data for this pet yet :frowning:')
            conn.close()

    @identify.error  # On error with identify command
    async def command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):  # If user didn't pass a valid link
            await ctx.send('That is not a valid pet link!')


def setup(bot):
    bot.add_cog(Identify(bot))
