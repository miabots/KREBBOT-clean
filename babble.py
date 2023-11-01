# babble.py
# NATO Phentics System

# from http import client
import random
from datetime import datetime

import psycopg2

import discord
from discord.ext import commands

# from discord.ext.commands import Bot

import asyncio
# import datetime

import re

import asyncio

import os
import sys
import unittest
import hashlib
import io
import json
import socket

from shlex import quote as shellquote

from pydub import AudioSegment

import time

from modules.utils.context import Context

# from test_helper import try_rm

# from test import (
# get_params,
# get_testcases,
# try_rm,
# md5,
# report_warning
# )

import youtube_dl.YoutubeDL
from youtube_dl.utils import (
    compat_http_client,
    compat_str,
    compat_urllib_error,
    compat_HTTPError,
    DownloadError,
    ExtractorError,
    UnavailableVideoError,
)
from youtube_dl.extractor import get_info_extractor


from turtley import *
# from modules.commands.commands_util import readCSV
from cns import *

#from blastoff import bot, intents, intentz

from database.db import Db

from typing import Optional, Union

# insertdb, selectdb, parseinsertsql, testsql, insertdb2

import pandas as pd

# from ..utils.context import Context

import csv

import re

import emoji

from emoji import UNICODE_EMOJI

import nottelib
from nottelib import sanitize

import uuid

from gtts import gTTS

from IPython.display import Image, display, Audio

import traceback

# global rolemessage

global vc
vc = None

global vc2

# from cns import rolemessage, rolemessageactive
global voice_clientz
voice_clientz = None


class Babble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        c = self.bot.get_channel(937038164357447690)
        self.c = c
        # print("I am setting intents to:")
        # print(intentz)
        # self.intents = intentz
        # self.timemodeon = timemodeon

    @commands.command()
    async def testb(self, ctx):
        await sanitize(self=self, ctx=ctx, bot=self.bot)
        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            return
        print('Test Command Works from Babble.')
        pass

    # @commands.command()
    async def spk(self, ctx, args):
        # await sanitize(self=self, ctx=ctx, bot=self.bot)

        if ctx.author.guild is None:
            return
        else:
            if ctx.author.guild.id in cns.PROD_GUILDS:
                # print('Returning due to Production Guild.')
                return
        responseuser = ctx.author
        if str(responseuser) not in cns.POWER_USERS and str(responseuser) not in cns.AUTHED_USERS:
            print('Returning due to lack of Power User permissions.')
            return
        # print("Calling convert to speech")
        # testfile = await self.convert_to_speech(message=input)

        mytext = str(args)

        #c = self.bot.get_channel(937038164357447690)

        # for x in args:
        #    mytext = mytext+x

        # mytext = '"' + input + '"'

        myobj = gTTS(text=mytext, lang="en-us", slow=False)
        # print(myobj)
        # print(mytext)

        newtext = ""
        for char in mytext:
            if char.isalnum():
                newtext += char

        audio_title = "d" + "_" + str(newtext) + ".mp3"

        image_dir = "./Sound_Files"

        sound_file = os.path.join(image_dir, audio_title)

        myobj.save(sound_file)

        path = sound_file
        channel = ctx.author.voice.channel

        # print(ctx.author.voice.channel)
        global voice_clientz

        ctx = self.bot
        # print(ctx)
        ctx.guild = ctx.get_guild(754510720590151751)
        channel = discord.utils.get(ctx.guild.voice_channels, name="babble-bot")
        # if voice_clientz is None:
        voice_clientz = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice_clientz is None:
            if not voice_clientz.is_connected():
                voice_clientz = await channel.connect()
        else:
            voice_clientz = await channel.connect()
        #    voice_clientz = discord.utils.get(
        #        self.bot.voice_clients, guild=ctx.guild)
        # await voice_clientz.disconnect()
        # print(voice_clientz)
        #print('VC initialized.')
        # pass

        vc = voice_clientz
        # try:
        #    vc = await self.c.connect()
        # except Exception:
        # await vc.disconnect()
        #    vc = await discord.VoiceClient.move_to(self, self.c)
        vc.play(discord.FFmpegPCMAudio(
            executable="G:\TerrariaWithMods\Terraria\\x64\\ffmpeg.exe", source=path))
        # while(vc.is_playing()):
        #    await asyncio.sleep(1)
        #    await vc.disconnect()

        #print("TEST OF SPEAK DONE")

    @ commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 855450076011561001:
            return

        # notte ID 181157857478049792
        if message.guild is None:
            return
        else:
            if message.guild.id in cns.PROD_GUILDS:
                # print('Returning due to Production Guild.')
                return

        if message.author == self:
            return

        if message.author.id == 855450076011561001:
            return

        if message.channel.id == 937042205158305813 and message.content[0] != "|":
            # ctx = await Context.get_context(message, cls=Context)  # await self.get_context(message)
            await self.spk(message, message)

    async def get_context(self, message, cls=Context):
        return await Context.get_context(message, cls=Context)

    def try_rm(self, filename):
        """ Remove a file if it exists """
        try:
            os.remove(filename)
        except OSError as ose:
            print("OOPS")
            # if ose.errno != errno.ENOENT:
            #   raise


"""
    async def convert_to_speech(self, message):
        mid = str(uuid.uuid4()).replace("-", "")

        print("----------------------------------------")
        print("SPEECH CONVERSION\n")
        print("MID: "+mid)
        print("MESSAGE: "+message)
        print("Converting to speech...")

        wav_file = ".\media\\"+mid+".wav"
        out_file = ".\media\\"+mid+".mp3"       # DOES NOT EXIST YET
        mp3_file = ".\media\\tmp\\"+out_file  # DOES NOT EXIST YET

        self.try_rm(wav_file)  # Deletes if exists
        self.try_rm(mp3_file)

        # command = "DISPLAY=:0.0 wine say.exe -w "+wav_file+" "+shellquote(message)

        # print(command)
        # os.system(command)

        # TODO: you have to use azure to spin up an entire virtual linux environment, install wine, then use the above command thing.
        #

        print("Converting to mp3...")
        sound = AudioSegment.from_file(wav_file, format="wav")
        loud = sound+3
        loud.export(mp3_file, bitrate='64k', format="mp3")

        print("DONE!")
        print("----------------------------------------")

        return out_file
"""


def setup(bot):
    bot.add_cog(Babble(bot))
