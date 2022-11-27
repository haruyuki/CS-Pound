import aiohttp
import io
from PIL import Image
import textwrap
from urllib.parse import urlparse, parse_qsl, urlencode
import json
import math

import discord
from discord.ext import commands

from constants import Constants, FlightRisingC
import flightrising as fr


class FlightRising(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spreadsheet = Constants.google_sheets_api.open_by_key(
            "1fmcwLdExvnPRME64Ylzpx1o0bA8qUeqX8HwyQzz1hGc"
        )  # Link to conversion spreadsheet
        self.headers = {  # HTTP request headers
            "User-Agent": "CS Pound Discord Bot Agent "
            + Constants.version,  # Connecting User-Agent
            "From": Constants.contact_email,
        }

    def calculate_cs_to_gems(
        self, cs
    ):  # Function to calculate exchange rate from C$ to gems
        worksheet = self.spreadsheet.sheet1
        cs_exchange_rate = float(worksheet.get_value("E10"))
        gem_exchange_rate = float(worksheet.get_value("F10"))
        return (cs / cs_exchange_rate) * gem_exchange_rate

    def calculate_cs_to_treasure(
        self, cs
    ):  # Function to calculate exchange rate from C$ to treasure
        worksheet = self.spreadsheet.sheet1
        cs_exchange_rate = float(worksheet.get_value("E10"))
        gem_exchange_rate = float(worksheet.get_value("F10"))
        treasure_exchange_rate = float(worksheet.get_value("G10"))
        return ((cs / cs_exchange_rate) * gem_exchange_rate) * treasure_exchange_rate

    def calculate_gems_to_cs(
        self, gems
    ):  # Function to calculate exchange rate from gems to C$
        worksheet = self.spreadsheet.sheet1
        gem_exchange_rate = float(worksheet.get_value("F10"))
        cs_exchange_rate = float(worksheet.get_value("E10"))
        return (gems / gem_exchange_rate) * cs_exchange_rate

    def calculate_gems_to_treasure(
        self, gems
    ):  # Function to calculate exchange rate from gems to treasure
        worksheet = self.spreadsheet.sheet1
        treasure_exchange_rate = float(worksheet.get_value("G10"))
        return gems * treasure_exchange_rate

    def calculate_treasure_to_cs(
        self, treasure
    ):  # Function to calculate exchange rate from treasure to C$
        worksheet = self.spreadsheet.sheet1
        treasure_exchange_rate = float(worksheet.get_value("G10"))
        gem_exchange_rate = float(worksheet.get_value("F10"))
        cs_exchange_rate = float(worksheet.get_value("E10"))
        return (
            (treasure / treasure_exchange_rate) / gem_exchange_rate
        ) * cs_exchange_rate

    def calculate_treasure_to_gems(
        self, treasure
    ):  # Function to calculate exchange rate from treasure to gems
        worksheet = self.spreadsheet.sheet1
        treasure_exchange_rate = float(worksheet.get_value("G10"))
        return treasure / treasure_exchange_rate

    @commands.command()
    async def cs(self, ctx, amount: float):
        if amount.is_integer():  # Converts float into integer if decimal is 0
            amount = int(amount)

        gems = self.calculate_cs_to_gems(amount)
        treasure = self.calculate_cs_to_treasure(amount)
        message = f"""\
        {amount}C$ equates to approximately:
        {round(gems, 2)} gems
        {round(treasure, 2)} treasure"""
        message = textwrap.dedent(message)
        await ctx.send(message)

    @commands.command(aliases=["fr"])
    async def gems(self, ctx, amount: float):
        if amount.is_integer():  # Converts float into integer if decimal is 0
            amount = int(amount)

        cs = self.calculate_gems_to_cs(amount)
        treasure = self.calculate_gems_to_treasure(amount)
        message = f"""\
        {amount} gems equates to approximately:
        {round(cs, 2)}C$
        {round(treasure, 2)} treasure"""
        message = textwrap.dedent(message)
        await ctx.send(message)

    @commands.command(aliases=["tr"])
    async def treasure(self, ctx, amount: float):
        if amount.is_integer():  # Converts float into integer if decimal is 0
            amount = int(amount)

        cs = self.calculate_treasure_to_cs(amount)
        gems = self.calculate_treasure_to_gems(amount)
        message = f"""\
        {amount} treasure equates to approximately:
        {round(cs, 2)}C$
        {round(gems, 2)} gems"""
        message = textwrap.dedent(message)
        await ctx.send(message)

    @commands.command(aliases=["prog"])
    async def progeny(self, ctx, dragon1, dragon2, multiplier=10):
        if multiplier > 10:
            await ctx.send("The maximum multiplier is 10!")
            return

        if dragon1.isdigit():
            pass
        else:
            dragon1 = fr.extract_dragon_id(dragon1)

        if dragon2.isdigit():
            pass
        else:
            dragon2 = fr.extract_dragon_id(dragon2)

        outcomes = await fr.get_progeny(dragon1, dragon2, multiplier)

        if isinstance(outcomes, str):
            await ctx.send(outcomes)

        else:
            image_data = []
            async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
                for image in outcomes:
                    async with session.get(image, headers=self.headers) as response:
                        if response.status == 200:
                            content = await response.read()
                    content = io.BytesIO(content)
                    image_data.append(content)

            image = generate_image(image_data, multiplier)
            output_buffer = io.BytesIO()  # Convert the PIL output into bytes
            image.save(output_buffer, "png")  # Save the bytes as a PNG format
            output_buffer.seek(0)
            await ctx.send(file=discord.File(fp=output_buffer, filename="pet.png"))

    @commands.command(aliases=["cprog"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cprogeny(self, ctx, dragon1, dragon2, element="shadow"):
        elements = {
            "earth": "1",
            "plague": "2",
            "wind": "3",
            "water": "4",
            "lightning": "5",
            "ice": "6",
            "shadow": "7",
            "light": "8",
            "arcane": "9",
            "nature": "10",
            "fire": "11",
        }
        element = elements[element.lower()]

        if dragon1.isdigit():
            pass
        else:
            dragon1 = fr.extract_dragon_id(dragon1)

        if dragon2.isdigit():
            pass
        else:
            dragon2 = fr.extract_dragon_id(dragon2)

        outcomes = await fr.get_progeny(dragon1, dragon2, 5)

        image_data = []
        async with aiohttp.ClientSession() as session:  # Create an AIOHTTP session
            links = []
            for dragon in outcomes:
                components = urlparse(dragon)
                parameters = dict(parse_qsl(components.query))
                del parameters["auth"]
                del parameters["dummyext"]
                parameters["age"] = "0"
                parameters["element"] = element
                parameters["_token"] = FlightRisingC.token

                async with session.post(
                    FlightRisingC.cprogeny_url, data=parameters, headers=self.headers
                ) as response:
                    if response.status == 200:
                        content = await response.read()
                        content = json.loads(content)
                        links.append(
                            "https://www1.flightrising.com" + content["dragon_url"]
                        )

            for link in links:
                async with session.get(link, headers=self.headers) as response:
                    if response.status == 200:
                        content = await response.read()
                content = io.BytesIO(content)
                image_data.append(content)

        image = generate_image(image_data, 5)
        output_buffer = io.BytesIO()  # Convert the PIL output into bytes
        image.save(output_buffer, "png")  # Save the bytes as a PNG format
        output_buffer.seek(0)
        await ctx.send(file=discord.File(fp=output_buffer, filename="pet.png"))

    @cs.error  # On error with cs command
    @gems.error  # On error with gems command
    @treasure.error  # On error with treasure command
    async def command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):  # If user didn't pass a number
            await ctx.send("That is not a valid number!")

    @progeny.error  # On error with progeny command
    async def progeny_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing another dragon link/ID!")

    @cprogeny.error  # On error with cprogeny command
    async def cprogeny_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You're missing another dragon link/ID!")
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send("You didn't provide a valid flight!")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"The command is on cooldown! Please try again after {int(error.retry_after)} seconds."
            )


async def setup(bot):
    await bot.add_cog(FlightRising(bot))


def generate_image(image_data, multiplier):
    pil_images = list(map(Image.open, image_data))
    if multiplier > 5:
        if pil_images[0].width == 350:
            max_width = 2800
            max_height = 350 * 5
        else:
            max_width = 1400
            max_height = 175 * 5
    else:
        if pil_images[0].width == 350:
            max_width = 1400
            max_height = 350 * multiplier
        else:
            max_width = 700
            max_height = 175 * multiplier
    canvas = Image.new("RGBA", (max_width, max_height), (255, 0, 0, 0))

    current_width = 0
    y_offset = 0
    for i in pil_images:
        if current_width >= max_width:
            current_width = 0
            y_offset += i.width

        canvas.paste(i, (current_width, y_offset))
        current_width += i.width

    return canvas
