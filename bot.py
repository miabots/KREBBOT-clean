# bot.py
# bot class
from aiohttp import web
from quart_discord import DiscordOAuth2Session
from quart import Quart, render_template, redirect, url_for
from typing import Dict, Any, Optional, List, Callable, Awaitable
from discord.ext.commands import Context as Contextc
from modules.utils.context import Context
from datetime import datetime
from PIL import Image
from discord import app_commands
from discord.ext import commands
import discord
import json
import aiohttp
import asyncpg
import logging
import traceback as formatter
import traceback
import parsedatetime
import re
import sys
import datetime
import calendar
from cns import *

import asyncio

import concurrent.futures
from _tkinter import *
import random
import os

import ssl

# from discord.player import FFmpegAudio

from dotenv import load_dotenv

path = "./"
load_dotenv()


# webserver handling
# from flask import Flask, request
# app = Flask(__name__)

# from .context import Context


# from slashtest import *
# import slashtest

# logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("discord")
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

path = "./"
load_dotenv()


class Bot(commands.Bot):
    loop: asyncio.AbstractEventLoop
    # gpass: discord.Guild

    def __init__(
        self,
        prefix: str,  # accepts with single quotes
        token: str,  # name of the token as str
        branch: str = "Beta",  # Live or Beta
        *,
        slash_commands: bool = False,
        slash_command_guilds: Optional[List[int]] = [754510720590151751],
        **options,
    ):
        # self.loop: asyncio.AbstractEventLoop
        self.owner_id = 181157857478049792
        # self._token = os.getenv('DISCORD_TOKEN')
        self._token = os.getenv(token)
        self.tindex = 0
        self.prefix = prefix
        self.branch = branch
        self.settings = {}
        self.db: asyncpg.pool.Pool = None
        with open("config.json") as f:
            self.settings = json.load(f)

        owners = [
            181157857478049792,
            855450076011561001,
            858945219448799263,
            937408817212305418,
        ]
        intents = discord.Intents.all()
        allowed_mentions = discord.AllowedMentions.none()
        command_prefix = commands.when_mentioned_or(prefix)
        slash_commands = slash_commands
        # slash_command_guilds = slash_command_guilds

        super().__init__(
            command_prefix=command_prefix,
            owner_ids=set(owners),
            intents=intents,
            allowed_mentions=allowed_mentions,
            slash_commands=slash_commands,
            # slash_command_guilds=slash_command_guilds
        )

    async def on_ready(self):
        print(f"{self.user} is here.")
        global guildlist
        guildlist = self.guilds

        print("Guilds:")
        for guild in guildlist:
            print("Name: " + str(guild.name) + " and ID: " + str(guild.id))
            print("Owner: " + str(guild.owner) + " and ID: " + str(guild.owner_id))
            if guild.id == 754510720590151751:
                print("trying to save guild pass")
                self.gpass = guild
                print("saved guild pass!")
                # print("trying app commands")
                # await self.upload_guild_application_commands(guild.id)
        print("app commands")
        # await self.wait_until_ready()
        # intents = discord.Intents.default()
        # intents.message_content = True
        # client = discord.Client(intents=intents, application_id=855450076011561001)
        # client = commands.Bot(" ", intents=intents, application_id=855450076011561001)
        # tree = app_commands.CommandTree(client)

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="you. Always."
            )
        )

        # print("Slash Commands: ", self.slash_commands)

    async def get_context(self, message, cls=Context):
        return await super().get_context(message, cls=cls)

    async def is_owner(self, user: discord.User):
        if user.id in [
            181157857478049792,
            855450076011561001,
            858945219448799263,
            937408817212305418,
        ]:  # notte, kb, uv, nb
            return True

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CheckFailure):
            return await context.send(exception.args[0])

        else:
            print(f"Ignoring exception in command {context.command}:", file=sys.stderr)
            traceback.print_exception(
                type(exception), exception, exception.__traceback__, file=sys.stderr
            )

    async def on_error(self, event_method, *args, **kwargs):
        traceback.print_exc()
        print("".join(formatter.format_exc()), file=sys.stderr)

        # print("woops")

    async def is_power_user(self, ctx):
        # print(ctx)
        # print(ctx.args)
        # print(ctx.kwargs)
        if ctx:
            if ctx.user:
                if ctx.user.id in cns.POWER_USERS:
                    return True
            else:
                print("Power User Elevation Check Failed\n")
                print("CTX is: ", ctx)
                return False
        else:
            print("Power User Elevation Check Failed\n")
            print("CTX is: ", ctx)
            return False

    async def is_authed_user(self, ctx):
        if ctx:
            if ctx.user.id in cns.AUTHED_USERS:
                return True
        else:
            print("Authed User Elevation Check Failed\n")
            print("CTX is: ", ctx)
            return False

    async def is_prod_guild(self, ctx):
        if ctx:
            if ctx.guild:
                if ctx.guild.id in cns.PROD_GUILDS:
                    return True
        else:
            return False

    async def is_automod_on(self, ctx):
        if ctx:
            if ctx.guild:
                if ctx.guild.id in cns.AM_GUILDS:
                    # print("am on")
                    return True
        else:
            # print("am off")
            return False

    async def is_guild_elevated(self, ctx, req):
        pass
        # eventually send various guild role elevations checks for parsing

    async def is_there(self, ctx):
        if ctx:
            return True
        else:
            return False

    async def has_emote(self, ctx):
        if ctx:
            # print(ctx)
            # print(re.search(str(ctx), "(<(:|a:)).+?:([0-9]{18}>)"))
            if re.search("(<(:|a:)).+?:([0-9]{18}>)", str(ctx)):
                return True
            else:
                return False
        else:
            return False

    async def check_emote(self, ctx):
        if ctx:
            return re.match("(<(:|a:)).+?:([0-9]{18}>)", str(ctx))

    async def on_message(self, message: discord.Message):
        # if message.author.bot:
        #    return

        ctx = await self.get_context(message, cls=Context)
        # if not ctx.valid:
        # customcmd = self.get_cog("Commands")
        # await customcmd.dispatch_hook(ctx)  # noqa
        # print("CTX IS INVALID INTO BOT")
        # print("ATTEMPTING DEFAULT CLASS")
        # ctx2 = await self.get_context(message, cls=Contextc)
        # if not ctx2.valid:
        #    print("DEFAULT CTX ALSO INVALID")
        # else:
        #    ctx = ctx2

        await self.invoke(ctx)

    # async def start(self) -> None:  # noqa

    # THIS IS THE MIDDLE TIER CODE

    async def handle(self, request):
        conhtml = open("index.html", "r")
        return web.Response(text=conhtml.read(), content_type="text/html")

    async def handleauth(self, data):
        # conhtml = open("index.html", "r")
        # return web.Response(text=conhtml.read(), content_type='text/html')
        print("RECEIVED CODE HERE IS THE DATA:")
        print(data)

    # auth URL is http://73.16.11.8:4444/auth

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()

        # SSL
        print("TRYING SSL")
        # serverHost = "localhost"
        # serverPort = "443"
        # serverAddress = (serverHost, serverPort)
        # pem = ssl.get_server_certificate(serverAddress)
        # with open('cert.pem', 'w') as f:
        #    f.write(pem)

        # async with aiohttp.ClientSession(ssl='./cert.pem') as self.session:
        #    async with self.session.get('https://73.16.11.8') as resp:
        #        print("AIOHTTP CLIENT SESSION:")
        #        print(resp.status)
        #        print(await resp.text())

        # setup db
        self.db: asyncpg.pool.Pool = await asyncpg.create_pool(
            self.settings["db_uri"], min_size=1
        )
        with open("schema.sql") as f:
            schema = f.read()

        await self.db.execute(schema)

        # slashz = slashtest.Slasho()

        # WEB SERVER IMPLEMENTATION
        self.router = web.RouteTableDef()

        # self.server = web.Application()
        # self.server.add_routes([web.get("/", self.handle), web.get("/auth", self.handleauth)])

        # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # ssl_context.load_cert_chain("cert.pem", "key.pem")

        # TURN THE WEBSERVER OFF IN NONPROD
        # self.loop.create_task(web._run_app(self.server, host="0.0.0.0", port=4444))

        await self.load_extension("jishaku")
        print("Loaded jsk")
        # custom jsk
        # self.load_extension("abstract")

        self.remove_command("help")

        if self.branch == "Live":
            for cog in cns.cogs_prod:
                try:
                    await self.load_extension(cog)
                    print("Loaded a Cog: " + str(cog))
                except Exception:
                    print("\n COG LOAD FAILED:\n")
                    traceback.print_exc()

        elif self.branch == "Beta":
            for cog in cns.cogs_beta:
                try:
                    await self.load_extension(cog)
                    print("Loaded a Cog: " + str(cog))
                except Exception:
                    print("\n COG LOAD FAILED:\n")
                    traceback.print_exc()

        # await self.upload_global_application_commands()

        # print("Initializing VC.")
        # vccog = self.get_cog("Voice")
        # await vccog.initVC()

        print("Initializing DB.")
        # print("asdasdasd: \n" + str(self))
        dbcog = self.get_cog("Db")
        dbcog.initdb()

        print("Setting Presence.")

        # await self.login(self._token)
        # await self.setup()
        # await self.connect(reconnect=True)
