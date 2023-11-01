# auto rules handler

import discord
from discord.ext import commands
from datetime import datetime
import os
import sys
import random

from typing import Optional, Union

from database.db import Db
# insertdb, selectdb, parseinsertsql, testsql, insertdb2

import pandas as pd

import csv

import re

from cns import *


class Rules(commands.Cog):
    """
    Rules handler
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(help="Basic test command to confirm that the module is loaded and responding.\nIt is only usable by Power Users.", brief="Power User Command", hidden=True)
    async def testrules(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return

    @commands.command(help="Request Rules to be sent to DM", brief="Rules", aliases=['rules'])
    async def checkrules(self, ctx, arg: Optional[discord.Member]):
        if await self.bot.is_prod_guild(ctx):
            return

        if arg == None:
            responseuser = ctx.message.author
        else:
            if str(ctx.message.author) not in cns.POWER_USERS:
                responseuser = None
                return
            else:
                responseuser = arg

        member = responseuser

        await member.send(cns.rules)


async def setup(bot):
    await bot.add_cog(Rules(bot))
