import datetime
import json
import os
import random
import re
import time
import uuid

import asyncio
import discord
from discord.ext import commands

from library import parse_short_time
import chickensmoothie as cs


def _create_encoder(cls):
    def _default(self, o):
        if isinstance(o, cls):
            return o.to_json()
        return super().default(o)

    return type('_Encoder', (json.JSONEncoder,), {'default': _default})


class NoWinnerFound(Exception):
    pass


class Database:
    """The "database" object. Internally based on ``json``."""

    def __init__(self, name, **options):
        self.name = f'{name}.json'
        self.object_hook = options.pop('object_hook', None)
        self.encoder = options.pop('encoder', None)

        self._db = None

        try:
            hook = options.pop('hook')
        except KeyError:
            pass
        else:
            self.object_hook = hook.from_json
            self.encoder = _create_encoder(hook)

        self.loop = options.pop('loop', asyncio.get_event_loop())
        self.lock = asyncio.Lock()
        if options.pop('load_later', False):
            self.loop.create_task(self.load())
        else:
            self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.name, 'r') as f:
                self._db = json.load(f, object_hook=self.object_hook)
        except FileNotFoundError:
            self._db = {}

    async def load(self):
        with await self.lock:
            await self.loop.run_in_executor(None, self.load_from_file)

    def _dump(self):
        temp = '%s-%s.tmp' % (uuid.uuid4(), self.name)
        with open(temp, 'w', encoding='utf-8') as tmp:
            json.dump(self._db.copy(), tmp, ensure_ascii=True, cls=self.encoder, separators=(',', ':'))

        # atomically move the file
        os.replace(temp, self.name)

    async def save(self):
        with await self.lock:
            await self.loop.run_in_executor(None, self._dump)

    def get(self, key, *args):
        """Retrieves a config entry."""
        return self._db.get(str(key), *args)

    async def put(self, key, value, *args):
        """Edits a config entry."""
        self._db[str(key)] = value
        await self.save()

    async def remove(self, key):
        """Removes a config entry."""
        del self._db[str(key)]
        await self.save()

    def __contains__(self, item):
        return str(item) in self._db

    def __getitem__(self, item):
        return self._db[str(item)]

    def __len__(self):
        return len(self._db)

    def all(self):
        return self._db


class Giveaway:
    def __init__(self, bot):  # Initialise some variables
        self.bot = bot
        self.config = Database('giveaways')  # Create JSON Database called 'giveaways'
        self._giveaway_task = bot.loop.create_task(self.giveaway_loop())  # Finish off any unfinished giveaways from last run
        self.emoji = u'\U0001F389'  # Reaction emoji

    def has_permission():
        def predicate(ctx):
            roles_list = [role.name for role in ctx.author.roles]
            if 'Giveaways' in roles_list or ctx.author.permissions_in(ctx.channel).manage_guild == True:
                return True
            else:
                return False
        return commands.check(predicate)

    @commands.command(aliases=['g'])  # Alternate aliases that can be invoked to call the command
    @commands.guild_only()  # Can only be run on a server
    @has_permission()
    async def giveaway(self, ctx, length, *, description: str = 'Giveaway'):  # Giveaway command
        duration = parse_short_time(length)
        if duration == -1:
            cross_emoji = u"\u274C"
            await ctx.send(f'{cross_emoji} Failed to parse time from `{length}`')
        else:
            number_of_winners = re.findall('^[0-9]*[wW]\\s', description)
            if number_of_winners:
                winners = int(number_of_winners[0][:-2])
                description = description.replace(number_of_winners[0], '')
            else:
                winners = 1

            ends_at = ctx.message.created_at + datetime.timedelta(seconds=duration)

            embed = discord.Embed(title=description, description=f'React with {self.emoji} to win!', colour=0x4ba139, timestamp=ends_at)
            footer_text = (f'{winners} Winners | ' if winners > 1 else '') + 'Ends at'
            embed.set_footer(text=footer_text)

            pet_link = re.findall('https?:\\/\\/(?:www\\.)chickensmoothie\\.[a-z]{2,6}\\/viewpet.php\\?id=[0-9]*', description)
            if pet_link:
                image = await cs.image(pet_link[0])
                file = discord.File(image, filename='image.png')
                message = await ctx.send(file=file, embed=embed)
            else:
                message = await ctx.send(embed=embed)
            channel_id = message.channel.id
            await message.add_reaction(self.emoji)
            storage = f'{message.channel.id}/{message.id}'
            await self.config.put(ends_at.timestamp(), storage)

            if self._giveaway_task.done():
                self._giveaway_task = self.bot.loop.create_task(self.giveaway_loop(winners))

    async def giveaway_loop(self, number_of_winners=1):
        await self.bot.wait_until_ready()
        while self.config:
            oldest = min(self.config.all())
            until_end = float(oldest) - datetime.datetime.utcnow().timestamp()
            await asyncio.sleep(until_end)
            giveaway_data = self.config.get(oldest)
            channel_id = int(giveaway_data.split('/')[0])
            message_id = int(giveaway_data.split('/')[1])
            try:
                channel_object = [channel for channel in self.bot.get_all_channels() if channel.id == channel_id][0]
                message = await channel_object.get_message(message_id)
            except discord.NotFound:
                await self.config.remove(oldest)
                continue

            embed = message.embeds[0]
            footer_text = (f'{number_of_winners} Winners | ' if number_of_winners > 1 else '') + 'Ended at'
            embed.set_footer(text=footer_text)

            giveaway_desc = embed.title
            try:
                winners = await self.roll_user(message, number_of_winners)
            except NoWinnerFound:
                embed.description = 'No one won this giveaway!'
                await message.edit(embed=embed)
                await message.channel.send(f'No winner found for **{giveaway_desc}**!')
            else:
                embed_description = ('\n' if len(winners) > 1 else '') + '\n'.join([winners[x].mention for x in range(len(winners))])
                embed.description = f'Winner: {embed_description}'
                await message.edit(embed=embed)

                congrats_description = ', '.join([winners[x].mention for x in range(len(winners))])
                await message.channel.send(f'Congratulations {congrats_description}! You won **{giveaway_desc}**')
            finally:
                await self.config.remove(oldest)

    async def roll_user(self, message: discord.Message, number_of_winners):
        try:
            reaction = next(x for x in message.reactions if x.emoji == self.emoji)
        except StopIteration:
            raise NoWinnerFound('Coundn\'t find giveaway emoji on specified message')

        users = await reaction.users().filter(lambda x: not x.bot).flatten()
        if not users:
            raise NoWinnerFound('No human reacted with the giveaway emoji on this message')
        else:
            winners_list = []
            for _ in range(number_of_winners):
                try:
                    winner = random.choice(users)
                    winners_list.append(winner)
                    users.remove(winner)
                except IndexError:
                    pass

            return winners_list

    @giveaway.error
    async def giveaway_handler(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CheckFailure):
            embed = discord.Embed(title='Support', description='You don\'t have permission to run this command!', colour=0xff5252)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Giveaway(bot))
