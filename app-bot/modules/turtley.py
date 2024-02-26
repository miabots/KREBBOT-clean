# turtley.py
from cns import *
import turtle
from turtle import *
from PIL import Image
import random
import os
import discord
from discord.ext import commands

colorsg = ["red", "green", "blue", "orange", "purple", "pink", "yellow"]

turtnum = 0


class Turtley(commands.Cog):
    """
    Draw a fun picture with a command! Try it out in the bot channel!
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def convert_to_png(self, path):
        img = Image.open(path)
        img.save("./img.png")

    def setTurtleColors(self, *argv):
        # for arg in argv:
        global colorsg
        # del argv[0]
        colorsg = list(argv)
        print(colorsg)
        colorsg = colorsg.pop(0)
        # print(colorsg)
        colorsg = colorsg[1:]
        # print(colorsg)
        print('Colors Setting Now To:')
        print(colorsg)
        # pass

    def draw_turtle(self, widthx, lengthx, size, turn):
        global turtnum

        colors = colorsg  # Make a list of colors to pick from

        # turtle.speed(speed=0)
        turtle.reset()
        turtle.width(widthx)  # What does this line do?

        length = lengthx

        turtle.tracer(0, 0)

        for count in range(size):
            color = random.choice(colors)  # Choose a random color
            turtle.forward(length)
            turtle.right(turn)
            turtle.color(color)  # Why is color spelt like this?
            length = length + 5

        turtle.update()
        ts = turtle.getcanvas()
        ts.postscript(file="turtle.ps", colormod='color')
        psimage = Image.open('turtle.ps')
        self.convert_to_png('turtle.ps')
        # TurtleScreen._RUNNING = False
        # turtle.bye()
        turtnum += 1

    def best_turtle(self):
        global turtnum
        widthx = 5
        lengthx = 5
        size = 500
        turn = 70
        colors = colorsg  # Make a list of colors to pick from

        # turtle.speed(speed=0)
        turtle.reset()
        turtle.width(widthx)  # What does this line do?

        length = lengthx

        turtle.tracer(0, 0)

        for count in range(size):
            color = random.choice(colors)  # Choose a random color
            turtle.forward(length)
            turtle.right(turn)
            turtle.color(color)  # Why is color spelt like this?
            length = length + 5

        turtle.update()
        ts = turtle.getcanvas()
        ts.postscript(file="turtle.ps", colormod='color')
        psimage = Image.open('turtle.ps')
        self.convert_to_png('turtle.ps')
        # TurtleScreen._RUNNING = False
        # turtle.bye()
        turtnum += 1

    @commands.command(help="The turtle command can be used to draw fun 'turtles'!\nTurtles are basically just fun shapes you can make.\nYou will need to specify the arguments like:\n|turtle linewidth(1-10 ish),linelength(1-100ish),picturesize(50-500ish),turn(default 135)\nHere is an example: |turtle 10,10,50,135", brief="Draw an image using a command!")
    async def turtle(self, ctx):
        print(ctx.message.content)
        responseuser = ctx.message.author
        com1 = ctx.message.content[8:]
        chunks = com1.split(',')
        print(chunks)
        print(len(chunks))
        # print(chunks[1])
        # print(chunks[2])
        # print(chunks[3])

        if len(chunks) == 4:

            if str(responseuser) in cns.POWER_USERS:

                self.draw_turtle(int(chunks[0]), int(chunks[1]),
                                 int(chunks[2]), int(chunks[3]))
                await ctx.message.channel.send(files=[discord.File("img.png", filename="aaaa.png")])
                os.remove("turtle.ps")
                os.remove("img.png")
            else:
                self.draw_turtle(int(chunks[0]), int(chunks[1]),
                                 int(chunks[2]), int(chunks[3]))
                await ctx.message.channel.send(files=[discord.File("img.png", filename="aaaa.png")])
                os.remove("turtle.ps")
                os.remove("img.png")
        else:
            response = 'You need to specify the arguments. Try again - like: |turtle linewidth(1-10 ish),linelength(1-100ish),picturesize(50-500ish),turn(default 135) so like |turtle 10,10,50,135'
            responseuser = ctx.message.author
            await ctx.message.channel.send(response)

    @commands.command(help="Currently restricted to power users, but is used to set the colors when drawing turtles.", brief="Changes the colors used for drawing turtles")
    async def setcolors(self, ctx):
        responseuser = ctx.message.author
        com1 = ctx.message.content[8:]
        chunks = com1.split(',')
        print(len(chunks))

        if len(chunks) == 7:  # number of colors
            if str(responseuser) in cns.POWER_USERS:
                print('CHUNK DATA: ')
                print(chunks)
                self.setTurtleColors(chunks)
                response = 'Executed Successfully.'
                responseuser = ctx.message.author
                await ctx.message.channel.send(response)
            else:
                pass
        else:
            response = 'Nope'
            responseuser = ctx.message.author
            await ctx.message.channel.send(response)

    @commands.command(help="Partially implemented, eventually will work properly. Power users only at this time.", brief="Shows the current 'best' Turtle")
    async def bist(self, ctx):
        responseuser = ctx.message.author
        # response = 'Test: '
        responseuser = ctx.message.author

        if str(responseuser) in cns.POWER_USERS:
            self.best_turtle()
            await ctx.message.channel.send(files=[discord.File("img.png", filename="aaaa.png")])
        else:
            self.best_turtle()
            await ctx.message.channel.send(files=[discord.File("img.png", filename="aaaa.png")])


async def setup(bot):
    await bot.add_cog(Turtley(bot))
