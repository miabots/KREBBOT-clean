# commands_mod.py
# commands for interacting with the moderator

import discord
from discord.ext import commands
from datetime import datetime

import sys
import traceback

from typing import Dict, Any, Optional, List, Callable, Awaitable

from cns import *

global inboxtest
inboxtest = cns.NOTTE_INBOX

# TODO: refactor the globals into the class via self.


bwltest = \
    {
        1: {'val': 'custom automod string abc123', 'active': 'True', 'emote': 'False'},
        2: {'val': '<:Z_blobmelt:690246301123739768>', 'active': 'True', 'emote': 'True'}
    }


class Moderation(commands.Cog):
    """
    Utilities and helpful commands for mods/power users!
    Do help Moderation for more info on what commands you can use!
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(hidden=True)
    async def testmod(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            return
        print('Test Command Works from Moderation.')
        pass

    @commands.command(help="Bans the mentioned user from the server. This utility is ONLY usable by the server owner.", brief="Ban")
    async def ban(self, ctx, target: discord.Member):
        responseuser = ctx.message.author
        if responseuser.id == responseuser.guild.owner.id or responseuser.id == 181157857478049792:
            print("Attempting to Destroy Target.")
            response = "That's unfortunate. One moment please."
            await ctx.message.channel.send(response)
            target = target
            #print("Banning " + str(target.name)) + " Now."
            await target.ban(reason="")
            response = "Done."
            await ctx.message.channel.send(response)
        else:
            pass

    helpo = """
    Clears chat messages in the channel from which it is invoked.
    Usage: purge <# of messages to check> <Optional: a specific user> <Optional: a word or phrase to find and delete instead of all messages>
    For example: purge 20 @user badword | purge 20 | purge 20 @user | purge 20 badword
    This command is only usable by the server owner or Moderators.
    """

    @commands.command(help=helpo, brief="Purge Messages From a Channel")
    async def purge(self, ctx, amt: int, user: Optional[discord.Member], filter: Optional[str]):
        if not ctx.guild:
            return
        if user:
            targetuser = user
        else:
            targetuser = None

        cap = ctx.message

        def predicate(msg):
            if targetuser:
                if filter:
                    if targetuser == msg.author and str(filter) in str(msg.content):
                        print("1 - user on filter on PASS")
                        return True
                    else:
                        print("2 - user on filter on FAIL")
                        return False
                else:
                    if targetuser == msg.author:
                        print("3 - user on filter off PASS")
                        return True
                    else:
                        print("4 - user on filter off FAIL")
                        return False
            else:
                if filter:
                    if str(filter) in str(msg.content):
                        print("5  - user off filter on PASS")
                        return True
                    else:
                        print("6 - user off filter on FAIL")
                        return False
                else:
                    print("7  - user off filter off PASS aka catchall")
                    return (msg.author == targetuser) if targetuser else True

        responseuser = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name="Stream Mod")
        if responseuser.id == responseuser.guild.owner.id or role in responseuser.roles or responseuser.id == 181157857478049792:
            clrmsg = await ctx.channel.purge(limit=amt+1, check=predicate)
            print("".join(traceback.format_exc()), file=sys.stderr)
            await ctx.channel.send("Cleared " + str(len(clrmsg)) + " messages from this channel.", delete_after=3)
            try:
                await cap.delete()
            except:
                pass
        else:
            print("Passing purge attempt due to bad perms")

    @commands.command(help="Configure your KREBBOT Mod settings! (Server owner only)")
    async def configmod(self, ctx):

        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        # if str(responseuser) not in cns.POWER_USERS:
        #    print('Returning due to lack of Power User permissions.')
        #    return

        if responseuser.id != responseuser.guild.owner.id:
            return

        response = "Hello! Welcome to KREBBOT Configuration!\nPlease enter the number of the choice you want(e.g. 1m):\n"
        await ctx.channel.send(response)

        response = "1m. Turn automoderation on or off\n2m. Add words or emotes to be filtered\n3m. Get your list of words\n4m. Change the automoderator style\n5m. Change the automoderator message\n6m. Remove words or emotes from the filter"
        await ctx.channel.send(response)

        #cns.awaitingchoicem = True


async def setup(bot):
    await bot.add_cog(Moderation(bot))

  # <@&754762965760213062> <@&849353797506957373>


# 2, 3, 4, 5, 10, 11, 12
