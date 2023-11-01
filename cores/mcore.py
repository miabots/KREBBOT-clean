# mcore.py
# Moderation core for KREBBOT

import modulefinder
import discord
from discord.ext import commands

from database.db import Db

from psycopg2.extras import Json, DictCursor

from cns import *

import rich

import ast

import re

from rich import print as print

import traceback

import traceback as formatter

badwords = {
    1: {"val": "custom automod string abc123", "active": "True", "emote": "False"},
    2: {"val": "<:Z_blobmelt:690246301123739768>", "active": "True", "emote": "True"},
}

# TODO: use above dictionary instead of cns.bad_words to more dynamically handle the Automod content


class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.bwc = 0
        self.pymod = False
        self.bad_words = {}
        self.intents = bot.intents

    async def gbwl(self, ctx):
        Db.dangerset(
            f"select bad_words_list from moderation where server_id = {ctx.guild.id};"
        )
        bwl = Db.dangerexecute()
        bwl = bwl[0]
        bwl = str(bwl)
        bwl = bwl[1:-2]
        if bwl is None:
            return []
        else:
            return bwl
        # print(str(bwl))

    async def countBadWords(self, ctx, wordlist):
        self.bwc = 0
        mm = str(ctx)
        # print(wordlist)
        # print(mm)
        fn = []
        wl = dict()
        wl = ast.literal_eval(wordlist)
        for key in wl:
            fn.append(wl[key]["val"])

        for badword in fn:
            # print(badword)
            if badword in mm:
                self.bwc += 1
        return self.bwc

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 754510720590151751:
            for role in member.guild.roles:
                if role.name == "Pending Manual Verification":
                    roles2 = role
                    break
            try:
                await member.add_roles(roles2, reason=None, atomic=True)
            except discord.HTTPException:
                print("Adding Role Failed")
                pass
            except:
                print("UH OHHDGDFGDFG")
                traceback.print_exc()
                pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self:
            # message is from itself
            return

        if message.guild is None:
            # no guild found
            return

        else:  # guild found
            # data collection and database population check on every message
            c = 0
            guildlist = self.bot.guilds
            # print('Guilds:')
            for guild in guildlist:
                Db.dangerset("select server_id from moderation")
                testid = Db.dangerexecute()

                if str(guild.id) in str(testid):
                    pass
                else:
                    Db.dangerset(
                        f"INSERT INTO moderation(server_id, moderation_on_ind, moderation_style_id) VALUES ({guild.id}, 0, 0);commit;"
                    )
                    noth = Db.dangerexecute()
                c = 0
                Db.dangerset("select discord_id from users")
                testid = Db.dangerexecute()
                for member in guild.members:
                    if str(member.id) in str(testid):
                        # print("User already in table")
                        pass
                    else:
                        Db.dangerset(
                            f"insert into users (discord_id,discord_name,discord_des,guild) values ({member.id},'{member.name}',{member.discriminator},{member.guild.id});commit;"
                        )
                        noth = Db.dangerexecute()
                        c += 1
                # print("Added " + str(c) + " new users from " + str(guild.name))

            if await self.bot.is_prod_guild(message):
                return

            badwordlist = await self.gbwl(message)
            badwordlist = str(badwordlist)
            # print("CNS: " + str(cns.bad_words))
            # print("DB: " + badwordlist)

            gid = message.guild.id
            Db.dangerset(
                f"select moderation_on_ind from moderation where server_id = {gid}"
            )
            modind = Db.dangerexecute()
            modind = str(modind[0])
            modind = modind[1:-2]
            modind = int(modind)

            Db.dangerset(
                f"select moderation_style_id from moderation where server_id = {gid}"
            )
            styleind = Db.dangerexecute()
            styleind = str(styleind[0])
            styleind = styleind[1:-2]
            styleind = int(styleind)

            # print("styleIND: " + str(styleind))
            if modind == 1:
                bwcl = 0
                try:
                    bwcl = await self.countBadWords(
                        message.content, badwordlist
                    )  # also send guild for db
                except:
                    pass

                # TODO: pass guild and make this fully dynamic
                Db.dangerset(
                    f"select mod_response from moderation where server_id = {message.author.guild.id};"
                )
                words = Db.dangerexecute()
                words = str(words[0])
                words = words[2:-3]
                if bwcl > 0:
                    # if message.author.bot:
                    #     pass
                    # else:
                    await message.delete()
                    if styleind == 1:
                        await message.channel.send(words)
                    else:
                        print("silent mode")
                    return
            else:
                pass

            if (
                self.bot.user.mentioned_in(message)
                and message.mention_everyone is False
            ):
                if "prefix" in message.content.lower():
                    await message.channel.send(
                        f"Hello, my command prefix is {self.bot.prefix}.\nFor example, you can see the list of commands by typing {self.bot.prefix}help"
                    )
                else:
                    await message.add_reaction("👀")

            if message.content == "Am I being watched?":
                response = f"Yes. I am always watching. You can DM me if you ever need assistance or type {self.bot.prefix}help."
                await message.channel.send(response)

            # april fools
            # if "i'm " in message.content.lower() or "im " in message.content.lower():
            if True == False:
                # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                x = re.search("(?:im|i'm\s)", message.content.lower())
                print(x)
                if x:
                    y = x.end()
                else:
                    y = 0
                print(y)
                stringo = str(message.content)
                stringy = stringo[y:]
                stringy = stringy.strip()
                z = re.search("^\S*", stringy)
                print(z)
                if z:
                    newnick = z.group()
                    print(newnick)
                    await message.author.edit(nick=newnick)
                else:
                    pass

            if message.author.id == message.author.guild.owner.id:
                if message.content == "1m":
                    response = f'Enable or disable the automoderator.\nType "automod on" or "automod off" to do so.'
                    await message.channel.send(response)

                if message.content == "automod on":
                    Db.dangerset(
                        f"update moderation set moderation_on_ind=1 where server_id = {message.author.guild.id};commit;"
                    )
                    testid = Db.dangerexecute()
                    response = f"Automod is now on."
                    await message.channel.send(response)

                if message.content == "automod off":
                    Db.dangerset(
                        f"update moderation set moderation_on_ind=0 where server_id = {message.author.guild.id};commit;"
                    )
                    testid = Db.dangerexecute()
                    response = f"Automod is now off."
                    await message.channel.send(response)

                if message.content == "2m":
                    response = f'Add words to the automod filter.\nType "addword" then in double quotes the text, e.g.:\naddword "badword"\naddword "hello example"'
                    await message.channel.send(response)

                if "addword" in message.content:
                    modresponse = message.content
                    modresponse = modresponse[9:-1]
                    # print("MR: " + modresponse)
                    Db.dangerset(
                        f"select bad_words_list from moderation where server_id = {message.author.guild.id};"
                    )
                    words = Db.dangerexecute()
                    words = str(words[0])
                    words = words[1:-2]
                    wl = dict()
                    wl = ast.literal_eval(words)
                    index = max(wl)
                    # print("INDEX: " + str(index))
                    index = int(index)
                    index += 1
                    index = str(index)

                    # index = '"' + index + '"'
                    # print(str(wl))
                    into = {"val": modresponse, "active": "True", "emote": "False"}
                    wl[index] = into

                    # print(str(wl))
                    Db.dangerset(
                        f"update moderation set bad_words_list={Json(wl)} where server_id = {message.author.guild.id};commit;"
                    )
                    testid = Db.dangerexecute()
                    response = f"Successfully Added."
                    await message.channel.send(response)

                if message.content == "3m":
                    response = f"Get words from the automod filter.\nYour list of badwords has been sent to your DM.\n"
                    await message.channel.send(response)
                    Db.dangerset(
                        f"select bad_words_list from moderation where server_id = {message.author.guild.id};"
                    )
                    words = Db.dangerexecute()
                    words = str(words[0])
                    words = words[1:-2]
                    wl = dict()
                    wl = ast.literal_eval(words)
                    # for item in wl:
                    # print("WEWEWE\n")
                    # print(wl)
                    fn = ""
                    for key in wl:
                        fn = fn + key + ": " + str(wl[key]) + "\n"
                    response = fn
                    await message.author.send(response)

                if message.content == "6m":
                    response = f'Remove words from the automod filter.\nType "removeword" then the ID of the word you want removed.\nYour list of badwords has been sent to your DM.\n'
                    await message.channel.send(response)
                    Db.dangerset(
                        f"select bad_words_list from moderation where server_id = {message.author.guild.id};"
                    )
                    words = Db.dangerexecute()
                    words = str(words[0])
                    words = words[1:-2]
                    # wl = dict(words.split("},"))
                    wl = dict()
                    wl = ast.literal_eval(words)
                    # for item in wl:
                    # print("WEWEWE\n")
                    # print(wl)
                    fn = ""
                    for key in wl:
                        fn = fn + key + ": " + str(wl[key]) + "\n"
                    response = fn
                    await message.author.send(response)

                if "removeword" in message.content:
                    modresponse = message.content
                    modresponse = modresponse[11:]
                    # print("MR: " + modresponse)
                    Db.dangerset(
                        f"select bad_words_list from moderation where server_id = {message.author.guild.id};"
                    )
                    words = Db.dangerexecute()
                    words = str(words[0])
                    words = words[1:-2]
                    wl = dict()
                    wl = ast.literal_eval(words)
                    index = modresponse
                    # print("INDEX: " + str(index))

                    # index = '"' + index + '"'
                    # print(str(wl))
                    del wl[index]

                    # print(str(wl))
                    Db.dangerset(
                        f"update moderation set bad_words_list={Json(wl)} where server_id = {message.author.guild.id};commit;"
                    )
                    testid = Db.dangerexecute()
                    response = f"Successfully Removed."
                    await message.channel.send(response)

                if message.content == "4m":
                    response = f'Type "style quiet" or "style loud" to enable or disable silent vs. verbose moderation\n(e.g. posting a message when something is deleted vs just deleting)'
                    await message.channel.send(response)

                if message.content == "style loud":
                    Db.dangerset(
                        f"update moderation set moderation_style_id=1 where server_id = {message.author.guild.id};commit;"
                    )
                    testid = Db.dangerexecute()
                    response = f"Style is now loud."
                    await message.channel.send(response)

                if message.content == "style quiet":
                    Db.dangerset(
                        f"update moderation set moderation_style_id=0 where server_id = {message.author.guild.id};commit;"
                    )
                    testid = Db.dangerexecute()
                    response = f"Style is now quiet."
                    await message.channel.send(response)

                if message.content == "5m":
                    response = f'Type "modmessage" and then the moderation message in double quotes to send when the automod is triggered. e.g.:\nmodmessage "Message deleted by filter"'
                    await message.channel.send(response)

                if "modmessage" in message.content:
                    modresponse = message.content
                    modresponse = modresponse[12:-1]
                    # print("MR: " + modresponse)
                    Db.dangerset(
                        f"update moderation set mod_response='{modresponse}' where server_id = {message.author.guild.id};commit;"
                    )
                    testid = Db.dangerexecute()
                    response = f"Mod Message Updated."
                    await message.channel.send(response)


async def setup(bot):
    await bot.add_cog(Automod(bot))
