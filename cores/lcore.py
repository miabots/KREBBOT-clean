# lcore.py
# core module for all logging activities

import random
from datetime import datetime

import psycopg2

import discord
from discord.ext import commands

from cns import *

import rich

from rich import print as print

from modules.utils.context import Context

from typing import Union, List, Dict, Any, Optional, TypedDict

import re


class Loggerz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.intents = bot.intents

    @commands.command(help="")
    async def ltest7(self, ctx):
        b = self.bot
        guild = b.get_guild(754510720590151751)
        print("PRINTING AUDIT LOG:")
        async for entry in guild.audit_logs(limit=100):
            print(str(entry) + "\n")
        print("PRINT COMPLETE")

    # TODO: add handling for big payloads

    @ commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        # print(str(payload))
        if payload.guild_id == 754510720590151751:
            #guild = message.guild.id
            embed = discord.Embed(title="{} deleted a message".format(payload.cached_message.author.name), description="")
            try:
                embed.add_field(name="Channel:", value=payload.cached_message.channel.name, inline=False)
                embed.add_field(name="This is the message that was deleted", value=payload.cached_message.content, inline=True)
            except:
                print("couldn't write message deletion to log")
                embed.add_field(name="This is the message that was deleted", value="CONTENT COULD NOT BE LOADED", inline=True)
            channel = self.bot.get_channel(942864411335487528)
            await channel.send(embed=embed)

    @ commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.guild.id == 754510720590151751:
            if message_before.content == message_after.content:
                return
            try:
                embed = discord.Embed(title="{} edited a message".format(message_before.author.name), description="")
                embed.add_field(name="Channel:", value=message_before.channel.name, inline=False)
                embed.add_field(name="This is the message before any edit", value=message_before.content, inline=True)
                embed.add_field(name="This is the message after the edit", value=message_after.content, inline=True)
                embed.set_footer(text=f'Timestamp: {message_after.created_at}')
                channel = self.bot.get_channel(942864411335487528)
                await channel.send(embed=embed)
            except:
                print("couldn't write message edit to log")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title='Server Event Log',
            color=discord.Color.green()
        )

        embed.add_field(name='Event', value='Member joined', inline=False)
        embed.add_field(name='Member', value=f'{member} ({member.id})', inline=False)
        embed.set_footer(text=f'Timestamp: {member.joined_at}')

        # Send the log to the desired channel
        channel = self.bot.get_channel(942864411335487528)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title='Server Event Log',
            color=discord.Color.red()
        )

        embed.add_field(name='Event', value='Member left', inline=False)
        embed.add_field(name='Member', value=f'{member} ({member.id})', inline=False)
        embed.set_footer(text=f'Timestamp: {member.joined_at}')

        # Send the log to the desired channel
        channel = self.bot.get_channel(942864411335487528)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if set(before.roles) == set(after.roles):
            return
        embed = discord.Embed(
            title='Server Event Log',
            color=discord.Color.blue()
        )

        embed.add_field(name='Event', value='Member role changed', inline=False)
        embed.add_field(name='Member', value=f'{after} ({after.id})', inline=False)
        embed.add_field(name='Old roles', value=', '.join([r.mention for r in before.roles]), inline=False)
        embed.add_field(name='New roles', value=', '.join([r.mention for r in after.roles]), inline=False)
        embed.set_footer(text=f'Timestamp: {before.joined_at}')

        channel = self.bot.get_channel(942864411335487528)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Loggerz(bot))
