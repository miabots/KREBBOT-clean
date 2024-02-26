# run_bot.py
# this should be run to run the bot, it is basically the bot loop.

import asyncio

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

import signal
import logging

path = "./"
load_dotenv(path + ".env")

print(os.environ)

now = datetime.datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

print("ARGS")
print(sys.argv)

app_env = sys.argv[1]
print("app_env")
print(app_env)

if app_env == "beta":
    TOKEN = os.getenv("DISCORD_TOKEN_BETA")
    branch = "beta"
    command_prefix = "$"
elif app_env == "live":    
    TOKEN = os.getenv("DISCORD_TOKEN")
    branch = "live"
    command_prefix = "|"
else:
    #fallback to beta if there is an issue with args
    print("Falling back to beta")
    TOKEN = os.getenv("DISCORD_TOKEN_BETA")
    branch = "beta"
    command_prefix = "$"

intents = discord.Intents.all()
intentz = intents

client = commands.Bot(" ", intents=intents)

tree = client.tree

bot = Bot(command_prefix, TOKEN, branch, slash_commands=True, tree=tree)

#handle docker SIGTERM
def shutdown_handler(signal_number, frame, bot=bot):
    try:
        if signal_number == signal.SIGTERM:
            print("SIGTERM received, shutting down.")
            cleanup_task = asyncio.create_task(cleanup())
            sys.exit(0)
    except Exception as e:
        print(f"Error during shutdown: {e}")
        sys.exit(1)

async def cleanup(bot=bot):
    print("Cleaning up...")
    try:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="RESTARTING"))
        await bot.close()
        #sys.exit(0)
    except Exception as e:
        print(f"Error during cleanup: {e}")

signal.signal(signal.SIGTERM, shutdown_handler)
async def main():
    async with bot:
        try:
            await bot.start(TOKEN)  # loop.run_until_complete(bot.start())
        except Exception:
            traceback.print_exc()
            
asyncio.run(main())
