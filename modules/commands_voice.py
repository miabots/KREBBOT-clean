# commands_voice.py
import discord
from discord import *
from discord.ext import commands
from asyncio import sleep

from cns import *

global voice_clientz
# global djguild


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # initialize the VC
        ctx = self.bot
        print(ctx)
        ctx.guild = ctx.get_guild(754510720590151751)
        channel = discord.utils.get(ctx.guild.voice_channels, name="joinme")
        global voice_clientz
        voice_clientz = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voice_clientz is None:
            if not voice_clientz.is_connected():
                await channel.connect()
        else:
            await channel.connect()
            voice_clientz = discord.utils.get(
                self.bot.voice_clients, guild=ctx.guild)
        await voice_clientz.disconnect()
        print(voice_clientz)
        print('VC initialized.')
        pass

    @commands.command(help="Forces the bot to join voice.\nIt is only usable by Power Users.", brief="Power User Command")
    async def joinvc(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            #print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(help="Forces the bot to leave voice.\nIt is only usable by Power Users.", brief="Power User Command")
    async def leavevc(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            #print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        await voice_clientz.disconnect(force=True)

    @commands.command(help="Basic test command to confirm that the module is loaded and responding.\nIt is only usable by Power Users.", brief="Power User Command")
    async def testvc(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            #print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        print('Test Command Works from voice.')
        pass

    @commands.command(help="The bot joins your VC, plays a sound, and leaves.\nIt is only usable by Power Users.", brief="The bot joins your VC, plays a sound, and leaves.")
    async def plays(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            #print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        path = ".\media\Hlo_HF083.mp3"
        channel = ctx.author.voice.channel
        # print(ctx.author.voice.channel)
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(
            executable="G:\TerrariaWithMods\Terraria\\x64\\ffmpeg.exe", source=path))
        while(vc.is_playing()):
            await sleep(2)
            await vc.disconnect()

    @ commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id in cns.PROD_GUILDS:
            #print('Returning due to Production Guild.')
            return
        if str(member) != 'KREBBOT#8186':
            path = ".\media\Hlo_HF083.mp3"

            global voice_clientz

            if member.voice is None:
                pass
                #global voice_clientz
               # await voice_clientz.disconnect(force=True)
                #print('Executing disconnect due to no member ctx')
            else:
                #print('I AM HERE BEANS')
                channel = member.voice.channel
              #  if not voice_clientz.is_connected():
                vc = await channel.connect()
                await sleep(1)
                vc.play(discord.FFmpegPCMAudio(
                    executable="G:\TerrariaWithMods\Terraria\\x64\\ffmpeg.exe", source=path))
                while(vc.is_playing()):
                    await sleep(2)
                    await vc.disconnect()


def setup(bot):
    bot.add_cog(Voice(bot))
