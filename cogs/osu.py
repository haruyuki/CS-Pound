import math
import re
import time

import cv2
import discord
from discord.ext import commands
import numpy as np
from osuapi import OsuApi, AHConnector, enums
import urllib.error
import urllib.request

from constants import Constants
from library import get_dominant_colour


class Osu:
    def __init__(self, bot):
        self.bot = bot
        self.osu_emoji = discord.utils.get(bot.emojis, name='osu')  # Osu emoji
        self.osu_track_emoji = discord.utils.get(bot.emojis, name='osutrack')  # osu!track emoji
        self.osu_skills_emoji = discord.utils.get(bot.emojis, name='osuskills')  # osu!skills emoji
        self.osu_chan_emoji = discord.utils.get(bot.emojis, name='osuchan')  # osu!chan emoji
        self.pp_plus_emoji = discord.utils.get(bot.emojis, name='pp_plus')  # PP+ emoji
        self.score_xh = discord.utils.get(bot.emojis, name='scoreXH')  # XH score emoji
        self.score_x = discord.utils.get(bot.emojis, name='scoreX')  # X score emoji
        self.score_sh = discord.utils.get(bot.emojis, name='scoreSH')  # SH score emoji
        self.score_s = discord.utils.get(bot.emojis, name='scoreS')  # S score emoji
        self.score_a = discord.utils.get(bot.emojis, name='scoreA')  # A score emoji

    @commands.group()
    @commands.guild_only()
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None:
            title = f'{self.osu_emoji} Welcome to osu!'
            embed = discord.Embed(title=title, description='Available commands:', colour=0xFC6BA4)
            # embed.add_field(name='__**osu link**__ <username|id>', value='Link your Discord account to osu', inline=False)
            embed.add_field(name='__**osu profile**__ <username|id> [osu|taiko|ctb|mania]', value="View a user's osu! profile.", inline=False)
            # embed.add_field(name="__**osu beatmap**__ <link/id>", value="View information about a beatmap.", inline=False)
            # embed.add_field(name='__**osu recent**__ <username|id>')
            await ctx.send(embed=embed)

    @osu.command(aliases=['p'])
    @commands.guild_only()
    async def profile(self, ctx, user=None, mode=''):
        if user is None:
            embed = discord.Embed(title='osu!', description="You didn't provide a username/id!", colour=0xff5252)
        else:
            success = True
            regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)  # Regex to check if a link is provided

            if user.isdigit():  # If user provided an ID
                user = int(user)
            elif re.match(regex, user) is not None:  # If user provided an link
                link_split = user.split('/')
                user_id = [i for i in link_split if i.isdigit()]  # Get the user ID
                user = int(user_id[0])  # Convert ID into integer
            elif user.isalpha():  # If user provided a username
                pass

            if mode == 'taiko':  # If taiko mode selected
                gamemode = enums.OsuMode.taiko
            elif mode == 'ctb' or mode == 'catch' or mode == 'fruits':  # If catch the beat mode selected
                gamemode = enums.OsuMode.ctb
            elif mode == 'mania':  # If mania mode selected
                gamemode = enums.OsuMode.mania
            else:  # Set default gamemode
                gamemode = enums.OsuMode.osu

            api = OsuApi(Constants.osu_api_key, connector=AHConnector())  # Connect to osu! API
            result = await api.get_user(user, mode=gamemode)
            try:
                user_data = result[0]
            except IndexError:
                success = False
                user_data = None

            if success:
                try:
                    user_icon = f'https://a.ppy.sh/{user_data.user_id}?_={int(time.time())}'  # The URL to the user profile picture
                    resp = urllib.request.urlopen(user_icon)  # Get icon
                    image = np.asarray(bytearray(resp.read()), dtype='uint8')  # Convert image into array
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # Convert into openCV-friendly format
                    rgb = get_dominant_colour(image)
                    hex_colour = eval('0x%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2])))  # Convert RGB into hex colour
                except urllib.error.HTTPError:
                    user_icon = 'https://osu.ppy.sh/images/layout/avatar-guest.png'
                    hex_colour = eval('0xfefefe')

                title = f'{self.osu_emoji} Stats for {user_data.username} (Lvl. {math.floor(user_data.level)})'
                seconds_played = user_data.total_seconds_played
                m, s = divmod(seconds_played, 60)
                h, m = divmod(m, 60)
                seconds_played = "%dhrs, %02dmins, %02dsecs" % (h, m, s)
                total_hits = user_data.count300 + user_data.count100 + user_data.count50

                description = f'''User ID: {user_data.user_id}
PP: {round(user_data.pp_raw)}
Rank: #{user_data.pp_rank}
Country Rank: :flag_{user_data.country.lower()}: #{user_data.pp_country_rank}

Ranked Score: {format(user_data.ranked_score, ',')}
Hit Accuracy: {round(user_data.accuracy, 2)}
Play Count: {format(user_data.playcount, ',')}
Total Score: {format(user_data.total_score, ',')}
Total Hits: {format(total_hits, ',')}
Play Time: {seconds_played}

{self.score_xh}: {user_data.count_rank_ssh}　{self.score_x}: {user_data.count_rank_ss}　{self.score_sh}: {user_data.count_rank_sh}　{self.score_s}: {user_data.count_rank_s}　{self.score_a}: {user_data.count_rank_a}'''
                embed = discord.Embed(title=title, description=description, colour=hex_colour)
                embed.set_thumbnail(url=user_icon)

                ameobea_link = 'https://ameobea.me/osutrack/user/' + user_data.username
                osuskills_link = 'http://osuskills.tk/user/' + user_data.username
                osuchan_link = 'https://syrin.me/osuchan/u/' + str(user_data.user_id)
                ppplus_link = 'https://syrin.me/pp+/u/' + user_data.username

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
                embed.add_field(name="More information", value=other_sites, inline=False)

            else:
                embed = discord.Embed(title='osu!', description="That username/id doesn't exist!", colour=0xff5252)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
