# ecore.py
# auto-emote parsing

import random
from datetime import datetime

import psycopg2

import discord
from discord.ext import commands

from cns import *

import rich

from rich import print as print

global pingmode
pingmode = False


class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.intents = bot.intents

    @ commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id == 855450076011561001:
            return

        # notte ID 181157857478049792
        if message.guild is None:
            return

        else:  # guild found

            if await self.bot.is_prod_guild(message):
                return

            if message.content == ':popcat:':
                response = '<a:popCat:839937844428013589>'
                await message.delete()
                await message.channel.send(response)


async def setup(bot):
    await bot.add_cog(Emotes(bot))
