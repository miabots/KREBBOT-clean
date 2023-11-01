# util.py

from fileinput import filename
from inspect import signature
from msilib.schema import Error
from sqlite3 import Timestamp

import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime, timedelta

from modules.utils.NumericStringParser import NumericStringParser

import ast
import operator as op

import ssl

import wolframalpha

from database.db import Db

import pandas as pd

from pandas.io.json import json_normalize
import json

import requests

import csv

import re

from cns import *

import msilib

import io

import json

import numpy as np

from sklearn.datasets import load_iris

import asyncio
import aiohttp

import logging

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib_venn import venn3


from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc
import os

from typing import Dict, Any, Optional, List, Callable, Awaitable

client = commands.Bot(
    " ", intents=discord.Intents.all(), application_id=855450076011561001
)

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

    def check_splcharacter(test):
        string_check = re.compile("[@_!#$%^&*()<>?/\|}{~:]")

        if string_check.search(test) == None:
            return True
        else:
            return False

    def check_splcharacter2(self, test):
        string_check = re.compile(".[@!#$%^&*()<>?/\|}{~:]")

        if string_check.search(test) == None:
            return True
        else:
            return False

    # TODO: fix the guild checking add Nonetype check

    @commands.command(hidden=True)
    async def testu(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        print("Test Command Works from util.")
        pass

    @commands.command(hidden=True)
    async def testcall(self, ctx, pl):
        if await self.bot.is_prod_guild(ctx):
            return
        async with self.bot.session as session:
            async with session.get("http://127.0.0.1:4444") as response:
                print("Status:", response.status)
                print("Content-type:", response.headers["content-type"])

                html = await response.text()
                print("Body:", html[:15], "...")

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

        # color=discord.Colour.random()
        # for role in [role for role in members.roles if role.name in roles.keys()]:
        # em.add_field(name=f"{role} : ", value=roles[role])
        # total += roles[role]
        await ctx.channel.send(embed=em)
        #  except:
        #      await ctx.channel.send(msilib.Fetch(Error))
        # for attr in responseuser:
        #    print(attr)
        #    print("\n")
        pass

        # TODO: FIX THIS

    # @commands.command(help="Test command for getting guild contexts.\nIt is only usable by Power Users.", brief="Power User Command")
    async def whereami(self, ctx):
        # if await self.bot.is_prod_guild(ctx):
        #    return
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
            peepee = ctx.message.content
            response = peepee[6:]
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
        enabled=False,
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

        async with None as session:  # aiohttp.ClientSession() as session:
            # urlp = 'http://python.org'
            urlp = "https://encycolorpedia.com/"
            urlp2 = urlp + hex
            print(urlp2)
            async with session.get(urlp2) as response:
                #  print("Status:", response.status)
                #  print("Content-type:", response.headers['content-type'])

                html = await response.text()
                # resp_dict = json.loads(html)
                # print("HTML PAYLOAD:\n", html[:20])
                logging.basicConfig(
                    filename="std.log",
                    filemode="w",
                    format="%(name)s - %(levelname)s - %(message)s",
                )
                logging.warning(html)

                contentis = "<section id=information>"
                contenti = html.find(contentis)

                # print(contenti)

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

                # print("NEW\n", y)

                # print("dp1", dp1)

                # print("dp2", dp2)

                # print("dp3", dp3)

                # print(html2)

                l = len(html2)

                # soup = bs(response, features='all')
                # print(soup)
                # soup = BS(html2)
                # elem = soup.findAll('a', {'

                # print("MAP\n")
                n = 0
                for i in y:
                    #   print(i, " : ", n)
                    # print(html2[n])
                    n += 1

                urlo = str(urlp2) + ".png"
                embed = discord.Embed(title="Color:", description=dp1)
                # embed.set_author(name="TEST AUTHOR")
                # embed.add_field(name="Color Code and Name:", value=dp1, inline=False)
                embed.add_field(name="Color Details:", value=dp3, inline=False)
                embed.set_image(url=urlo)
                # embed.set_thumbnail(url=thumburl)
                embed.set_footer(text="Delivered by KREBBOT with love <3")

                await ctx.message.channel.send(embed=embed)

    @commands.command(help="asdasd", brief="asdasd", hidden=True)
    async def es(self, ctx):
        responseuser = ctx.message.author
        if str(responseuser) in cns.POWER_USERS:
            peepee = ctx.message.content
            cap = str(peepee[4:]).lower()
            letdict = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]

            cap = [":regional_indicator_" + i + ":" for i in cap if i in letdict]

            cap = "".join(cap)

            response = cap
            await ctx.message.channel.send(response)
            # await ctx.message.delete()
        else:
            return

    @commands.command()
    async def synccommands(self, ctx):
        # await ctx.bot.tree.copy_global_to_guild()
        await ctx.bot.tree.sync(guild=discord.Object(id=754510720590151751))

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
        plt.savefig("chart.png")
        # imgplot = plt.imshow(img)

        # data_stream.seek(0)
        chart = discord.File("chart.png", filename="chart.png")

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
