import asyncio
import discord
from discord.ext import commands
import hashlib
import subprocess


class AutoRemind:
    def __init__(self, bot):
        self.bot = bot
        self._auto_remind_task = bot.loop.create_task(self.pound_countdown())
        self.autoremind_hash = ''
        self.autoremind_times = []

    @commands.command()
    @commands.guild_only()
    async def autoremind(self, ctx, args=''):
        grep_statement = f'grep -n "{ctx.message.author.id}" autoremind.txt | cut -f1 -d:'  # Get line number of ID
        id_exists = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1]  # Run grep statement
        guild_roles = ctx.message.guild.roles  # List of roles in guild
        for role in guild_roles:  # For each role in the guild
            if role.name == "CS Pound":  # If 'CS Pound' role exists
                permission = role.permissions.manage_roles  # Check whether role has 'Manage Roles' permission and set boolean value
                break  # Break out of for loop
        else:  # If role doesn't exist
            permission = False

        if permission:  # If bot has permission to 'Manage Roles'
            guild_roles = ctx.message.guild.roles  # List of roles in guild
            for role in guild_roles:  # Checks if role already exists in guild
                if role.name == "Auto Remind":  # If role exists
                    break  # Break out of for loop
            else:  # If role doesn't exist
                await self.bot.create_role(ctx.message.guild, name='Auto Remind')  # Create 'Auto Remind' role in guild

        if args == 'off':  # If user wants to turn off Auto Remind
            if id_exists == '':  # If user doesn't exist in database
                embed = discord.Embed(title='Auto Remind', description='You don\'t have Auto Remind setup {0.mention}!'.format(ctx.message.author), colour=0xff5252)  # Create embed
            else:  # If user exists
                sed_statement = 'sed -i.bak ' + id_exists + 'd autoremind.txt'  # sed statement
                subprocess.Popen(sed_statement, shell=True)  # Run sed statement
                if permission:  # If bot has permission to 'Manage Roles'
                    await ctx.message.author.remove_roles(discord.utils.get(guild_roles, name='Auto Remind'), reason='User disabled Auto Remind.')  # Remove role from user
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
                        embed = discord.Embed(title='Auto Remind', description='You already have Auto Remind setup {0.mention}!'.format(ctx.message.author), colour=0xff5252)  # Create embed
                    else:  # If user doesn't have an Auto Remind setup
                        text = f'{ctx.message.guild.id} {ctx.message.channel.id} {ctx.message.author.id} {args}' + '\n'  # Write in the format 'GUILD_ID CHANNEL_ID USER_ID REMIND_TIME'
                        with open('autoremind.txt', 'a+') as file:  # Open autoremind.txt
                            file.write(text)  # Write the text

                        if permission:  # If bot has 'Manage Roles' permission
                            await ctx.message.author.add_roles(discord.utils.get(guild_roles, name='Auto Remind'), reason='User enabled Auto Remind.')  # Add user to Auto Remind role

                        message = 'Will ping you ' + args + ' minutes before the pound opens!'
                        embed = discord.Embed(title='Auto Remind', description=message, colour=0x4ba139)  # Create embed

        await ctx.send(embed=embed)  # Send embed


    async def compose_message(self, time):  # Function to compose and send mention messages to channels
        grep_statement = 'grep \'[0-9]*\\s[0-9]*\\s[0-9]*\\s' + time + '\' autoremind.txt | cut -f2 -d\' \' | sort -u'  # Get channels with Auto Remind set at 'time'
        channel_ids = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run grep statement
        for i in range(len(channel_ids)):  # For each Discord channel ID
            grep_statement = 'grep \'[0-9]*\\s' + channel_ids[i] + '\\s[0-9]*\\s' + time + '\' autoremind.txt | cut -f3 -d\' \''  # Grab all unique Discord user ID's with that channel ID
            user_ids = subprocess.Popen(grep_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run grep statement
            if time == '1':  # If there is only one minute left
                message = time + ' minute until pound opens! '
            else:  # If there is more than 1 minute left
                message = time + ' minutes until pound opens! '
            for j in range(len(user_ids)):  # For each Discord user
                message += '<@' + user_ids[j] + '> '  # Message format for mentioning users | <@USER_ID>
            await self.bot.get_channel(int(channel_ids[i])).send(message)  # Send message to Discord channel with mention message


    async def minute_check(self, time):  # Function to check if any user has Auto Remind setup at 'time'
        time = str(time)
        new_hash = hashlib.md5(open('autoremind.txt').read().encode()).hexdigest()  # MD5 hash of autoremind.txt
        if self.autoremind_hash != new_hash:  # If file has been modified since last check
            self.autoremind_hash = new_hash
            cut_statement = 'cut -f4 -d\' \' autoremind.txt | sort -u'  # Grab all unique reminding times from autoremind.txt
            self.autoremind_times = subprocess.Popen(cut_statement, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')[:-1].split('\n')  # Run cut statement

        if time in self.autoremind_times:  # If someone has a Auto Remind set at current 'time'
            await self.compose_message(time)  # Run compose message


    async def pound_countdown(self):  # Background task to countdown to when the pound opens
        global cooldown  # Use cooldown from global scope
        await self.bot.wait_until_ready()  # Wait until bot has loaded before starting background task
        while not self.bot.is_closed:  # While bot is still running
            if not cooldown:  # If command is not on cooldown
                data = await get_web_data('', 'pound')  # Get pound data
                if data[0]:  # If pound data is valid and contains content
                    text = data[1].xpath('//h2/text()')  # List all texts with H2 element
                    try:  # Try getting pound opening text
                        text = text[1]  # Grab the pound opening time text
                        value = [int(s) for s in text.split() if s.isdigit()]  # Extract the numbers in the text
                        if len(value) == 1:  # If there is only one number
                            value = value[0]
                            if 'hour' in text:  # If hour in pound opening time
                                if value == 1:  # If there is one hour left
                                    cooldown = True
                                    value = 60  # Start countdown from 60 minutes
                                    sleep_amount = 0
                                else:  # If there is more than one hour
                                    sleep_amount = (value - 2) * 3600  # -1 hour and convert into seconds
                            elif 'minute' in text:  # If minute in pound opening time
                                sleep_amount = 0
                                cooldown = True
                            elif 'second' in text:  # If second in pound opening time
                                pass
                        elif len(value) == 2:  # If there are two numbers
                            if 'hour' and 'minute' in text:
                                sleep_amount = value[1] * 60  # Get the minutes and convert to seconds
                                value = 60
                                text = 'minute'
                                cooldown = True
                            elif 'minute' and 'second' in text:
                                pass
                        elif len(value) == 0:  # If there are no times i.e. Pound recently closed or not opening anytime soon
                            sleep_amount = 3600  # 1 hour
                    except IndexError:  # Pound is currently open
                        sleep_amount = 3600  # 1 hour
                else:  # If pound data isn't valid
                    sleep_amount = 11400  # 3 hours 10 minutes
            else:  # If command is on cooldown
                if 'hour' in text:  # If hour in text
                    if value != 0:  # If minutes left is not zero
                        await self.minute_check(value)  # Run minute check
                        value -= 1  # Remove one minute
                        sleep_amount = 60  # 1 minute
                    else:  # If time ran out (i.e. Pound is now open)
                        cooldown = False
                        sleep_amount = 10800  # 3 hours
                elif 'minute' and 'second' in text:  # If minute and second in text
                    sleep_amount = value[1]
                    value = 1
                elif 'minute' in text:  # If minute in text
                    if value != 0:  # If minutes left is not zero
                        await self.minute_check(value)  # Run minute check
                        value -= 1  # Remove one minute
                        sleep_amount = 60  # 1 minute
                    else:  # If time ran out (i.e. Pound is now open)
                        cooldown = False
                        sleep_amount = 10800  # 3 hours
                elif 'second' in text:  # If second in text
                    pass
            await asyncio.sleep(sleep_amount)  # Sleep for sleep amount


def setup(bot):
    bot.add_cog(AutoRemind(bot))
