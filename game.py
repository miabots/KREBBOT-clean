# First Line of code for the game!

import discord
from discord.ext import commands

from database.db import Db

import pygame


import traceback

import traceback as formatter


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="", brief="", hidden=True)
    async def game(self, ctx):
        if await self.bot.is_prod_guild(ctx):
            return

        pygame.init()
        print("Game")

        # color library

        global red
        global green
        global blue
        global white
        global black
        global purple
        global orange

        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        white = (255, 255, 255)
        black = (0, 0, 0)
        purple = (127, 0, 255)
        orange = (255, 165, 0)
        # red = (255, 0, 0)
        # red = (255, 0, 0)
        # red = (255, 0, 0)
        # red = (255, 0, 0)

        global screen
        global font
        screen = pygame.display.set_mode([450, 800])
        pygame.display.set_caption('Notte a Problem Squared')
        background = black
        framerate = 60
        font = pygame.font.Font('freesansbold.ttf', 32)
        timer = pygame.time.Clock()
        global score

        score = 0

        # gamer variables

        green_value = 1
        red_value = 2
        orange_value = 3
        white_value = 4
        purple_value = 5

        draw_green = False
        draw_red = False
        draw_orange = False
        draw_white = False
        draw_purple = False

        green_length = 0
        red_length = 0
        orange_length = 0
        white_length = 0
        purple_length = 0

        green_speed = 5
        red_speed = 4
        orange_speed = 3
        white_speed = 2
        purple_speed = 1

        def draw_task(color, ycoord, value, draw, length, speed):
            global score
            global screen
            global black
            global font
            if draw and length < 290:
                length += speed
            elif length >= 290:
                draw = False
                length = 0
                score += value

            task = pygame.draw.circle(screen, color, (50, ycoord), 30, 5)
            pygame.draw.rect(screen, color, [100, ycoord - 25, 300, 50])
            pygame.draw.rect(screen, black, [105, ycoord - 20, 290, 40])
            pygame.draw.rect(screen, color, [100, ycoord - 25, length, 50])

            valuetext = font.render(str(value), True, white)
            screen.blit(valuetext, (40, ycoord - 15))
            return task, length, draw

        running = True
        while running:

            timer.tick(framerate)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if task1.collidepoint(event.pos):
                        draw_green = True
                    if task2.collidepoint(event.pos):
                        draw_red = True
                    if task3.collidepoint(event.pos):
                        draw_orange = True
                    if task4.collidepoint(event.pos):
                        draw_white = True
                    if task5.collidepoint(event.pos):
                        draw_purple = True

            screen.fill(background)

            task1, green_length, draw_green = draw_task(green, 90, green_value, draw_green, green_length, green_speed)
            task2, red_length, draw_red = draw_task(red, 160, red_value, draw_red, red_length, red_speed)
            task3, orange_length, draw_orange = draw_task(orange, 240, orange_value, draw_orange, orange_length, orange_speed)
            task4, white_length, draw_white = draw_task(white, 320, white_value, draw_white, white_length, white_speed)
            task5, purple_length, draw_purple = draw_task(purple, 410, purple_value, draw_purple, purple_length, purple_speed)

            display_score = font.render('Money: $' + str(round(score, 2)), True, white, black)
            screen.blit(display_score, (10, 5))
            pygame.display.flip()

        pygame.quit()


async def setup(bot):
    await bot.add_cog(Game(bot))
