from collections import Counter
import re

import asyncio
import cv2
import discord
from discord.ext import commands
import numpy as np
from osuapi import OsuApi, AHConnector, enums
from sklearn.cluster import KMeans
import urllib.request

from constants import constants


class Osu:
    def __init__(self, bot):
        self.bot = bot

    def get_dominant_color(self, image):
        image = cv2.resize(image, (25, 25), interpolation=cv2.INTER_AREA)
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        clt = KMeans(n_clusters=4)
        labels = clt.fit_predict(image)
        label_counts = Counter(labels)
        dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
        return list(dominant_color)

    @commands.group()
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Welcome to osu!", description="List of available commands:", colour=0xFC6BA4)
            embed.add_field(name="__**osu profile**__ <username/id>", value="View your osu! profile.", inline=False)
            # embed.add_field(name="__**osu beatmap**__ <link/id>", value="View information about a beatmap.", inline=False)
            await ctx.send(embed=embed)

    @osu.command()
    async def profile(self, ctx, user, mode=''):
        success = True
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if user.isdigit():  # If user provided an ID
            user = int(user)
        elif re.match(regex, user) is not None:  # If user provided an link
            link_split = user.split('/')
            id = [i for i in link_split if i.isdigit()]
            user = int(id[0])
        elif user.isalpha():  # If user provided a username
            pass

        if mode == 'taiko':  # If taiko mode selected
            gamemode = enums.OsuMode.taiko
        elif mode == 'ctb':  # If catch the beat mode selected
            gamemode = enums.OsuMode.ctb
        elif mode == 'mania':  # If mania mode selected
            gamemode = enums.OsuMode.mania
        else:  # Set default gamemode
            gamemode = enums.OsuMode.osu

        api = OsuApi(constants.osu_api_key, connector=AHConnector())
        result = await api.get_user(user, mode=gamemode)
        try:
            user_data = result[0]
        except IndexError:
            success = False

        if success:
            user_icon = 'https://a.ppy.sh/' + str(user_data.user_id)
            resp = urllib.request.urlopen(user_icon)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            rgb = self.get_dominant_color(image)
            hex_colour = '0x%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))
            print(hex_colour)

            title = 'Statistics for ' + user_data.username
            embed = discord.Embed(title=title, description="test", colour=eval(hex_colour))
            embed.add_field(name='User ID', value=user_data.user_id)
            embed.add_field(name="Username", value=user_data.username)
            embed.add_field(name="Play Count", value=user_data.playcount)
            embed.add_field(name="PP", value=int(user_data.pp_raw))
            embed.add_field(name="Ranking", value=user_data.pp_rank)
            ameobea = 'https://ameobea.me/osutrack/user/' + user_data.username
            osuskills = 'http://osuskills.tk/user/' + user_data.username
            osuchan = 'https://syrin.me/osuchan/u/' + str(user_data.user_id)
            ppplus = 'https://syrin.me/pp+/u/' + user_data.username
            if mode == '':
                other_sites = f'[osu!track]({ameobea}) - [osu!Skills]({osuskills}) - [osu!chan]({osuchan}) - [PP+]({ppplus})'
                embed.add_field(name="Other Sites", value=other_sites, inline=False)
            embed.set_thumbnail(url=user_icon)

            await ctx.send(embed=embed)
        else:
            await ctx.send("That user doesn't exist!")

def setup(bot):
    bot.add_cog(Osu(bot))
