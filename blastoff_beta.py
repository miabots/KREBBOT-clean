# blastoff beta.py
# this should be run to run the bot, it is basically the bot loop.

import asyncio
import concurrent.futures

from turtle import *
from _tkinter import *

import os

# from discord.player import FFmpegAudio

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

# from modules.utils.context import Context

# from typing import Dict, Any, Optional, List, Callable, Awaitable

path = "./"
load_dotenv()

now = datetime.datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

TurtleScreen._RUNNING = True

TOKEN = os.getenv("DISCORD_TOKEN_BETA")

intents = discord.Intents.all()
intentz = intents

client = commands.Bot(" ", intents=intents)

clientz = discord.Client(intents=intents)

treez = app_commands.CommandTree(clientz)

tree = client.tree


@tree.command(guild=discord.Object(id=754510720590151751))
async def slash(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(f"{number=} {string=}", ephemeral=True)


pool = concurrent.futures.ThreadPoolExecutor()

bot = Bot(
    "$", "DISCORD_TOKEN_BETA", "Beta", slash_commands=True
)  # , =[754510720590151751])


async def main():
    async with bot:
        try:
            await bot.start(TOKEN)  # loop.run_until_complete(bot.start())
        except Exception:
            traceback.print_exc()


asyncio.run(main())
