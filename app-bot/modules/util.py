# util.py

from fileinput import filename
from inspect import signature

import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime, timedelta

from modules.NumericStringParser import NumericStringParser

import ast
import operator as op

import ssl

import wolframalpha



import pandas as pd

import re

from cns import *

import aiohttp

import logging

import matplotlib.pyplot as plt
from matplotlib_venn import venn3

import os

from typing import Dict, Any, Optional, List, Callable, Awaitable

client = commands.Bot(
    " ", intents=discord.Intents.all(), application_id=855450076011561001
)

nyc = tz.gettz("America/New_York")

global data
data = pd.DataFrame(columns=["content", "time", "author"])

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}


class Util(commands.Cog):
    """
    Utilities and helpful commands that mostly everyone can use!
    Do help Util for more info on what commands you can use!
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # TODO: fix the guild checking add Nonetype check

    @app_commands.command()
    @app_commands.guilds(discord.Object(id=754510720590151751))
    async def testun(self, interaction):
        #if await self.bot.is_prod_guild(interaction):
        #    return
        print("Test Command Works from util.")
        await interaction.response.send_message("Hello!")

    @commands.command(
        help="Get your own Data, and have it sent to you as an embed.",
        brief="Check Your Data",
    )
    async def getmydata(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        # if str(responseuser) not in cns.POWER_USERS:
        #    return
        print("attempting full data output.")

        member = responseuser

        # user = member.guild.get_user()

        em = discord.Embed(title="Member Data: ", color=member.color)
        # try:
        em.add_field(name="Member ID: ", value=member.id)
        em.add_field(name="Member Name: ", value=member.name)
        em.add_field(name="Member Nick: ", value=member.nick)
        em.add_field(name="disc: ", value=member.discriminator)
        em.add_field(name="bot: ", value=member.bot)
        em.add_field(name="Display Name: ", value=member.display_name)
        em.add_field(name="Mobile Status: ", value=member.mobile_status)
        em.add_field(name="Guild: ", value=member.guild.name)
        em.add_field(name="Account Age: ", value=member.created_at)
        # em.set_footer(text="Type `.role_shop` test", icon_url=ctx.guild.owner.avatar_url)

        # ctx.guild.owner.avatar_url
        await ctx.channel.send(embed=em)

        # TODO: FIX THIS

    # @commands.command(help="Test command for getting guild contexts.\nIt is only usable by Power Users.", brief="Power User Command")
    async def whereami(self, ctx):
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        print("self.guild:")
        print(self.bot.gpass)
        print(self.bot.gpass.id)
        print("ctx.guild:")
        print(ctx.guild)
        print(ctx.guild.id)

    @commands.command(
        help="The bot will send you a DM with the current time.",
        brief="The bot will send you a DM with the current time.",
    )
    async def dmme(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        now = datetime.datetime.now()
        current_time = str(now)
        await ctx.message.author.send(
            "I am DMing you. To make this unique, the time is " + current_time
        )

    @commands.command(
        help="Helps you do math! Type any math problem and see what happens!",
        brief="Does Math",
    )
    async def mathpls(self, ctx, mathproblem: str):
        if await self.bot.is_prod_guild(ctx):
            return
        print(mathproblem)
        math = mathproblem
        print(math)
        nsp = NumericStringParser()
        result = nsp.eval(math)
        response = result
        # responseuser = ctx.message.author
        await ctx.message.channel.send(response)

    @commands.command(
        help="Allows Power Users to send messages as KREBBOT.\nIt is only usable by Power Users.",
        brief="Power User Command",
    )
    async def echo(self, ctx):
        responseuser = ctx.message.author
        if str(responseuser) in cns.POWER_USERS:
            resp = ctx.message.content
            response = resp[6:]
            await ctx.message.channel.send(response)
            await ctx.message.delete()
        else:
            return

    @commands.command(
        help="Type |wa then ANY QUESTION, and WolframAlpha will answer it.",
        brief="WA, VERY FUN",
    )
    async def wa(self, ctx, *, query):
        if await self.bot.is_prod_guild(ctx):
            return

        try:
            async with ctx.typing():
                # username = str(ctx.message.author)
                client = wolframalpha.Client("UQ42PE-53LH275XRA")
                res = client.query(query)
                res2 = ""
                res3 = ""
                for pod in res.pods:
                    for sub in pod.subpods:
                        res3 = res3 + str(sub)
                        if res2 == next(res.results).text + "\n":
                            continue
                        res2 = res2 + next(res.results).text + "\n"
            if res2 != "":
                await ctx.channel.send("Simple Response:\n" + res2)
                # await ctx.channel.send("Attempting Big Response:\n" + res3)
            else:
                await ctx.channel.send("No Data to Return!")
        except Exception:
            response = "Unable to complete request as worded, try re-wording, or be more/less specific!"
            # await ctx.channel.send(username)
            # + "\n" + "Warnings:\n" + str(res.warnings))
            await ctx.channel.send(response)

    @commands.command(
        help="Input a hex code, and get back info on that color!",
        enabled=True,
        hidden=True,
    )
    async def getcolor(self, ctx, hex):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            return

        hexc = str(hex)

        async with aiohttp.ClientSession() as session:  # None
            urlp = "https://encycolorpedia.com/"
            urlp2 = urlp + hex
            print(urlp2)
            async with session.get(urlp2) as response:
                html = await response.text()
                #logging.basicConfig(
                #    filename="./logs/std.log",
                #    filemode="w",
                #    format="%(name)s - %(levelname)s - %(message)s",
                #)
                logging.warning(html)

                contentis = "<section id=information>"
                contenti = html.find(contentis)

                print(contenti)

                contenti2 = contenti + 488
                html2 = html[contenti:contenti2]

                # d1 = html2.split(
                d1 = re.split("([<>]*[<>])", html2)
                # print("REEE", d1)

                y = [s for s in d1 if len(s) > 5]
                y = [s for s in y if s != "/strong"]
                y = [s for s in y if s != "strong"]

                dp1 = y[1]
                dp2 = y[2]
                dp3 = y[3] + y[4] + y[5] + y[6] + y[7] + y[8] + y[9]

                l = len(html2)
                n = 0
                for i in y:
                    n += 1

                urlo = str(urlp2) + ".png"
                embed = discord.Embed(title="Color:", description=dp1)
                embed.add_field(name="Color Details:", value=dp3, inline=False)
                embed.set_image(url=urlo)
                embed.set_footer(text="Delivered by KREBBOT with love <3")

                await ctx.message.channel.send(embed=embed)

    @commands.command()
    async def r(self, ctx, hr, mn, sc, data="Default"):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            print("beep beep")
            # return
        if hr.startswith("0"):
            hr = hr[1:]
        if mn.startswith("0"):
            mn = mn[1:]
        if sc.startswith("0"):
            sc = sc[1:]
        input = f"datetime.time(hour={hr}, minute={mn}, second={sc}, tzinfo=nyc)"
        if eval(input) in cns.times:
            await ctx.channel.send("This time is reserved, try again!")
            return
        cns.times.append(eval(input))
        cns.timesdata.append(data)
        cns.timesusers.append(responseuser.id)
        await ctx.channel.send("Got it!")
        print("looky here")
        await self.bot.reload_extension("cores.tcore")

    @commands.command()
    async def schedule(self, ctx, start, end, inc):
        if await self.bot.is_prod_guild(ctx):
            return
        # print("Start\n" + str(start))
        # print("End\n" + str(end))
        # print("Inc\n" + str(inc))

        channel = ctx.message.channel

        start = start[3:-1]
        start = int(start)
        start = datetime.fromtimestamp(start)
        end = end[3:-1]
        end = int(end)
        end = datetime.fromtimestamp(end)
        inc = int(inc)

        await channel.send("Please react below to the time(s) that work for you!")

        while start <= end:
            msg = await channel.send("<t:" + str(int(datetime.timestamp(start))) + ">")
            await msg.add_reaction("👍")
            # start = start + inc
            start = start + timedelta(minutes=inc)

        # responseuser = ctx.message.author
        await channel.send("Done!")

    # @ commands.command()  # gets private channels
    async def sig(self, ctx):
        # response = self.bot.private_channels
        response = commands.command.__get__(signature)
        # response = .signature
        print(response)
        pass

    @commands.command()
    async def synccommands(self, ctx):
        guild=754510720590151751
        print("syncing commands")
        print(self.bot.tree)
        print(guild)
        tree = self.bot.tree
        await tree.sync(guild=self.bot.gpass)
        await tree.copy_global_to(guild=754510720590151751)

    @commands.command()
    async def apply(self, ctx):
        response = """
        What is your name? (This is the name you will go by in the ORG, not your legal name unless you wish to use it)

How old are you?

What are your pronouns?

What time zone do you reside in?

After you record your responses, enter |apply2 to continue. 
        """
        await ctx.channel.send(response)
    
    @commands.command()
    async def apply2(self, ctx):
        response = """
How did you hear about us? And if someone referred you to us, who was it?

Have you played in any ORGs before? If so, which ones? How did you place? Did you get any awards?

What is the biggest thing you learned from your past games? If you have never played before, what are you hoping to get out of this experience?

How competitive are you? Can you share a story with us that shows just how competitive or cutthroat you are as a person?
        
After you record your responses, enter |apply3 to continue. 
        """
        await ctx.channel.send(response)

    @commands.command()
    async def apply3(self, ctx):
        response = """
This season, we may have a few live or semi-live challenges that will take place in the evenings based on the EST time zone. What time(s) would you be available for these challenges?

In the past, we have had challenges that require the use of speakers and a microphone. Do you have access to each of those tools and feel comfortable using them?

This season, you may be able to act as a traitor and sabotage the rest of the cast. Would you like to be considered for this role?

Do you require or need any accommodations for challenges? An example of this would be needing modifications to a challenge involving colors if you have color blindness. 

Is there anyone in the ORG community you refuse to play with? 

Is there anything else you want to tell the Parks & Rec staff?

After you record your responses, enter |apply4 to submit your application! 
        """
        await ctx.channel.send(response)

    @commands.command()
    async def apply4(self, ctx):
        roleid = 1175277956948557865
        server = self.bot.get_guild(1175277956885651526)
        role = server.get_role(roleid)
        response = f"""
{role.mention} - We have a new completed application!
Thank you for applying to Parks&Recvivor 2!
        """
        await ctx.channel.send(response)

    @commands.command(name="🦝🦝🦝🦝🦝🦝🦝")
    async def rcc(self, ctx):
        roleid = 1175277956948557865
        server = self.bot.get_guild(1175277956885651526)
        role = server.get_role(roleid)
        response = f"""hi!
        """
        await ctx.channel.send(response)

    @app_commands.guilds(discord.Object(id=754510720590151751),discord.Object(id=1175277956885651526))
    @app_commands.command(name="convert_time")
    async def convert_time(self, interaction: discord.Interaction, time_str: str, from_zone: str, to_zone: str) -> None:
        """
        Converts a time from one timezone to another.

        Args:
            time_str: A string representing the time in the format "HH:MM".
            from_zone: A string representing the timezone the time is currently in.
            to_zone: A string representing the timezone the time should be converted to.

        Returns:
            A string representing the time in the converted timezone, or None if the conversion fails.
        """
        resp = ""
        try:
            # Parse the time string into a datetime object.
            time_obj = datetime.datetime.strptime(time_str, "%H:%M")
            # Get the timezone offsets for the two timezones.
            from_offset = self.get_offset_from_utc(from_zone)
            to_offset = self.get_offset_from_utc(to_zone)
            # Calculate the difference between the two offsets.
            offset_diff = to_offset - from_offset
            # Add the offset difference to the time object.
            converted_time = time_obj + offset_diff
            # Format the converted time as a string.
            t = converted_time.strftime("%H:%M")
        except ValueError:
            t = None
            print("valerr")

        print(t)
        
        if t:
            resp = f"{time_str} {from_zone} is {t} {to_zone}"
        else:
            resp = "Invalid time or timezone format."

        await interaction.response.send_message(resp)

    def get_offset_from_utc(self, timezone):
        """
        Gets the timezone offset from UTC for a given timezone abbreviation.
        """

        # Implement your logic to determine the offset based on the timezone abbreviation.
        # You can use a mapping, a database, or external libraries like pytz.
        # For example, using a mapping:
        print("HIII")
        timezone_offsets = {
            "PST": -8,  # Pacific Standard Time
            "PDT": -7,  # Pacific Daylight Time
            "MST": -7,  # Mountain Standard Time
            "MDT": -6,  # Mountain Daylight Time
            "CST": -6,  # Central Standard Time
            "CDT": -5,  # Central Daylight Time
            "EST": -5,  # Eastern Standard Time
            "EDT": -4,  # Eastern Daylight Time
            "UTC": 0,   # Coordinated Universal Time
            "GMT": 0,   # Greenwich Mean Time
            "BST": 1,   # British Summer Time
            "CET": 1,   # Central European Time
            "CEST": 2,  # Central European Summer Time
            "EET": 2,   # Eastern European Time
            "EEST": 3,  # Eastern European Summer Time
            "MSK": 3,   # Moscow Standard Time
            "IST": 5.5,  # Indian Standard Time
            "KST": 9,   # Korea Standard Time
            "JST": 9,   # Japan Standard Time
            "AEST": 10,  # Australian Eastern Standard Time
            "AEDT": 11,  # Australian Eastern Daylight Time
            "NZST": 12,  # New Zealand Standard Time
            "NZDT": 13,  # New Zealand Daylight Time
        }
        return timedelta(hours=timezone_offsets.get(timezone, 0))  # Use 0 as a default offset if not found


    @commands.command()
    async def userdiff(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return

        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            return
        c = ctx.message.channel

        # hi
        l1 = []
        l2 = []
        l3 = [181157857478049792]
        for guild in self.bot.guilds:
            if guild.id == 754510720590151751:
                l1 = guild.members
            if guild.id == 843927271483113472:
                l2 = guild.members

        # Create the Venn diagram
        venn = venn3(
            [set(l1), set(l2), set(l3)], set_labels=("List 1", "List 2", "List 3")
        )

        # Display the Venn diagram
        # e = plt.show()
        plt.savefig("./media/chart.png")
        # imgplot = plt.imshow(img)

        # data_stream.seek(0)
        chart = discord.File("chart.png", filename="./media/chart.png")

        await c.send(file=chart)

        # embed = discord.Embed(title="Testing:", description="Test")
        # embed.set_author(name="TEST AUTHOR")
        # embed.add_field(name="TestFieldName", value=html, inline=False)
        # embed.set_image(url="attachment://unemployment_chart.png")
        # embed.set_footer(text="Delivered by KREBBOT with love <3")
        # plt.savefig
        # await c.send(embed=embed)

        # lists = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]


async def setup(bot):
    await bot.add_cog(Util(bot))
