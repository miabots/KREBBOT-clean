# rcore.py
# core bot loop for Dynamic and Static behavior via reaction handling

# from http import client
import random
from datetime import datetime

import psycopg2

import discord
from discord.ext import commands

# from discord.ext.commands import Bot

import asyncio
import datetime

import re

from turtley import *
# from modules.commands.commands_util import readCSV
from cns import *

#from blastoff import bot as botto, intents, intentz

from database.db import Db

from typing import Optional, Union

# insertdb, selectdb, parseinsertsql, testsql, insertdb2

import pandas as pd

# from ..utils.context import Context

import csv

import re

import emoji

from emoji import UNICODE_EMOJI


import traceback

import traceback as formatter
# global rolemessage

# from cns import rolemessage, rolemessageactive


#topclient = discord.Client()
# botclient = (command_prefix=commands.when_mentioned_or('|'), intents=intents)

global rolecommandchannel
global mastermessage
global emojilist
# global mastermessagemode

# IMPLEMENT REMINDERS YOU DOLT


class Reactions(commands.Cog):
    """
    Reaction Roles for Pronouns, no config required!
    Go to your roles channel and run createpronounroles to enable!
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        # print("I am setting intents to:")
        # print(intentz)
        self.intents = bot.intents

    @commands.command(hidden=True)
    async def testreact(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            return
        print('Test Command Works from Reaction.')
        pass

    async def ereactor(self, emojis, emessage):
        for emoji in emojis:
            print("EMOJI")
            print(emoji)
            await emessage.add_reaction(emoji)

    @commands.command(help="Will create a Pronoun Role Selection Message in the current channel")
    async def createpronounroles(self, ctx):  # : list(str)
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if ctx.message.author.guild.owner.id != responseuser.id:
            msg = "This command is only usable by the guild owner."
            ctx.message.author.send(msg)
            return
        # response1 = "Okay " + responseuser.display_name + ", send me the data, and I will take care of the rest! <:notteLove:852251712243630131>"
        global rolecommandchannel
        global emojilist
        global guildref
        guildref = ctx.message.author.guild
        rolecommandchannel = ctx.channel
        # await ctx.channel.send(response1)

        # cns.rolemessage = ""
        cns.rolemessageactive = True

        # loop = asyncio.get_running_loop()
        async with ctx.typing():

            emojilist = ""

            rolestext = """
❤️ He/Him
🧡 She/Her
💛 They/Them
💚 Any/All Pronouns
💙 Pronoun Questioning
🤎 He/They
💜 She/They
"""

            # print("POST PARSE:")
            # print("EMOJI LIST:")
            # print(emojilist)

            print("manually setting emojilist")
            emojilist = ['❤️', '🧡', '💛', '💚', '💙', '🤎', '💜']
            rolelist = []
            # emojilist = ":heart:, :orange_heart:, :yellow_heart:, :green_heart:, :blue_heart:, :brown_heart:, :purple_heart:"
            global mastermessage
            mastermessage = await rolecommandchannel.send(rolestext)

            for emoji in emojilist:
                try:
                    print("EMOJI")
                    print(str(emoji))
                    await mastermessage.add_reaction(emoji)
                except:
                    print("ERROR ON REACT")
                    pass

            cns.rolemessageactive = False

            Db.dangerset(f"update moderation set rron=1,rrmmid={mastermessage.id},rrchid={rolecommandchannel.id} where server_id = {ctx.message.author.guild.id};commit;")
            toss = Db.dangerexecute()

            pass

    # |rrt ":eyes:, :grimacing:, :brain:"

    # ❤️ 🧡 💛 💚 💙 💜 🤎

    # temp = ":heart:, :orange_heart:, :yellow_heart:, :green_heart:, :blue_heart:, :brown_heart:, :purple_heart:"

    def is_emoji(self, s):
        print(s)
        if s in UNICODE_EMOJI:
            # print("AHHHHHHHHHHHHHHHHHHHHH GOT ONE")
            return s
        else:
            return 0

    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        # print("HELLO")
        # if (ctx.guild_id == 754510720590151751):

        Db.dangerset(f"select rron from moderation WHERE server_id = {ctx.guild_id}")
        rron = Db.dangerexecute()

        rron = str(rron[0])
        rron = rron[1:-2]
        # print("RRRRRRRRRRRRR\n")
        print(rron)
        rron = int(rron)

        if rron != 1:
            return

        guild = self.bot.get_guild(ctx.guild_id)
        #guild = self.bot.get_guild(754510720590151751)

        channel = guild.get_channel(ctx.channel_id)
        # channel = guild.get_channel(925930479037853736)  # nottes home
        member = guild.get_member(ctx.user_id)
        # also
        #member = ctx.member

        #print("mem details")
        # print(member.name)

        if not bool(member):
            return

        if member.bot:
            #print("BOT RETURN")
            return

        # global purgemessageactive
        # global purgemessage
        global emojilist

        emojilist = ['❤️', '🧡', '💛', '💚', '💙', '🤎', '💜']
        rolelist = ["He/Him", "She/Her", "They/Them", "Any/All Pronouns", "Pronoun Questioning", "He/They", "She/They"]
        if ctx.emoji.name in emojilist:

            Db.dangerset(f"select rrmmid from moderation WHERE server_id = {ctx.guild_id}")
            mmid = Db.dangerexecute()

            mmid = str(mmid[0])
            mmid = mmid[1:-2]
            mmid = int(mmid)

            if ctx.message_id == mmid:
                print("HEARTS HAVE BEEN DROPPED")
                ei = emojilist.index(ctx.emoji.name)
                print("TRYING TO SEND")
                global mastermessage
                print("id", ctx.message_id)
                roles = guild.roles
                roles2 = ''
                ref = rolelist.pop(ei)
                ref = str(ref)
                print("REF")
                print(ref)
                for role in guild.roles:
                    if role.name == ref:
                        roles2 = role
                        break

                # HEY REMEMBER THAT create_roles RETURNS THE ROLE IT CREATES, YOU DONT NEED TO
                # PARSE IT LIKE BELOW

                if roles2 == '':
                    print("NO ROLE DEFINED")
                    try:
                        perms = discord.Permissions.none()
                        await guild.create_role(name=ref)
                        for role in guild.roles:
                            if role.name == ref:
                                roles2 = role
                                break
                    except discord.HTTPException:
                        print("Creating Role Failed")
                        pass
                    except:
                        print("UH OHHDGDFGDFG")
                        traceback.print_exc()
                        pass

                try:
                    await member.add_roles(roles2, reason=None, atomic=True)
                except discord.HTTPException:
                    print("Adding Role Failed")
                    pass
                except:
                    print("UH OHHDGDFGDFG")
                    traceback.print_exc()
                    pass
            else:
                pass

    @ commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):

        Db.dangerset(f"select rron from moderation WHERE server_id = {ctx.guild_id}")
        rron = Db.dangerexecute()

        rron = str(rron[0])
        rron = rron[1:-2]
        print("RRRRRRRRRRRRR\n")
        print(rron)
        rron = int(rron)

        if rron != 1:
            return

        guild = self.bot.get_guild(ctx.guild_id)

        member = guild.get_member(ctx.user_id)

        if not bool(member):
            print("BOT RETURN")
            return
        else:
            if member.bot:
                return

        # global purgemessageactive
        # global purgemessage
        global emojilist

        emojilist = ['❤️', '🧡', '💛', '💚', '💙', '🤎', '💜']
        rolelist = ["He/Him", "She/Her", "They/Them", "Any/All Pronouns", "Pronoun Questioning", "He/They", "She/They"]
        if ctx.emoji.name in emojilist:

            Db.dangerset(f"select rrmmid from moderation WHERE server_id = {ctx.guild_id}")
            mmid = Db.dangerexecute()

            mmid = str(mmid[0])
            mmid = mmid[1:-2]
            mmid = int(mmid)

            print("HEARTS HAVE BEEN DROPPED")
            ei = emojilist.index(ctx.emoji.name)
            print("index")
            print(ei)

            if ctx.message_id == mmid:
                roles = guild.roles
                ref = rolelist.pop(ei)
                ref = str(ref)
                print("REF")
                print(ref)
                for role in guild.roles:
                    if role.name == ref:
                        roles2 = role

                if not roles2:
                    print("NO ROLE DEFINED")
                    return
                try:
                    await member.remove_roles(roles2, reason=None, atomic=True)
                except discord.HTTPException:
                    print("Removing Role Failed")
                    pass
                except:
                    print("UH OHHDGDFGDFG")
                    pass
            else:
                pass


async def setup(bot):
    await bot.add_cog(Reactions(bot))
