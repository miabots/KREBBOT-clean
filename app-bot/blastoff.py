import asyncio
import concurrent.futures

import os

from dotenv import load_dotenv

import discord
#from discord import app
from discord.ext import commands
from discord import app_commands

from datetime import datetime

import traceback

# import local modules ?
from cns import *
from bot import Bot

path = './'
load_dotenv()

now = datetime.datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intentz = intents

client = commands.Bot(" ", intents=intents)

tree = client.tree

pool = concurrent.futures.ThreadPoolExecutor()

bot = Bot('|', 'DISCORD_TOKEN', 'Live', slash_commands=True, tree=tree)  # , =[754510720590151751])


async def main():
    async with bot:
        try:
            await bot.start(TOKEN)  # loop.run_until_complete(bot.start())
        except Exception:
            traceback.print_exc()

asyncio.run(main())
