# blastoff beta.py
# this should be run to run the bot, it is basically the bot loop.

import asyncio
import concurrent.futures

import os
import sys

from dotenv import load_dotenv

import discord

# from discord import app
from discord.ext import commands
from discord import app_commands

from datetime import datetime

import traceback

# import local modules
from cns import *
from bot import Bot

path = "./"
load_dotenv()

now = datetime.datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#TurtleScreen._RUNNING = True

app_env = sys.argv[1]
print("app_env")
print(app_env)

if app_env == "Beta":
    TOKEN = os.getenv("DISCORD_TOKEN_BETA")
    branch = "Beta"
    command_prefix = "$"
else:    
    TOKEN = os.getenv("DISCORD_TOKEN")
    branch = "Live"
    command_prefix = "|"

intents = discord.Intents.all()
intentz = intents

client = commands.Bot(" ", intents=intents)

clientz = discord.Client(intents=intents)

treez = app_commands.CommandTree(clientz)

tree = client.tree

pool = concurrent.futures.ThreadPoolExecutor()



bot = Bot(command_prefix, TOKEN, branch, slash_commands=True, tree=tree)


async def main():
    async with bot:
        try:
            await bot.start(TOKEN)  # loop.run_until_complete(bot.start())
        except Exception:
            traceback.print_exc()


asyncio.run(main())
