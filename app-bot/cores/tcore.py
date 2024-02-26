# tcore.py
# core module for time loops

import discord
from discord.ext import commands, tasks
import asyncio
import re

import schedule

# import time
import datetime
import calendar

import time

import threading
import queue

import traceback

# import asyncpg

from typing import Dict, Any, Optional, List, Callable, Awaitable

from cns import *

# end imports
from dateutil import tz


nyc = tz.gettz("America/New_York")
utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.

times = cns.times
timesdata = cns.timesdata


class Loops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.lock = asyncio.Lock()
        self.data = []
        # self.batch_update.add_exception_type(asyncpg.PostgresConnectionError)
        # self.printer.start()
        self.dmr.start()

    def cog_unload(self):
        self.dmr.cancel()

    @tasks.loop(time=cns.times)
    async def dmr(self):
        try:
            c = datetime.datetime.now()
            print(c)
            # print(times[1])
            print("IN LOOP")
            c2 = c.strftime("%H:%M")
            c = c.strftime("%H:%M:%S")
            c = str(c)
            c2 = str(c2)

            timesc = [str(item) for item in cns.times]
            index = timesc.index(c)
            print("index: " + str(index))
            b = cns.times[index]
            b = str(b)
            b2 = b[:5]
            # print("b2: " + str(b2))
            # print("c2: " + str(c2))
            # print(cns.timesdata)
            time.sleep(2)
            # if b2 == c2:
            if b == c:
                print("match found")
                response = "This is a reminder:\n" + cns.timesdata[index]
                target = self.bot.get_user(cns.timesusers[index])
                await target.send(response)
                if index != 0:
                    cns.times.pop(index)
                    cns.timesdata.pop(index)
                    cns.timesusers.pop(index)
            else:
                print("match failed")

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    @dmr.before_loop
    async def before_dmr(self):
        global times
        global timesdata
        print("waiting for DMR...")
        print("contents of times:\n")
        print(cns.times)
        print("contents of timesdata:\n")
        print(cns.timesdata)
        print("contents of timesusers:\n")
        print(cns.timesusers)
        await self.bot.wait_until_ready()

    @dmr.after_loop
    async def after_dmr(self):
        print("reloading extension")
        await self.bot.reload_extension("cores.tcore")
        print("DM Loop Done")

    @commands.command()
    async def unstacktime(self, ctx, num=1):
        if ctx.guild.id in cns.PROD_GUILDS:
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            return
        if len(times) == 0:
            print("List is Empty.")
        else:
            i = num
            while i != 0:
                cns.times.pop(i)
                cns.timesdata.pop(i)
                cns.timesusers.pop(i)
                i -= 1
            await self.bot.reload_extension("cores.tcore")

    @commands.command()
    async def checkrems(self, ctx):
        global times
        global timesdata
        if ctx.guild.id in cns.PROD_GUILDS:
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            return
        print("contents of times:\n")
        print(times)
        print("contents of timesdata:\n")
        print(timesdata)
        print("contents of timesusers:\n")
        print(cns.timesusers)
        response = (
            "contents of times:\n"
            + str(times)
            + "\ncontents of timesdata:\n"
            + str(timesdata)
            + "\ncontents of timesusers:\n"
            + str(cns.timesusers)
        )
        await ctx.send(response)

    @commands.command()
    async def resetr(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            return
        if len(cns.times) == 0:
            print("List is Empty.")
        else:
            cns.times = [
                datetime.time(hour=5, minute=00, second=00, tzinfo=nyc),
            ]
            timesdata = [
                "First Row!",
            ]
            await self.bot.reload_extension("cores.tcore")


async def setup(bot):
    await bot.add_cog(Loops(bot))
