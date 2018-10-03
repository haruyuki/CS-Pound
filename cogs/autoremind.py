import subprocess

import discord
from discord.ext import commands
import motor.motor_asyncio as amotor

from constants import Constants
from library import pound_countdown

mongo_client = amotor.AsyncIOMotorClient(Constants.mongodb_uri)
database = mongo_client['cs_pound']
collection = database['test']


class AutoRemind:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ar'])
    @commands.guild_only()  # Command can only be run in guilds
    async def autoremind(self, ctx, args=''):
        id_exists = await collection.find({'_id': str(ctx.author.id)})  # Get document of user
        try:
            id_exists = id_exists[0]
        except IndexError:
            pass
        print(f'DOCUMENT: {id_exists}')
        guild_roles = ctx.guild.roles  # List of roles in guild
        embed = discord.Embed()
        for role in guild_roles:  # For each role in the guild
            if role.name == "CS Pound":  # If 'CS Pound' role exists
                permission = role.permissions.manage_roles  # Check whether role has 'Manage Roles' permission and set boolean value
                break  # Break out of for loop
        else:  # If role doesn't exist
            permission = False

        if permission:  # If bot has permission to 'Manage Roles'
            guild_roles = ctx.guild.roles  # List of roles in guild
            for role in guild_roles:  # Checks if role already exists in guild
                if role.name == "Auto Remind":  # If role exists
                    break  # Break out of for loop
            else:  # If role doesn't exist
                await ctx.guild.create_role(name='Auto Remind', reason='Auto Remind didn\'t exist')  # Create 'Auto Remind' role in guild

        if args == 'off' or args == 'cancel':  # If user wants to turn off Auto Remind
            if id_exists == '':  # If user doesn't exist in database
                embed = discord.Embed(title='Auto Remind', description='You don\'t have Auto Remind setup {0.mention}!'.format(ctx.message.author), colour=0xff5252)  # Create embed
            else:  # If user exists
                sed_statement = 'sed -i.bak ' + id_exists + 'd autoremind.txt'  # sed statement
                subprocess.Popen(sed_statement, shell=True)  # Run sed statement
                if permission:  # If bot has permission to 'Manage Roles'
                    await ctx.author.remove_roles(discord.utils.get(guild_roles, name='Auto Remind'), reason='User disabled Auto Remind.')  # Remove role from user
                    embed = discord.Embed(title='Auto Remind', description='You have been removed from the Auto Remind role.', colour=0x4ba139)  # Create embed
                else:  # If bot doesn't have permission to 'Manage Roles'
                    embed = discord.Embed(title='Auto Remind', description='You have been removed from the Auto Remind.', colour=0x4ba139)  # Create embed

        else:  # If user is setting an Auto Remind
            valid = False
            if args == '':  # If no arguments provided
                embed = discord.Embed(title='Auto Remind', description='You didn\'t input a time!', colour=0xff5252)  # Create embed
            elif args.isdigit():  # If the input is a digit
                valid = True
            else:  # If the input isn't a digit
                args = args[:-1]  # Remove the minute marker
                if args.isdigit():  # If the input is a digit now
                    valid = True
                else:  # If input is still not digit
                    embed = discord.Embed(title='Auto Remind', description='That is not a valid time!', colour=0xff5252)  # Create embed

            if valid:  # If inputted time was valid
                if int(args) > 60:  # If time is bigger than 60 minutes
                    embed = discord.Embed(title='Auto Remind', description='That time is too far!', colour=0xff5252)  # Create embed
                else:  # If time is less than 60 minutes
                    if id_exists != '':  # If user has already set an Auto Remind
                        embed = discord.Embed(title='Auto Remind', description='You already have Auto Remind setup!'.format(ctx.message.author), colour=0xff5252)  # Create embed
                    else:  # If user doesn't have an Auto Remind setup
                        text = f'{ctx.message.guild.id} {ctx.message.channel.id} {ctx.message.author.id} {args}' + '\n'  # Write in the format 'GUILD_ID CHANNEL_ID USER_ID REMIND_TIME'
                        with open('autoremind.txt', 'a+') as file:  # Open autoremind.txt
                            file.write(text)  # Write the text

                        if permission:  # If bot has 'Manage Roles' permission
                            await ctx.author.add_roles(discord.utils.get(guild_roles, name='Auto Remind'), reason='User enabled Auto Remind.')  # Add user to Auto Remind role

                        message = 'Will ping you ' + args + ' minutes before the pound opens!'
                        embed = discord.Embed(title='Auto Remind', description=message, colour=0x4ba139)  # Create embed

        await ctx.send(embed=embed)  # Send embed


def setup(bot):
    bot.add_cog(AutoRemind(bot))
    bot.loop.create_task(pound_countdown(bot))
