# commands_economy.py
# lets users have custom currency

import discord
from discord.ext import commands
from datetime import datetime
import os
import sys
import random

from typing import Optional, Union


# insertdb, selectdb, parseinsertsql, testsql, insertdb2

import pandas as pd

import csv

import re

from cns import *


class Economy(commands.Cog):
    """
    Currency and Economy features
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db

    @commands.command(help="Basic test command to confirm that the module is loaded and responding.\nIt is only usable by Power Users.", brief="Power User Command", hidden=True)
    async def testecon(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return

        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        print('Test Command Works from economy.')
        pass

    @commands.command(help="Register for the Economy System!", brief="Register for Economy")
    async def registerecon(self, ctx, arg: Optional[discord.Member]):
        if await self.bot.is_prod_guild(ctx):
            return
        
        if arg == None:
            responseuser = ctx.message.author
        else:
            responseuser = arg

        member = responseuser
        testid = await self.bot.do_query("select user_id from economy")
        if str(responseuser.id) in str(testid):
            response = "You have already registered. Please use '|help Economy' for more commands."
            await ctx.message.channel.send(response)
        else:
            vals = f"'{member.id}'"
            m2 = f"{member.name}#{member.discriminator}\n"
            await self.bot.do_query(
                f"insert into economy (user_id,balance,uname) values ({member.id},1000,'{member.name}#{member.discriminator}');")
            response = "You have successfully registered! As a thank you, you get 1000 coins for free."
            await ctx.message.channel.send(response)

    @commands.command(help="Check your coin balance", brief="Check Balance", aliases=['bal', 'checkbal', 'balance'])
    async def checkbalance(self, ctx, arg: Optional[discord.Member]):
        if await self.bot.is_prod_guild(ctx):
            return

        if arg == None:
            responseuser = ctx.message.author
        else:
            responseuser = arg
        testid = await self.bot.do_query("select user_id from economy")
        if str(responseuser.id) in str(testid):
            bal = await self.bot.do_query(
                f"select balance from economy where user_id = {responseuser.id}")
            response = f"{responseuser}, Your coin balance is: {bal[0][0]} coins."
            await ctx.message.channel.send(response)
        else:
            response = "You aren't registered! Do |registerecon to join!"
            await ctx.message.channel.send(response)

    @commands.command(help="Adds to a coin balance.\nPower Users Only.", brief="Add Coins")
    async def addcoins(self, ctx, targeto, amt):
        if await self.bot.is_prod_guild(ctx):
            return
        target = targeto
        # print('targeto')
        # print(target)
        target2 = str(target)
        # print('target1')
        # print(target2)
        #target = target2[3:21]
        target = target2
        # print('targety')
        # print(target)
        amt = amt
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return

        testid = await self.bot.do_query(f"select user_id from economy where user_id = {responseuser.id}")
        #print("testid: " + str(testid))
        target = str(target)
        target = target[2:-1]
        #print("POOPPPP " + target[2:-1])

        if target in str(testid):
            print(amt)
            print(target)
            await self.bot.do_query(
                f"update economy set balance = balance + {amt} where user_id = {target}")
            bal = await self.bot.do_query(
                f"select balance from economy where user_id = {target}")
            response = f"You gave {amt} coins! Their coin balance is now: {bal[0][0]} coins."
            # await ctx.message.channel.send(response)
            print(response)
            print(str(ctx))
            await ctx.channel.send(response)
        else:
            response = "Your target isn't registered! Do |registerecon to join!"
            # await ctx.message.channel.send(response)
            print(response)
            print(str(ctx))
            await ctx.channel.send(response)

    @commands.command(help="Removes from a coin balance.\nPower Users Only.", brief="Remove Coins")
    async def removecoins(self, ctx, targeto, amt: int):
        if await self.bot.is_prod_guild(ctx):
            return
        target = targeto
        # print('targeto')
        # print(target)
        target2 = str(target)
        # print('target1')
        # print(target2)
        numeric_string = re.sub("[^0-9]", "", target2)
        # numeric_string = "".join(numeric_filter)
        target = numeric_string
        # print('targety')
        # print(target)
        amt = amt
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return

        testid = await self.bot.do_query("select user_id from economy")
        if str(responseuser.id) in str(testid):
            await self.bot.do_query(
                f"select balance from economy where user_id = {responseuser.id}")
            balold = Db.dangerexecute()
            #print("BALOLD " + str(balold))
            #print("AMT " + str(amt))

        testid = await self.bot.do_query("select user_id from economy")
        if str(target) in str(testid):
            if balold[0][0] >= amt:
                await self.bot.do_query(
                    f"update economy set balance = balance - {amt} where {target} = user_id;")
                toss = Db.dangerexecute()
                bal = await self.bot.do_query(
                    f"select balance from economy where user_id = {target}")
                response = f"You took {amt} coins from {targeto}! Their coin balance is now: {bal[0][0]} coins."
                # await ctx.message.channel.send(response)
                print(response)
                print(str(ctx))
                await ctx.channel.send(response)
            else:
                await self.bot.do_query(
                    f"update economy set balance = 0 where {target} = user_id;")
                bal = await self.bot.do_query(
                    f"select balance from economy where user_id = {target}")

                response = f"You took {amt} coins from {targeto}! Their coin balance is now: {bal[0][0]} coins."
                # await ctx.message.channel.send(response)
                print(response)
                print(str(ctx))
                await ctx.channel.send(response)
        else:
            response = "Your target isn't registered! Do |registerecon to join!"
            # await ctx.message.channel.send(response)
            print(response)
            print(str(ctx))
            await ctx.channel.send(response)

    async def removecoins2(self, ctx, targeto, amt: int):
        if await self.bot.is_prod_guild(ctx):
            return
        target = targeto
        # print('targeto')
        # print(target)
        target2 = str(target)
        # print('target1')
        # print(target2)
        numeric_string = re.sub("[^0-9]", "", target2)
        # numeric_string = "".join(numeric_filter)
        target = numeric_string
        # print('targety')
        # print(target)
        amt = amt
        responseuser = ctx.message.author

        testid = await self.bot.do_query("select user_id from economy")
        if str(responseuser.id) in str(testid):
            await self.bot.do_query(
                f"select balance from economy where user_id = {responseuser.id}")
            balold = Db.dangerexecute()
            #print("BALOLD " + str(balold))
            #print("AMT " + str(amt))

        testid = await self.bot.do_query("select user_id from economy")
        if str(target) in str(testid):
            if balold[0][0] >= amt:
                await self.bot.do_query(
                    f"update economy set balance = balance - {amt} where {target} = user_id;")
                bal = await self.bot.do_query(
                    f"select balance from economy where user_id = {target}")
                response = f"You took {amt} coins from {targeto}! Their coin balance is now: {bal[0][0]} coins."
                # await ctx.message.channel.send(response)
                print(response)
            else:
                await self.bot.do_query(
                    f"update economy set balance = 0 where {target} = user_id;")
                bal = await self.bot.do_query(
                    f"select balance from economy where user_id = {target}")
                response = f"You took {amt} coins from {targeto}! Their coin balance is now: {bal[0][0]} coins."
                # await ctx.message.channel.send(response)
                print(response)
        else:
            response = "Your target isn't registered! Do |registerecon to join!"
            # await ctx.message.channel.send(response)
            print(response)

    @commands.command(help="Gamble away all of your coins like so many people irl.", brief="Money Toilet")
    async def gamble(self, ctx):
        # TODO: add typing
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author.id
        responseuser2 = ctx.message.author.name
        responseuser3 = ctx.message.author
        testid = await self.bot.do_query("select user_id from economy")
        if str(responseuser) in str(testid):

            response = "Okay " + str(responseuser2) + "! Good luck!"
            await ctx.message.channel.send(response)
            # await self.removecoins(ctx, responseuser, 100)

            response = "And your number is......... "
            await ctx.message.channel.send(response)

            result = random.randint(0, 1000)
            response = result
            await ctx.message.channel.send(response)

            if result == 0:
                await self.removecoins2(ctx, responseuser, 99999999)
                response = "OOOOOOOOOHHHHH NOOOOO! BANKRUPT!!!! You lose all your coins. Rough go."
            else:
                if result < 101:
                    await self.removecoins2(ctx, responseuser, 1000)
                    response = "Tough luck! You lose 1000 coins! Ouch."
                else:
                    if result < 501:
                        await self.removecoins2(ctx, responseuser, 250)
                        response = "Aw, shucks. You lose 250 coins."
                    else:
                        if result < 900:
                            await self.addcoins2(ctx, responseuser, 250)
                            response = "Not bad! You gain 250 coins."
                        else:
                            if result < 1000:
                                await self.addcoins2(ctx, responseuser, 1000)
                                response = "Nice!!! You gain 1000 coins."
                            else:
                                if result == 1000:
                                    await self.addcoins2(ctx, responseuser, 777777)
                                    response = "JACKPOT!!!!!!!!!! YOU WIN THE JACKPOT OF 777,777 COINS! WOOHOOOOO!"
                                else:
                                    response = "This should not happen, if it does, something is broken"
            await ctx.message.channel.send(response)

            testid = await self.bot.do_query("select user_id from economy")
            if str(responseuser) in str(testid):
                balnew = await self.bot.do_query(
                    f"select balance from economy where user_id = {responseuser}")

            response = "Your new balance is " + str(balnew[0][0]) + " coins."
            await ctx.message.channel.send(response)

            # 0 bankrupt
            # 1-100 big loss
            # 101-500 little loss
            # 501-899 little gain
            # 900-999 big gain
            # 1000 jackpot
        else:
            response = "You aren't registered! Do |registerecon to join!"
            await ctx.message.channel.send(response)

    @ commands.command(help="Removes from your coin balance and adds to another person's balance.", brief="Gift Coins")
    async def giftcoins(self, ctx, targeto, amt):
        if await self.bot.is_prod_guild(ctx):
            return
        target = targeto
        # print('targeto')
        # print(target)
        target2 = str(target)
        # print('target1')
        # print(target2)
        target = target2[2:-1]
        # print('targety')
        # print(target)
        amt = amt
        responseuser = ctx.message.author
        testid = await self.bot.do_query("select user_id from economy")
        if str(responseuser.id) in str(testid):
            testid = await self.bot.do_query("select user_id from economy")
            if str(target) in str(testid):
                bal1 = await self.bot.do_query(
                    f"select balance from economy where user_id = {responseuser.id}")
                bal2 = await self.bot.do_query(
                    f"select balance from economy where user_id = {target}")

                # print('amt')
                # print(amt)
                # print('bal1')
                # print(bal1[0][0])

                if int(amt) > int(bal1[0][0]):
                    response = f"You don't have enough coins. You only have {bal1[0][0]} coins, and are trying to gift {amt}."
                    await ctx.message.channel.send(response)
                    return

                await self.bot.do_query(
                    f"update economy set balance = balance - {amt} where {responseuser.id} = user_id;")
                await self.bot.do_query(
                    f"update economy set balance = balance + {amt} where {target} = user_id;")
                bal1 = await self.bot.do_query(
                    f"select balance from economy where user_id = {responseuser.id}")
                bal2 = await self.bot.do_query(
                    f"select balance from economy where user_id = {target}")

                response = f"You gifted {amt} coins to {targeto}!\nYou have {bal1[0][0]} coins remaining."
                await ctx.message.channel.send(response)
            else:
                response = "Your target isn't registered! Do |registerecon to join!"
                await ctx.message.channel.send(response)
        else:
            response = "You aren't registered! Do |registerecon to join!"
            await ctx.message.channel.send(response)


async def setup(bot):
    await bot.add_cog(Economy(bot))
