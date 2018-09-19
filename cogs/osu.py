import re

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

    @commands.group()
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None:
            osu_emoji = discord.utils.get(self.bot.emojis, name='osu')  # Osu emoji
            title = osu_emoji + ' Welcome to osu!'
            embed = discord.Embed(title=title, description='Available commands:', colour=0xFC6BA4)
            # embed.add_field(name='__**osu link**__ <username|id>', value='Link your Discord account to osu', inline=False)
            embed.add_field(name='__**osu profile**__ <username|id> [osu|taiko|ctb|mania]', value="View a user's osu! profile.", inline=False)
            # embed.add_field(name="__**osu beatmap**__ <link/id>", value="View information about a beatmap.", inline=False)
            # embed.add_field(name='__**osu recent**__ <username|id>')
            await ctx.send(embed=embed)

    @osu.command()
    async def profile(self, ctx, user, mode=''):
        osu_emoji = discord.utils.get(self.bot.emojis, name='osu')  # Osu emoji
        score_xh = discord.utils.get(self.bot.emojis, name='scoreXH')  # XH score emoji
        score_x = discord.utils.get(self.bot.emojis, name='scoreX')  # X score emoji
        score_sh = discord.utils.get(self.bot.emojis, name='scoreSH')  # SH score emoji
        score_s = discord.utils.get(self.bot.emojis, name='scoreS')  # S score emoji
        score_a = discord.utils.get(self.bot.emojis, name='scoreA')  # A score emoji

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
                user_icon = 'https://a.ppy.sh/' + str(user_data.user_id)  # The URL to the user profile picture
                resp = urllib.request.urlopen(user_icon)  # Get icon
                image = np.asarray(bytearray(resp.read()), dtype='uint8')  # Convert image into array
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # Convert into openCV-friendly format
                rgb = get_dominant_colour(image)
                hex_colour = eval('0x%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2])))  # Convert RGB into hex colour
            except urllib.error.HTTPError:
                user_icon = 'https://osu.ppy.sh/images/layout/avatar-guest.png'
                hex_colour = eval('0xfefefe')

            title = f'{osu_emoji} Stats for {user_data.username} (Lvl. {user_data.level})'
            try:
                seconds_played = user_data.total_seconds_played
                m, s = divmod(seconds_played, 60)
                h, m = divmod(m, 60)
                seconds_played = "%dhrs %02dmins %02dsecs" % (h, m, s)
            except Exception:
                seconds_played = 'Not Available Yet'

            description = f'''User ID: {user_data.user_id}
                        PP: {user_data.pp_raw}
                        Rank: #{user_data.pp_rank}
                        Country Rank: :flag_{user_data.country.lower()}: #{user_data.pp_country_rank}

                        Ranked Score: {user_data.ranked_score}
                        Hit Accuracy: {user_data.accuracy}
                        Play Count: {user_data.playcount}
                        Total Score: {user_data.total_score}
                        Total Hits: {user_data.count300 + user_data.count100 + user_data.count50}
                        Total Play Time: {seconds_played}

                        {score_xh}: {user_data.count_rank_ssh}　{score_x}: {user_data.count_rank_ss}　{score_sh}: {user_data.count_rank_sh}　{score_s}: {user_data.count_rank_s}　{score_a}: {user_data.count_rank_a}'''
            embed = discord.Embed(title=title, description=description, colour=hex_colour)
            embed.set_thumbnail(url=user_icon)

            if mode == 'taiko':
                ameobea = 'https://ameobea.me/osutrack/user/' + user_data.username + '/taiko'
                osuchan = 'https://syrin.me/osuchan/u/' + str(user_data.user_id) + '/?m=1'
                other_sites = f'[osu!track]({ameobea}) - [osu!chan]({osuchan})'
                embed.add_field(name="More information", value=other_sites, inline=False)
            elif mode == 'ctb' or mode == 'catch' or mode == 'fruits':
                ameobea = 'https://ameobea.me/osutrack/user/' + user_data.username + '/ctb'
                osuchan = 'https://syrin.me/osuchan/u/' + str(user_data.user_id) + '/?m=2'
                other_sites = f'[osu!track]({ameobea}) - [osu!chan]({osuchan})'
                embed.add_field(name="More information", value=other_sites, inline=False)
            elif mode == 'mania':
                ameobea = 'https://ameobea.me/osutrack/user/' + user_data.username + '/mania'
                osuchan = 'https://syrin.me/osuchan/u/' + str(user_data.user_id) + '/?m=3'
                other_sites = f'[osu!track]({ameobea}) - [osu!chan]({osuchan})'
                embed.add_field(name="More information", value=other_sites, inline=False)
            else:
                ameobea = 'https://ameobea.me/osutrack/user/' + user_data.username
                osuskills = 'http://osuskills.tk/user/' + user_data.username
                osuchan = 'https://syrin.me/osuchan/u/' + str(user_data.user_id)
                ppplus = 'https://syrin.me/pp+/u/' + user_data.username
                other_sites = f'[osu!track]({ameobea}) - [osu!Skills]({osuskills}) - [osu!chan]({osuchan}) - [PP+]({ppplus})'
                embed.add_field(name="More information", value=other_sites, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("That user doesn't exist!")


def setup(bot):
    bot.add_cog(Osu(bot))