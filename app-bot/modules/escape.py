# escape.py
# Escape Room For Parkvivor!
import discord
from discord.ext import commands
from discord import app_commands
from cns import *

import random
import time

class Escape(commands.Cog):
    """
    Escape Room For Parkvivor!
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db
        self.board = {
            "r1": {"floor": 0, "row": 0, "col": 0, "name": "f0r0c0", "result": "You are here!", "visited": False, "raccoons": 0},
            "r2": {"floor": 0, "row": 0, "col": 1, "name": "f0r0c1", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r3": {"floor": 0, "row": 0, "col": 2, "name": "f0r0c2", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r4": {"floor": 0, "row": 0, "col": 3, "name": "f0r0c3", "result": "You are in a hallway...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r5": {"floor": 0, "row": 1, "col": 0, "name": "f0r1c0", "result": "You are in a conference room!", "visited": False, "raccoons": 0},
            "r6": {"floor": 0, "row": 1, "col": 1, "name": "f0r1c1", "result": "You are in a hallway...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r7": {"floor": 0, "row": 1, "col": 2, "name": "f0r1c2", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r8": {"floor": 0, "row": 1, "col": 3, "name": "f0r1c3", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r9": {"floor": 0, "row": 2, "col": 0, "name": "f0r2c0", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r10": {"floor": 0, "row": 2, "col": 1, "name": "f0r2c1", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
            "r11": {"floor": 0, "row": 2, "col": 2, "name": "f0r2c2", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r12": {"floor": 0, "row": 2, "col": 3, "name": "f0r2c3", "result": "You find the stairs to the next floor! You are now on a new floor.", "visited": False, "raccoons": 0},
            "r13": {"floor": 0, "row": 3, "col": 0, "name": "f0r3c0", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
            "r14": {"floor": 0, "row": 3, "col": 1, "name": "f0r3c1", "result": "You are in the supply closet. You see a cute raccoon drinking some chemicals. It seems friendly. You pat it on the head.", "visited": False, "raccoons": 0},
            "r15": {"floor": 0, "row": 3, "col": 2, "name": "f0r3c2", "result": "You enter the employee lounge. Unfortunately for you, the only things lounging in here are 3 raccoons.", "visited": False, "raccoons": 3},
            "r16": {"floor": 0, "row": 3, "col": 3, "name": "f0r3c3", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r17": {"floor": 1, "row": 0, "col": 0, "name": "f1r0c0", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
            "r18": {"floor": 1, "row": 0, "col": 1, "name": "f1r0c1", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r19": {"floor": 1, "row": 0, "col": 2, "name": "f1r0c2", "result": "You are in a hallway...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r20": {"floor": 1, "row": 0, "col": 3, "name": "f1r0c3", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r21": {"floor": 1, "row": 1, "col": 0, "name": "f1r1c0", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r22": {"floor": 1, "row": 1, "col": 1, "name": "f1r1c1", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r23": {"floor": 1, "row": 1, "col": 2, "name": "f1r1c2", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r24": {"floor": 1, "row": 1, "col": 3, "name": "f1r1c3", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r25": {"floor": 1, "row": 2, "col": 0, "name": "f1r2c0", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r26": {"floor": 1, "row": 2, "col": 1, "name": "f1r2c1", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
            "r27": {"floor": 1, "row": 2, "col": 2, "name": "f1r2c2", "result": "You are in a conference room!", "visited": False, "raccoons": 0},
            "r28": {"floor": 1, "row": 2, "col": 3, "name": "f1r2c3", "result": "These are the stairs you just came from!", "visited": False, "raccoons": 0},
            "r29": {"floor": 1, "row": 3, "col": 0, "name": "f1r3c0", "result": "You find the stairs to the next floor! You are now on a new floor.", "visited": False, "raccoons": 0},
            "r30": {"floor": 1, "row": 3, "col": 1, "name": "f1r3c1", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r31": {"floor": 1, "row": 3, "col": 2, "name": "f1r3c2", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r32": {"floor": 1, "row": 3, "col": 3, "name": "f1r3c3", "result": "You enter the employee lounge. Unfortunately for you, the only thing lounging in here is a raccoon.", "visited": False, "raccoons": 1},
            "r33": {"floor": 2, "row": 0, "col": 0, "name": "f2r0c0", "result": "You are in a conference room!", "visited": False, "raccoons": 0},
            "r34": {"floor": 2, "row": 0, "col": 1, "name": "f2r0c1", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r35": {"floor": 2, "row": 0, "col": 2, "name": "f2r0c2", "result": "You find the stairs to the next floor! You are now on a new floor.", "visited": False, "raccoons": 0},
            "r36": {"floor": 2, "row": 0, "col": 3, "name": "f2r0c3", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r37": {"floor": 2, "row": 1, "col": 0, "name": "f2r1c0", "result": "You enter the employee lounge. Unfortunately for you, the only things lounging in here are 3 raccoons.", "visited": False, "raccoons": 3},
            "r38": {"floor": 2, "row": 1, "col": 1, "name": "f2r1c1", "result": "You are in a hallway...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r39": {"floor": 2, "row": 1, "col": 2, "name": "f2r1c2", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r40": {"floor": 2, "row": 1, "col": 3, "name": "f2r1c3", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r41": {"floor": 2, "row": 2, "col": 0, "name": "f2r2c0", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r42": {"floor": 2, "row": 2, "col": 1, "name": "f2r2c1", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r43": {"floor": 2, "row": 2, "col": 2, "name": "f2r2c2", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r44": {"floor": 2, "row": 2, "col": 3, "name": "f2r2c3", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
            "r45": {"floor": 2, "row": 3, "col": 0, "name": "f2r3c0", "result": "These are the stairs you just came from!", "visited": False, "raccoons": 0},
            "r46": {"floor": 2, "row": 3, "col": 1, "name": "f2r3c1", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r47": {"floor": 2, "row": 3, "col": 2, "name": "f2r3c2", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
            "r48": {"floor": 2, "row": 3, "col": 3, "name": "f2r3c3", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r49": {"floor": 3, "row": 0, "col": 0, "name": "f3r0c0", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r50": {"floor": 3, "row": 0, "col": 1, "name": "f3r0c1", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r51": {"floor": 3, "row": 0, "col": 2, "name": "f3r0c2", "result": "These are the stairs you just came from!", "visited": False, "raccoons": 0},
            "r52": {"floor": 3, "row": 0, "col": 3, "name": "f3r0c3", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r53": {"floor": 3, "row": 1, "col": 0, "name": "f3r1c0", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r54": {"floor": 3, "row": 1, "col": 1, "name": "f3r1c1", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r55": {"floor": 3, "row": 1, "col": 2, "name": "f3r1c2", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
            "r56": {"floor": 3, "row": 1, "col": 3, "name": "f3r1c3", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r57": {"floor": 3, "row": 2, "col": 0, "name": "f3r2c0", "result": "You are in a hallway!", "visited": False, "raccoons": 0},
            "r58": {"floor": 3, "row": 2, "col": 1, "name": "f3r2c1", "result": "You are in a courtyard...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r59": {"floor": 3, "row": 2, "col": 2, "name": "f3r2c2", "result": "You are in a courtyard!", "visited": False, "raccoons": 0},
            "r60": {"floor": 3, "row": 2, "col": 3, "name": "f3r2c3", "result": "You are in an office...and so is a raccoon!", "visited": False, "raccoons": 1},
            "r61": {"floor": 3, "row": 3, "col": 0, "name": "f3r3c0", "result": "You are in the Cafe!", "visited": False, "raccoons": 0},
            "r62": {"floor": 3, "row": 3, "col": 1, "name": "f3r3c1", "result": "You are in a conference room!", "visited": False, "raccoons": 0},
            "r63": {"floor": 3, "row": 3, "col": 2, "name": "f3r3c2", "result": "You find the exit and escape!", "visited": False, "raccoons": 0},
            "r64": {"floor": 3, "row": 3, "col": 3, "name": "f3r3c3", "result": "You are in an office...and so are 2 raccoons!", "visited": False, "raccoons": 2},
        }

        print("Escape Room Loaded")

    @commands.command(help="",hidden=True)
    async def showcell(self, ctx, cell):
        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        
        for i in self.board:
            if self.board[i]['name'] == cell:
                await ctx.channel.send(self.board[i])

    @commands.command(help="",hidden=True)
    async def f10toggle(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        
        if cns.f10con == False:
            cns.f10con = True
        else:
            cns.f10con = False
        
        await ctx.channel.send("f10con is now " + str(cns.f10con))

    @app_commands.guilds(discord.Object(id=754510720590151751),discord.Object(id=1175277956885651526))
    @app_commands.command(name="choose")
    async def choose(self, interaction: discord.Interaction, cell: str) -> None:
        """ Make a choice in the escape room! """

        if cns.f10con == False:
            return
        if interaction.user.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = interaction.user
        member = responseuser

        cfloor = await self.bot.do_query(f"select current_floor from escape where discord_id = {responseuser.id}")
        cfloor = cfloor[0][0]
        #print(cfloor)
        cfloor = int(cfloor)

        cell = "f" + str(cfloor) + cell

        gameon = await self.bot.do_query(f"select game_on from escape where discord_id = {responseuser.id}")
        gameon = gameon[0][0]
        if gameon is not None: gameon = int(gameon)
        if gameon == 0 or gameon is None:
            await interaction.response.send_message("The game is not running. Please start the game with /startescape.", ephemeral=True)
            return

        
        moves = await self.bot.do_query(f"select moves from escape where discord_id = {responseuser.id}")
        moves = moves[0][0]
        moves = int(moves)
        moves = moves + 1

        f0w = await self.bot.do_query(f"select f0w from escape where discord_id = {responseuser.id}")
        f0w = f0w[0][0]
        f1w = await self.bot.do_query(f"select f1w from escape where discord_id = {responseuser.id}")
        f1w = f1w[0][0]
        f2w = await self.bot.do_query(f"select f2w from escape where discord_id = {responseuser.id}")
        f2w = f2w[0][0]
        f3w = await self.bot.do_query(f"select f3w from escape where discord_id = {responseuser.id}")
        f3w = f3w[0][0]

        toss = await self.bot.do_query(f"update escape set moves = {moves} where discord_id = {responseuser.id}")

        raccoons = 0
        for i in self.board:
            if self.board[i]['name'] == cell:
                raccoons = self.board[i]['raccoons']

        toss = await self.bot.do_query(f"update escape set raccoons = raccoons + {raccoons} where discord_id = {responseuser.id}")
        
        #for i in self.board:
        #    if self.board[i]['name'] == cell:
        #            await interaction.response.send_message(self.board[i]['result'])
        #print(cell)
        #print(f0w)
        resp = ""

        if cfloor == 0 and cell == f0w:
            print("0")
            resp = "You have found the exit! You move to the next floor!\n"
            cfloor = 1
        if cfloor == 1 and cell == f1w:
            print("1")
            resp = "You have found the exit! You move to the next floor!\n"
            cfloor = 2
        if cfloor == 2 and cell == f2w:
            print("2")
            resp = "You have found the exit! You move to the next floor!\n"            
            cfloor = 3
        if (cfloor == 3 and cell == f3w) or (cell == "f0bypass" and responseuser.id == 181157857478049792):
            #WIN CONDITION
            
            resp = ""
            print("3")

            resp = resp + "You have found the exit! You made it out! Congratulations!\n"
            resp = resp +  "Thank you for playing the Escape Room!\n"

            etime = time.time()
            toss = await self.bot.do_query(f"update escape set end_time = {etime} where discord_id = {responseuser.id}")

            stime = await self.bot.do_query(f"select start_time from escape where discord_id = {responseuser.id}")
            stime = stime[0][0]
            ttime = etime - stime
            toss = await self.bot.do_query(f"update escape set last_time = {ttime} where discord_id = {responseuser.id}")

            btime = await self.bot.do_query(f"select best_time from escape where discord_id = {responseuser.id}")
            btime = btime[0][0]

            resp = resp + "Your time was: " + str(round(ttime, 2)) + " seconds."
            
            moves = await self.bot.do_query(f"select moves from escape where discord_id = {responseuser.id}")
            moves = moves[0][0]           
            
            resp = resp +  "Your moves were: " + str(moves) + " moves.\n"

            rc = await self.bot.do_query(f"select raccoons from escape where discord_id = {responseuser.id}")
            rc = rc[0][0]           
            
            resp = resp +  "You ran into " + str(rc) + " raccoons.\n"

            if ttime < btime or btime == 0:
                toss = await self.bot.do_query(f"update escape set best_time = {ttime} where discord_id = {responseuser.id}")
                resp = resp +  "You have a new best time! Play again if you want to try to beat it!\n"
                if btime != 0:
                    resp = resp + "Previous best time was: " + str(btime) + " seconds.\n"
            

            bmoves = await self.bot.do_query(f"select best_moves from escape where discord_id = {responseuser.id}")
            bmoves = bmoves[0][0]

            if moves < bmoves or bmoves == 0:
                toss = await self.bot.do_query(f"update escape set best_moves = {moves} where discord_id = {responseuser.id}")
                resp = resp +  "You have a new best moves! Play again if you want to try to beat it!\n"
                if bmoves != 0:
                    resp = resp + "Previous best moves was: " + str(bmoves) + " moves.\n"
            
            toss = await self.bot.do_query(f"update escape set current_floor = 0 where discord_id = {responseuser.id}")

            toss = await self.bot.do_query(f"update escape set game_on = 0 where discord_id = {responseuser.id}")

            cfloor = 0
            raccoons = 0
            toss = await self.bot.do_query(f"update escape set raccoons = {raccoons} where discord_id = {responseuser.id}")

        if resp == "":
            for i in self.board:
                if self.board[i]['name'] == cell:
                    resp = self.board[i]['result']
        print(resp)
        toss = await self.bot.do_query(f"update escape set current_floor = {cfloor} where discord_id = {responseuser.id}")
        await interaction.response.send_message(resp)

    
    @app_commands.guilds(discord.Object(id=754510720590151751),discord.Object(id=1175277956885651526))
    @app_commands.command(name="startescape")
    async def startescape(self, interaction: discord.Interaction) -> None:
        """ Play the escape room! """
        if await self.bot.is_prod_guild(interaction):
            print('Returning due to Production Guild.')
            return
        if cns.f10con == False:
            return
        responseuser = interaction.user
        member = responseuser

        self.setwinrooms(interaction)

        testid = await self.bot.do_query("select discord_id from escape")
        if str(responseuser.id) in str(testid):
            print("User exists")
            tossa = await self.bot.do_query("update escape set current_floor = 0 where discord_id = $1", responseuser.id)
            toss2 = await self.bot.do_query("update escape set moves = 0 where discord_id = $1", responseuser.id)
            toss3 = await self.bot.do_query("update escape set game_on = 1 where discord_id = $1", responseuser.id)
        else:
            print("User does not exist, adding")
            toss = await self.bot.do_query("insert into escape (discord_id,current_floor) values ($1,0)", responseuser.id)
            toss = await self.bot.do_query("update escape set best_time = 0 where discord_id = $1", responseuser.id)
            toss = await self.bot.do_query("update escape set best_moves = 0 where discord_id = $1", responseuser.id)
            toss = await self.bot.do_query("update escape set game_on = 1 where discord_id = $1", responseuser.id)
            toss = await self.bot.do_query("update escape set moves = 0 where discord_id = $1", responseuser.id)
            toss = await self.bot.do_query("update escape set raccoons = 0 where discord_id = $1", responseuser.id)

        toss = await self.bot.do_query("update escape set f0w = $1 where discord_id = $2", cns.f0w, responseuser.id)
        toss = await self.bot.do_query("update escape set f1w = $1 where discord_id = $2", cns.f1w, responseuser.id)
        toss = await self.bot.do_query("update escape set f2w = $1 where discord_id = $2", cns.f2w, responseuser.id)
        toss = await self.bot.do_query("update escape set f3w = $1 where discord_id = $2", cns.f3w, responseuser.id)

        stime = time.time()
        toss = await self.bot.do_query("update escape set start_time = $1 where discord_id = $2", stime, responseuser.id)
        
        response = "Hello! Welcome to the Escape Room.\nRooms are selected using row and column numbers. e.g. r0c0 is row 0, column 0. The numbers increment left to right and top to bottom.\nEnter the command choose with the Room Name to choose a Room. e.g. choose r0c0\nYour time starts NOW! Good luck!"
        await interaction.response.send_message(response)


    def getcell(self, interaction, floor, row, col):
        cell = "f" + str(floor) + "r" + str(row) + "c" + str(col)
        cell = str(cell)
        return cell
    
    def setwinrooms(self, interaction):
        f0wr = random.randint(0, 3)
        f0wc = random.randint(0, 3)
        f1wr = random.randint(0, 3)
        f1wc = random.randint(0, 3)
        f2wr = random.randint(0, 3)
        f2wc = random.randint(0, 3)
        f3wr = random.randint(0, 3)
        f3wc = random.randint(0, 3)

        #cns.f0w = self.getcell(interaction, 0, f0wr, f0wc)
        #cns.f1w = self.getcell(interaction, 1, f1wr, f1wc)
        #cns.f2w = self.getcell(interaction, 2, f2wr, f2wc)
        #cns.f3w = self.getcell(interaction, 3, f3wr, f3wc)

        print("Win Rooms Set")
        print(cns.f0w)
        print(cns.f1w)
        print(cns.f2w)
        print(cns.f3w)

async def setup(bot):
    await bot.add_cog(Escape(bot))