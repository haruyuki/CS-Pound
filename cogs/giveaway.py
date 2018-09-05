import datetime
import random
import re

import asyncio
import discord
from discord.ext import commands

from library import parse_short_time
import chickensmoothie as cs


class NoWinnerFound(Exception):
    pass


class Giveaway:
    def __init__(self, bot):  # Initialise some variables
        self.bot = bot
        self.emoji = u'\U0001F389'  # Reaction emoji

    def has_permission(self):
        def predicate(ctx):
            roles_list = [role.name for role in ctx.author.roles]
            if 'Giveaways' in roles_list or ctx.author.permissions_in(ctx.channel).manage_guild:
                return True
            else:
                return False
        return commands.check(predicate)

    @commands.command(aliases=['g', 'gstart'])  # Alternate aliases that can be invoked to call the command
    @commands.guild_only()  # Can only be run on a server
    @has_permission()
    async def giveaway(self, ctx, length, *, description: str = 'Giveaway'):  # Giveaway command
        add_reactions = False
        read_message_history = False
        guild_roles = ctx.message.guild.roles
        for role in guild_roles:
            if role.name == "CS Pound":
                add_reactions = role.permissions.add_reactions
                read_message_history = role.permissions.read_message_history

        if add_reactions and read_message_history:
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

                pet_link = re.findall('https?://(?:www\\.)chickensmoothie\\.[a-z]{2,6}/viewpet.php\\?id=[0-9]*', description)
                if pet_link:
                    image = await cs.image(pet_link[0])
                    file = discord.File(image, filename='image.png')
                    message = await ctx.send(file=file, embed=embed)
                else:
                    message = await ctx.send(embed=embed)

                until_end = float(ends_at.timestamp()) - datetime.datetime.utcnow().timestamp()

                await message.add_reaction(self.emoji)
                await asyncio.sleep(until_end)

                message = await message.channel.get_message(message.id)
                embed = message.embeds[0]
                giveaway_title = embed.title

                try:
                    winners = await self.roll_user(message, winners)
                except NoWinnerFound:
                    embed.description = 'No one won this giveaway!'
                    await message.edit(embed=embed)
                    await message.channel.send(f'No winner found for **{giveaway_title}**!')
                else:
                    embed_description = ('\n' if len(winners) > 1 else '') + '\n'.join([winners[x].mention for x in range(len(winners))])
                    embed.description = f'Winner: {embed_description}'
                    await message.edit(embed=embed)

                    congrats_description = ', '.join([winners[x].mention for x in range(len(winners))])
                    await message.channel.send(f'Congratulations {congrats_description}! You won **{giveaway_title}**')

        else:
            embed = discord.Embed(title='Giveaway', description='I don\'t have permission to create giveaways! Please ask the owner or admin to enable \'Add Reactions\' and \'Read Message History\'!')
            await ctx.send(embed=embed)

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
                    winner = random.SystemRandom().choice(users)
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
