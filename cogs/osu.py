import math
import time

import cv2
import discord
from discord.ext import commands
import motor.motor_asyncio as amotor
import numpy as np
import urllib.error
import urllib.request

from constants import Constants
from library import get_dominant_colour
from osu import get_user

client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
db = client['cs_pound']
collection = db['osu_profiles']


class Osu:
    def __init__(self, bot):
        self.bot = bot
        self.osu_emoji = None
        self.osu_track_emoji = None
        self.osu_skills_emoji = None
        self.osu_chan_emoji = None
        self.pp_plus_emoji = None
        self.score_xh = None
        self.score_x = None
        self.score_sh = None
        self.score_s = None
        self.score_a = None
        bot.loop.create_task(self.load_emoji())

    async def load_emoji(self):
        await self.bot.wait_until_ready()
        self.osu_emoji = discord.utils.get(self.bot.emojis, name='osu')  # Osu emoji
        self.osu_track_emoji = discord.utils.get(self.bot.emojis, name='osutrack')  # osu!track emoji
        self.osu_skills_emoji = discord.utils.get(self.bot.emojis, name='osuskills')  # osu!skills emoji
        self.osu_chan_emoji = discord.utils.get(self.bot.emojis, name='osuchan')  # osu!chan emoji
        self.pp_plus_emoji = discord.utils.get(self.bot.emojis, name='pp_plus')  # PP+ emoji
        self.score_xh = discord.utils.get(self.bot.emojis, name='scoreXH')  # XH score emoji
        self.score_x = discord.utils.get(self.bot.emojis, name='scoreX')  # X score emoji
        self.score_sh = discord.utils.get(self.bot.emojis, name='scoreSH')  # SH score emoji
        self.score_s = discord.utils.get(self.bot.emojis, name='scoreS')  # S score emoji
        self.score_a = discord.utils.get(self.bot.emojis, name='scoreA')  # A score emoji
        return None

    @commands.group()
    @commands.guild_only()
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None:
            title = f'{self.osu_emoji} Welcome to osu!'
            embed = discord.Embed(title=title, description='Available commands:', colour=0xFC6BA4)
            embed.add_field(name='__**osu link**__ <username|id>', value='Link your Discord account to osu', inline=False)
            embed.add_field(name='__**osu profile**__ <username|id> [osu|taiko|ctb|mania]', value="View a user's osu! profile.", inline=False)
            # embed.add_field(name='__**osu beatmap**__ <link/id>', value='View information about a beatmap.', inline=False)
            # embed.add_field(name='__**osu recent**__ <username|id>', value="View a user's recently played maps")
            await ctx.send(embed=embed)

    @osu.command(aliases=['l'])
    @commands.guild_only()
    async def link(self, ctx, user=None):
        if user is None:
            embed = discord.Embed(title='osu!', description="You didn't provide a username/id!", colour=0xff5252)
        else:
            await collection.insert_one({'user_id': str(ctx.author.id), 'osu_user': str(user)})
            embed = discord.Embed(title='osu! **Linked!**', description='Your profile has been linked!', colour=0xFC6BA4)
        await ctx.send(embed=embed)

    @osu.command(aliases=['p'])
    @commands.guild_only()
    async def profile(self, ctx, user=None, mode=''):
        if user is None:
            user = ctx.author.id
        data = await get_user(user, mode)

        if data is not None:
            try:
                user_icon = f'https://a.ppy.sh/{data.user_id}?_={int(time.time())}'  # The URL to the user profile picture
                resp = urllib.request.urlopen(user_icon)  # Get icon
                image = np.asarray(bytearray(resp.read()), dtype='uint8')  # Convert image into array
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # Convert into openCV-friendly format
                rgb = get_dominant_colour(image)
                hex_colour = '0x%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))  # Convert RGB into hex colour
            except urllib.error.HTTPError:
                user_icon = 'https://osu.ppy.sh/images/layout/avatar-guest.png'
                hex_colour = 0xfefefe

            title = f'{self.osu_emoji} Stats for {data.username} (Lvl. {math.floor(data.level)})'
            seconds_played = data.total_seconds_played
            m, s = divmod(seconds_played, 60)
            h, m = divmod(m, 60)
            seconds_played = '%dhrs, %02dmins, %02dsecs' % (h, m, s)
            total_hits = data.count300 + data.count100 + data.count50
            description = f'''User ID: {data.user_id}

Ranked Score: {format(data.ranked_score, ',')}
Hit Accuracy: {round(data.accuracy, 2)}
Play Count: {format(data.playcount, ',')}
Total Score: {format(data.total_score, ',')}
Total Hits: {format(total_hits, ',')}
Play Time: {seconds_played}

{self.score_xh}: {data.count_rank_ssh}　{self.score_x}: {data.count_rank_ss}　{self.score_sh}: {data.count_rank_sh}　{self.score_s}: {data.count_rank_s}　{self.score_a}: {data.count_rank_a}'''

            embed = discord.Embed(title=title, colour=hex_colour)
            embed.set_thumbnail(url=user_icon)
            embed.add_field(name=f'**PP: {round(data.pp_raw)}pp　(#{data.pp_rank})　:flag_{data.country.lower()}: #{data.pp_country_rank}**', value=description)

            ameobea_link = 'https://ameobea.me/osutrack/user/' + data.username
            osuskills_link = 'http://osuskills.tk/user/' + data.username
            osuchan_link = 'https://syrin.me/osuchan/u/' + str(data.user_id)
            ppplus_link = 'https://syrin.me/pp+/u/' + data.username

            if mode == 'taiko':
                ameobea_link += '/taiko'
                osuchan_link += '/?m=1'
                other_sites = f'{self.osu_track_emoji} [osu!track]({ameobea_link}) - {self.osu_chan_emoji} [osu!chan]({osuchan_link})'
            elif mode == 'ctb' or mode == 'catch' or mode == 'fruits':
                ameobea_link += '/ctb'
                osuchan_link += '/?m=2'
                other_sites = f'{self.osu_track_emoji} [osu!track]({ameobea_link}) - {self.osu_chan_emoji} [osu!chan]({osuchan_link})'
            elif mode == 'mania':
                ameobea_link += '/mania'
                osuchan_link += '/?m=3'
                other_sites = f'{self.osu_track_emoji} [osu!track]({ameobea_link}) - {self.osu_chan_emoji} [osu!chan]({osuchan_link})'
            else:
                other_sites = f'{self.osu_track_emoji} [osu!track]({ameobea_link}) - {self.osu_skills_emoji} [osu!Skills]({osuskills_link}) - {self.osu_chan_emoji} [osu!chan]({osuchan_link}) - {self.pp_plus_emoji} [PP+]({ppplus_link})'
            embed.add_field(name='More information', value=other_sites, inline=False)

        else:
            embed = discord.Embed(title='osu!', description="You didn't provide a valid username or id!", colour=0xff5252)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
