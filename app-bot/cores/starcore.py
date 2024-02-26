# starcore.py
# core bot loop for Dynamic and Static behavior via reaction handling

from datetime import datetime

import discord
from discord.ext import commands

from cns import *

from typing import Optional, Union
import traceback

class Reactions(commands.Cog):
    """
    Starboard and other reaction based commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.intents = bot.intents

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):

        guild = self.bot.get_guild(ctx.guild_id)
        # guild = self.bot.get_guild(754510720590151751)

        if guild.id not in [754510720590151751,1175277956885651526]: #dove, pr2
            return

        if guild.id == 754510720590151751:
            schannel = guild.get_channel(1170040533838729327)
        elif guild.id == 1175277956885651526:
            schannel = guild.get_channel(1178764942279716904)
        # channel = guild.get_channel(925930479037853736)  # nottes home
        member = guild.get_member(ctx.user_id)

        if not bool(member):
            return

        if member.bot:
            return

        emojilist = ["⭐"]

        if ctx.emoji.name in emojilist:
            #Mia, Rose, Trey, Fifi, Geo
            userlist = [181157857478049792,842062444292603915,282318464465502208,816732742515294208,233762709932474370]

            if member.id in userlist:
                print("STARCORE CALLED")
                try:

                    channel_id = ctx.channel_id
                    message_id = ctx.message_id
                    user_id = ctx.user_id

                    message = await self.bot.get_channel(channel_id).fetch_message(int(ctx.message_id))


                    embed = discord.Embed(
                        title=f"Message from {message.author.display_name} ({message.author.name})",
                        description=message.content,
                        color=discord.Color.blue(),
                        timestamp=message.created_at
                    )
                    
                    if message.attachments:
                        embed.set_image(url=message.attachments[0].url)
                            
                    ref = "https://discord.com/channels/" + str(message.guild.id) + "/" + str(message.channel.id) + "/" + str(message.id)
                    embed.add_field(name="Original Message:", value=f'[Click here]({ref})',inline=True)
                    embed.set_footer(text=f"In #{message.channel.name}")

                    await schannel.send(embed=embed)
                except discord.NotFound:
                    print("Message not found.")
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
            else:
                return

async def setup(bot):
    await bot.add_cog(Reactions(bot))
