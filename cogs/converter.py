import json
import os
import textwrap

from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Converter:
    def __init__(self, bot):
        self.bot = bot
        self.spreadsheet = self.authorisation().open_by_key('1fmcwLdExvnPRME64Ylzpx1o0bA8qUeqX8HwyQzz1hGc')

    @staticmethod
    def authorisation():
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '{}')
        service_account_info = json.loads(credentials_raw)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
        return gspread.authorize(credentials)

    def calculate_cs_to_gems(self, cs):
        worksheet = self.spreadsheet.sheet1
        cs_exchange_rate = float(worksheet.acell('E10').value)
        gem_exchange_rate = float(worksheet.acell('F10').value)
        return (cs / cs_exchange_rate) * gem_exchange_rate

    def calculate_cs_to_treasure(self, cs):
        worksheet = self.spreadsheet.sheet1
        cs_exchange_rate = float(worksheet.acell('E10').value)
        gem_exchange_rate = float(worksheet.acell('F10').value)
        treasure_exchange_rate = float(worksheet.acell('G10').value)
        return ((cs / cs_exchange_rate) * gem_exchange_rate) * treasure_exchange_rate

    def calculate_gems_to_cs(self, gems):
        worksheet = self.spreadsheet.sheet1
        gem_exchange_rate = float(worksheet.acell('F10').value)
        cs_exchange_rate = float(worksheet.acell('E10').value)
        return (gems / gem_exchange_rate) * cs_exchange_rate

    def calculate_gems_to_treasure(self, gems):
        worksheet = self.spreadsheet.sheet1
        treasure_exchange_rate = float(worksheet.acell('G10').value)
        return gems * treasure_exchange_rate

    def calculate_treasure_to_cs(self, treasure):
        worksheet = self.spreadsheet.sheet1
        treasure_exchange_rate = float(worksheet.acell('G10').value)
        gem_exchange_rate = float(worksheet.acell('F10').value)
        cs_exchange_rate = float(worksheet.acell('E10').value)
        return ((treasure / treasure_exchange_rate) / gem_exchange_rate) * cs_exchange_rate

    def calculate_treasure_to_gems(self, treasure):
        worksheet = self.spreadsheet.sheet1
        treasure_exchange_rate = float(worksheet.acell('G10').value)
        return treasure / treasure_exchange_rate

    @commands.command()
    async def cs(self, ctx, amount: float):
        if amount.is_integer():
            amount = int(amount)

        gems = self.calculate_cs_to_gems(amount)
        treasure = self.calculate_cs_to_treasure(amount)
        message = f'''\
        {amount}C$ equates to approximately:
        {round(gems, 2)} gems
        {round(treasure, 2)} treasure'''
        message = textwrap.dedent(message)
        await ctx.send(message)

    @commands.command(aliases=['fr'])
    async def gems(self, ctx, amount: float):
        if amount.is_integer():
            amount = int(amount)

        cs = self.calculate_gems_to_cs(amount)
        treasure = self.calculate_gems_to_treasure(amount)
        message = f'''\
        {amount} gems equates to approximately:
        {round(cs, 2)}C$
        {round(treasure, 2)} treasure'''
        message = textwrap.dedent(message)
        await ctx.send(message)

    @commands.command(aliases=['tr'])
    async def treasure(self, ctx, amount: float):
        if amount.is_integer():
            amount = int(amount)

        cs = self.calculate_treasure_to_cs(amount)
        gems = self.calculate_treasure_to_gems(amount)
        message = f'''\
        {amount} treasure equates to approximately:
        {round(cs, 2)}C$
        {round(gems, 2)} gems'''
        message = textwrap.dedent(message)
        await ctx.send(message)

    @cs.error
    @gems.error
    @treasure.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('That is not a valid number!')


def setup(bot):
    bot.add_cog(Converter(bot))