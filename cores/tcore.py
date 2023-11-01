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
global times
global timesdata
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

    global times
    global timesdata

    ## TODO: Known issue of line 62 print times[1] returning an error
    @tasks.loop(time=times)
    async def dmr(self):
        try:
            c = datetime.datetime.now()
            global times
            global timesdata
            print(times[1])
            print("IN LOOP")

            c2 = c.strftime("%H:%M")
            c = c.strftime("%H:%M:%S")
            c = str(c)
            c2 = str(c2)

            timesc = [str(item) for item in times]
            index = timesc.index(c)
            b = times[index]
            b = str(b)
            b2 = b[:5]

            if b2 == c2:
                response = "This is a reminder:\n" + timesdata[index]
                target = self.bot.get_user(181157857478049792)
                await target.send(response)
                if index != 0:
                    times.pop(index)
                    timesdata.pop(index)
                await asyncio.sleep(2)
                await self.bot.reload_extension("cores.tcore")
            else:
                pass
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    @dmr.before_loop
    async def before_dmr(self):
        global times
        global timesdata
        print("waiting for DMR...")
        print("contents of times:\n")
        print(times)
        print("contents of timesdata:\n")
        print(timesdata)
        await self.bot.wait_until_ready()

    @dmr.after_loop
    async def after_dmr(self):
        print("DM Loop Done")

    @commands.command()
    async def r(self, ctx, hr, mn, data="Default"):
        global times
        global timesdata
        if ctx.guild.id in cns.PROD_GUILDS:
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            return

        input = f"datetime.time(hour={hr}, minute={mn}, second=00, tzinfo=nyc)"
        global times
        global timesdata
        times.append(eval(input))
        timesdata.append(data)
        await ctx.channel.send("Got it!")
        await self.bot.reload_extension("cores.tcore")

    @commands.command()
    async def unstacktime(self, ctx, num=1):
        global times
        global timesdata
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
                times.pop(i)
                timesdata.pop(i)
                i -= 1
            await self.bot.reload_extension("cores.tcore")

    @commands.command()
    async def resetr(self, ctx, num=1):
        global times
        global timesdata
        if ctx.guild.id in cns.PROD_GUILDS:
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print("Returning due to lack of Power User permissions.")
            return
        if len(times) == 0:
            print("List is Empty.")
        else:
            times = [
                datetime.time(hour=5, minute=00, second=00, tzinfo=nyc),
            ]
            timesdata = [
                "First Row!",
            ]
            await self.bot.reload_extension("cores.tcore")


async def setup(bot):
    await bot.add_cog(Loops(bot))
