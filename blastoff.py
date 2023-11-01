# blastoff.py
# this should be run to run the bot, it is basically the bot loop.
import asyncio
import concurrent.futures
import turtle
from turtle import *
from _tkinter import *
import random
import os
#from discord.player import FFmpegAudio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from PIL import Image
from datetime import datetime

import traceback

import azure

# discord modules from 3rd parties
#from pretty_help import DefaultMenu, PrettyHelp


# import local modules
from cns import *
from bot import Bot


from turtley import *

from database.db import Db
#initdb, insertdb, selectdb, parseinsertsql, testsql, insertdb2

# init db

# def __init__(self, bot: commands.Bot) -> None:
#    print("HELLO IS THIS THING ON???")

from modules.utils.context import Context

from typing import Dict, Any, Optional, List, Callable, Awaitable

#import discord
#from discord import ui

#from discord_ui import UI

#import pretty_errors


#t = discord.User()

path = './'
load_dotenv()

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

TurtleScreen._RUNNING = True

# Load Secrets via Environment Variables in .env


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Turn on intents?


intents = discord.Intents.all()
intents.members = True
intents.voice_states = True

#intents = discord.Intents.none()

intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.members = True
intents.voice_states = True
intents.guild_messages = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.members = True
intents.voice_states = True
intents.webhooks = True

intentz = intents

# For now, until I can get Bot classes to work, do a simple Bot creation

#bot = commands.Bot(command_prefix=commands.when_mentioned_or('|'), intents=intents)

#bot = commands.Bot(command_prefix=commands.when_mentioned_or('|'), slash_commands=False, intents=intents)

#bot = MyBot(command_prefix=commands.when_mentioned_or('|'), intents=intents)


client = commands.Bot(" ", intents=intents)

pool = concurrent.futures.ThreadPoolExecutor()


if __name__ == "__main__":
    bot = Bot()
    try:
        bot.loop.run_until_complete(bot.start())

    except Exception:
        traceback.print_exc()
    finally:
        bot.loop.run_until_complete(bot.close())
        bot.loop.close()
