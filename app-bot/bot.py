# bot.py
# bot class
from aiohttp import web
from typing import Dict, Any, Optional, List, Callable, Awaitable
#from discord.ext.commands import Context as Context
from datetime import datetime
from discord.ext import commands
from discord import app_commands
import discord
import json
import asyncpg
import logging
import traceback
import re
import sys
import signal
import time
import socket
import sys
import datetime
from cns import *
import asyncio
import os
from dotenv import load_dotenv

path = "./"
load_dotenv()

# logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("discord")
logger.setLevel(logging.ERROR)
if not os.path.isfile("./logs/discord.log"):
    with open("./logs/discord.log", "w") as f:
        handler = logging.FileHandler(filename="./logs/discord.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        logger.addHandler(handler)
else:
        handler = logging.FileHandler(filename="./logs/discord.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        logger.addHandler(handler)

class Bot(commands.Bot):
    loop: asyncio.AbstractEventLoop

    def __init__(
        self,
        prefix: str,  # accepts with single quotes
        token: str,  # name of the token as str
        branch: str,  # Live or Beta
        tree: app_commands.tree.CommandTree = None,
        *,
        slash_commands: bool = True,
        **options,
    ):
        self.owner_id = 181157857478049792
        self._token = os.getenv(token)
        self.tindex = 0
        self.prefix = prefix
        self.branch = branch
        self.settings = {}
        self.webserver = True
        self.db: asyncpg.pool.Pool = None
        with open("./configs/config.json") as f:
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
        #self.tree = tree
        # slash_command_guilds = slash_command_guilds

        super().__init__(
            command_prefix=command_prefix,
            owner_ids=set(owners),
            intents=intents,
            allowed_mentions=allowed_mentions,
            slash_commands=slash_commands,
            tree=tree,
            # slash_command_guilds=slash_command_guilds
        )

    async def on_ready(self):
        print(f"{self.user} is here.")

        
        global guildlist
        guildlist = self.guilds

        print("Guilds:")
        for guildz in guildlist:
            print("Name: " + str(guildz.name) + " and ID: " + str(guildz.id))
            print("Owner: " + str(guildz.owner) + " and ID: " + str(guildz.owner_id))
            if guildz.id == 754510720590151751:
                print("trying to save guild pass")
                self.gpass = guildz
                print("saved guild pass!")
                # print("trying app commands")
                # await self.upload_guild_application_commands(guild.id)
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="you. Always."
            )
        )

        # print("Slash Commands: ", self.slash_commands)

    #async def get_context(self, message, cls=Context):
    #    return await super().get_context(message, cls=cls)

    async def is_owner(self, user: discord.User):
        if user.id in [
            181157857478049792,
            855450076011561001,
            858945219448799263,
            937408817212305418,
        ]:  # notte, kb, uv, nb
            return True

    # this differentiates between breaking and non-breaking errors
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
        print("".join(traceback.format_exc()), file=sys.stderr)

    async def is_power_user(self, ctx):
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
        if message.author.bot:
            return
        await self.process_commands(message)


    # query handling for all db calls
    async def do_query(self, sql: str, *args) -> list[asyncpg.Record]:
        try:
            response = await self.pool.fetch(sql, *args, timeout=60)
            return response
        except asyncio.TimeoutError:
            return []

    async def getbranch(self):
        return self.branch

    async def get_variable_value(self, variable_name):
        if variable_name in globals():
            return globals()[variable_name]
        else:
            return None
        

    async def setup_hook(self):
        # setup db
        #with open("schema.sql") as f:
        #    schema = f.read()

        #await self.db.execute(schema)

        await self.load_extension("jishaku")
        print("Loaded jsk")

        self.remove_command("help")
        print("Removed help")

        print("Initializing DB.")
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        
        if self.branch == "live":
            print("LIVE BRANCH")
            dsn = f"postgresql://postgres:{DB_PASSWORD}@db:5432/KREBBOTDB"
            self.pool = await asyncpg.create_pool(
                dsn, max_inactive_connection_lifetime=3, max_size=3, min_size=0)
            print("Database Init Done.")

            for cog in cns.cogs_prod:
                try:
                    await self.load_extension(cog)
                    print("Loaded a Cog: " + str(cog))
                except Exception:
                    print("\n COG LOAD FAILED:\n")
                    traceback.print_exc()

        elif self.branch == "beta":
            print("BETA BRANCH")
            dsn = f"postgresql://postgres:{DB_PASSWORD}@db:5431/KREBBOTDB"
            self.pool = await asyncpg.create_pool(
                dsn, max_inactive_connection_lifetime=3, max_size=3, min_size=0)
            print("Database Init Done.")

            for cog in cns.cogs_beta:
                try:
                    await self.load_extension(cog)
                    print("Loaded a Cog: " + str(cog))
                except Exception:
                    print("\n COG LOAD FAILED:\n")
                    traceback.print_exc()

        tree = self.tree
        print("syncing commands")
        guild=discord.Object(id=754510720590151751)
        guild2=discord.Object(id=1175277956885651526)
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
        tree.copy_global_to(guild=guild2)
        await tree.sync(guild=guild2)
        print("app commands done")
        print("Setting Presence.")