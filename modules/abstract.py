# jishaku.py
# custom jsk impl

from discord.ext import commands
import asyncio
#from blastoff import bot

from jishaku.features.python import PythonFeature
from jishaku.features.root_command import RootCommand

import jishaku
from jishaku.features.baseclass import Feature

from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES


class CustomDebugCog(PythonFeature, RootCommand):
    @Feature.Command(parent="jsk", name="notte")
    async def jsk_foobar(self, ctx: commands.Context):
        # await ctx.send("Hello there!")
        print("beans")
    pass


def setup(bot):
    bot.add_cog(CustomDebugCog(bot=bot))
