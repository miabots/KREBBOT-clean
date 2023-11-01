# commands_db.py

from discord.ext import commands

from database.db import Db

#insertdb, selectdb, parseinsertsql, testsql, con, insertdb2

from cns import *


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global executionsql
    executionsql = ""

    @commands.command(help="This command is used to test database functionality.\nIt is only usable by Power Users.", brief="Power User Command")
    async def querytest(self, ctx, table):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            return
        selection = Db.selectdb(table)
        # print(selection)
        helptext = ""
        #helptext += f"\n"
      #  helptext += "ID_______VALUE_________NUMBER"
      #  helptext += f"\n"
       # print(helptext)
        for row in selection:
            helptext += f"{row}\n"
        #    print(helptext)
        #helptext += "```"
        # print(helptext)
        #helptext = "``` FUCKING WORK ```"
        while len(helptext) > 0:
            #helptext = "```" + helptext + "```"
            print('len = ' + str(len(helptext)))
            # print(helptext[:1000])
            funtext = "```" + helptext[:1000] + "```"
            await ctx.send(funtext)
            helptext = helptext[1000:]
            print(funtext)

    @commands.command(help="Test command for basic insert into db tests. Doesn't do much.\nIt is only usable by Power Users.", brief="Power User Command")
    async def insert(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) in cns.POWER_USERS:
            Db.insertdb()
            response = 'Command Executed.'
        else:
            pass
            # response = responseuser
        await ctx.message.channel.send(response)

    @commands.command(help="Test command for upcoming features.\nIt is only usable by Power Users.", brief="Power User Command")
    async def register(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) in cns.POWER_USERS:
            # registerdb()

            did = ctx.message.author.id
            dname = ctx.message.author.name
            ddes = ctx.message.author.discriminator

            print('I believe that the follow data will go (ID, NAME, DDES)')
            print(did)
            print(dname)
            print(ddes)

            sqltext = f"INSERT INTO users (discord_id,discord_name,discord_des) VALUES ('{did}','{dname}','{ddes}')"
            print(sqltext)
            Db.insertdb2(sqltext)
            response = 'Command Executed.'
        else:
            pass
            # response = responseuser
        await ctx.message.channel.send(response)

    @commands.command(help="Currently does nothing.\nIt is only usable by Power Users.", brief="Power User Command")
    async def updatesql(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) in cns.POWER_USERS:
            print(ctx.message.content)
            mymessage = ctx.message.content[11:]
            print(mymessage)
            Db.parseinsertsql(mymessage)
            response = 'Command Executed.'
        else:
            pass
            # response = responseuser
        await ctx.message.channel.send(response)

    @commands.command(help="Basic test command to confirm that the module is loaded and responding.\nIt is only usable by Power Users.", brief="Power User Command")
    async def testdb(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            return
        print('Test Command Works from DB.')
        pass

    @commands.command(help="Inits the DB if needed.\nIt is only usable by Power Users.", brief="Power User Command")
    async def initdb1(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            return
        Db.initdb()
        pass

    @commands.command(help="Extremely Dangerous Command.\nIt is only usable by Power Users.", brief="Power User Command")
    async def dangerset1(self, ctx, sql):
        if ctx.guild.id is None:
            return
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            response = f"Attention <@!858945219448799263>, the user {responseuser} has just attempted to invoke a dangerous command."
            await ctx.message.channel.send(response)
            return
        global executionsql
        executionsql = sql
        Db.dangerset(sql)
        pass

    @commands.command(help="Extremely Dangerous Command.\nIt is only usable by Power Users.", brief="Power User Command")
    async def dangerexecute1(self, ctx):
        if ctx.guild.id is None:
            return
        if await self.bot.is_prod_guild(ctx):
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            print('Returning due to lack of Power User permissions.')
            response = f"Attention <@!858945219448799263>, the user {responseuser} has just attempted to invoke a dangerous command."
            await ctx.message.channel.send(response)
            return
        global executionsql
        result = Db.dangerexecute()
        print(str(result))
        pass


async def setup(bot):
    await bot.add_cog(Database(bot))
