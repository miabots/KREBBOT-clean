# mcore.py
# Moderation core for KREBBOT

import discord
from discord.ext import commands

from psycopg2.extras import Json, DictCursor

from cns import *

import ast

from rich import print as print

badwords = \
    {
        1: {'val': 'custom automod string abc123', 'active': 'True', 'emote': 'False'},
        2: {'val': '<:Z_blobmelt:690246301123739768>', 'active': 'True', 'emote': 'True'}
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
        bwl = await self.bot.do_query(f"select bad_words_list from moderation where server_id = {ctx.guild.id};")
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
            fn.append(wl[key]['val'])

        for badword in fn:
            # print(badword)
            if badword in mm:
                self.bwc += 1
        return self.bwc

    @ commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 754510720590151751 or member.guild.id == 843927271483113472:
            for role in member.guild.roles:
                if role.name == 'Common':
                    roles2 = role
                    break
            try:
                await member.add_roles(roles2, reason=None, atomic=True)
            except discord.HTTPException:
                print("Adding Role Failed")
                pass
            except:
                print("UH OHHDGDFGDFG")
                # traceback.print_exc()
                pass
        
        if member.guild.id == 1175277956885651526:
            #parks 2
            channel = self.bot.get_channel(1175277957875499009)
            embed = discord.Embed(title="KREBBOT", description=f"Hi {member.mention}, welcome to Parks&Recvivor! Watch out for raccoons.", color=discord.Color.purple())
            embed.set_image(url="https://cdn-longterm.mee6.xyz/plugins/welcome/images/1018405423440728084/73c3327a9d937ba8cf75e88bbc012c2f87b1c086f5f748949fa1fa13e3c0a7e7.jpeg")
            await channel.send(embed=embed) 

        if member.id == 180844306825740288 or member.id == 229669847057956876:
            try:
                await member.ban(reason=None)
            except discord.HTTPException:
                print("autoban Failed")
                pass
            except:
                print("UH OHHDGDFGDFG")
                # traceback.print_exc()
                pass

            # dang 180844306825740288
            # egg 229669847057956876

    @ commands.Cog.listener()
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
                try:
                    testid = await self.bot.do_query("select server_id from moderation")
                except:
                    testid = 'gdfsgsfgsfgsdfg'

                if str(guild.id) in str(testid):
                    pass
                else:
                    try:
                        await self.bot.do_query(f"INSERT INTO moderation(server_id, moderation_on_ind, moderation_style_id) VALUES ({guild.id}, 0, 0);")
                    except:
                        pass
                c = 0
                try:
                    testid = await self.bot.do_query("select discord_id from users")
                except:
                    testid = 'fgsdfgsfdgsf'
                for member in guild.members:
                    if str(member.id) in str(testid):
                        # print("User already in table")
                        pass
                    else:
                        try:
                            m2 = member.name
                            m2 = m2.replace("'", "")
                            await self.bot.do_query(
                                f"insert into users (discord_id,discord_name,discord_des,guild) values ({member.id},'{m2}',{member.discriminator},{member.guild.id});")
                        except:
                            pass
                        c += 1
                # print("Added " + str(c) + " new users from " + str(guild.name))

            if await self.bot.is_prod_guild(message):
                return

            badwordlist = await self.gbwl(message)
            badwordlist = str(badwordlist)
            # print("CNS: " + str(cns.bad_words))
            # print("DB: " + badwordlist)

            gid = message.guild.id
            modind = await self.bot.do_query(f"select moderation_on_ind from moderation where server_id = {gid}")
            modind = str(modind[0])
            modind = modind[-2]
            modind = int(modind)

            styleind = await self.bot.do_query(f"select moderation_style_id from moderation where server_id = {gid}")
            styleind = str(styleind[0])
            styleind = styleind[-2]
            styleind = int(styleind)

            # print("styleIND: " + str(styleind))
            if modind == 1:
                bwcl = 0
                try:
                    bwcl = await self.countBadWords(message.content, badwordlist)  # also send guild for db
                except:
                    print("AHHHHHHHHH")

                # TODO: pass guild and make this fully dynamic
                words = await self.bot.do_query(f"select mod_response from moderation where server_id = {message.author.guild.id};")
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

            if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
                if 'prefix' in message.content.lower():
                    await message.channel.send(f"Hello, my command prefix is {self.bot.prefix}.\nFor example, you can see the list of commands by typing {self.bot.prefix}help")
                else:
                    await message.add_reaction('👀')

            if message.content == 'Am I being watched?':
                response = f'Yes. I am always watching. You can DM me if you ever need assistance or type {self.bot.prefix}help.'
                await message.channel.send(response)

            if message.author.id == message.guild.owner.id:
                if message.content == '1m':
                    response = f'Enable or disable the automoderator.\nType "automod on" or "automod off" to do so.'
                    await message.channel.send(response)

                if message.content == 'automod on':
                    await self.bot.do_query(f"update moderation set moderation_on_ind=1 where server_id = {message.author.guild.id};")
                    response = f'Automod is now on.'
                    await message.channel.send(response)

                if message.content == 'automod off':
                    await self.bot.do_query(f"update moderation set moderation_on_ind=0 where server_id = {message.author.guild.id};")
                    response = f'Automod is now off.'
                    await message.channel.send(response)

                if message.content == '2m':
                    response = f'Add words to the automod filter.\nType "addword" then in double quotes the text, e.g.:\naddword "badword"\naddword "hello example"'
                    await message.channel.send(response)

                if 'addword' in message.content:
                    modresponse = message.content
                    modresponse = modresponse[9:-1]
                    # print("MR: " + modresponse)
                    words = await self.bot.do_query(f"select bad_words_list from moderation where server_id = {message.author.guild.id};")
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
                    into = {'val': modresponse, 'active': 'True', 'emote': 'False'}
                    wl[index] = into

                    # print(str(wl))
                    await self.bot.do_query(f"update moderation set bad_words_list={Json(wl)} where server_id = {message.author.guild.id};")
                    response = f'Successfully Added.'
                    await message.channel.send(response)

                if message.content == '3m':
                    response = f'Get words from the automod filter.\nYour list of badwords has been sent to your DM.\n'
                    await message.channel.send(response)
                    words = await self.bot.do_query(f"select bad_words_list from moderation where server_id = {message.author.guild.id};")
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

                if message.content == '6m':
                    response = f'Remove words from the automod filter.\nType "removeword" then the ID of the word you want removed.\nYour list of badwords has been sent to your DM.\n'
                    await message.channel.send(response)
                    words = await self.bot.do_query(f"select bad_words_list from moderation where server_id = {message.author.guild.id};")
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

                if 'removeword' in message.content:
                    modresponse = message.content
                    modresponse = modresponse[11:]
                    # print("MR: " + modresponse)
                    words = await self.bot.do_query(f"select bad_words_list from moderation where server_id = {message.author.guild.id};")
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
                    await self.bot.do_query(f"update moderation set bad_words_list={Json(wl)} where server_id = {message.author.guild.id};")
                    response = f'Successfully Removed.'
                    await message.channel.send(response)

                if message.content == '4m':
                    response = f'Type "style quiet" or "style loud" to enable or disable silent vs. verbose moderation\n(e.g. posting a message when something is deleted vs just deleting)'
                    await message.channel.send(response)

                if message.content == 'style loud':
                    await self.bot.do_query(f"update moderation set moderation_style_id=1 where server_id = {message.author.guild.id};")
                    response = f'Style is now loud.'
                    await message.channel.send(response)

                if message.content == 'style quiet':
                    await self.bot.do_query(f"update moderation set moderation_style_id=0 where server_id = {message.author.guild.id};")
                    response = f'Style is now quiet.'
                    await message.channel.send(response)

                if message.content == '5m':
                    response = f'Type "modmessage" and then the moderation message in double quotes to send when the automod is triggered. e.g.:\nmodmessage "Message deleted by filter"'
                    await message.channel.send(response)

                if 'modmessage' in message.content:
                    modresponse = message.content
                    modresponse = modresponse[12:-1]
                    # print("MR: " + modresponse)
                    await self.bot.do_query(f"update moderation set mod_response='{modresponse}' where server_id = {message.author.guild.id};")
                    response = f'Mod Message Updated.'
                    await message.channel.send(response)


async def setup(bot):
    await bot.add_cog(Automod(bot))
