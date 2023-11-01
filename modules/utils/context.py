# borrowing from tom until I can figure out

from __future__ import annotations
import asyncio
from typing import Optional, Union, Callable, TYPE_CHECKING, Dict, Any

import discord
from discord.ext import commands

from . import paginator

if TYPE_CHECKING:
    from bot import Bot


def boolize(string: str) -> bool:
    string = string.lower()
    if string in ["true", "yes", "on", "enabled", "y", "t", "1"]:
        return True
    elif string in ["false", "no", "off", "disabled", "n", "f", "0"]:
        return False
    else:
        raise commands.UserInputError(
            f"{string} is not a recognized boolean option")


class Context(commands.Context):
    message: discord.Message
    bot: Bot
    author: Union[discord.User, discord.Member]
    user: Union[discord.User, discord.Member]
    #guild: user.guild[discord.Guild]
    #author = None

    async def paginate_fields(self, fields, **kwargs):
        pages = paginator.FieldPages(self, entries=fields, **kwargs)
        await pages.paginate()

    async def paginate(self, fields, **kwargs):
        pages = paginator.Pages(self, entries=fields, **kwargs)
        await pages.paginate()

    async def paginate_text(
        self, content: str, codeblock=False, codeblock_pre="", allow_stop=False, msg_kwargs: Dict[str, Any] = None
    ):
        if codeblock:
            pages = paginator.TextPages(self, content, prefix=f"```{codeblock_pre}", stop=allow_stop)
        else:
            pages = paginator.TextPages(self, content, prefix="", suffix="", stop=allow_stop)

        await pages.paginate(msg_kwargs)

    async def ask(
        self,
        question: Optional[str],
        return_bool=True,
        timeout=60,
        predicate: Optional[Callable[[discord.Message], bool]] = None,
        reply=False,
        reply_mention=False,
    ) -> Union[discord.Message, bool]:
        if question:
            if reply:
                await self.reply(question, mention_author=reply_mention)
            else:
                await self.send(question)

        predicate = predicate or (
            lambda msg: msg.channel == self.channel and msg.author == self.author)

        try:
            m: discord.Message = await self.bot.wait_for("message", timeout=timeout, check=predicate)
        except asyncio.TimeoutError:
            raise commands.CommandError(
                f"Timed out. Please respond within {timeout} seconds")

        if not return_bool:
            return m

        return boolize(m.content)

    @staticmethod
    def embed(**kwargs) -> discord.Embed:
        return discord.Embed(color=discord.Color.teal(), **kwargs)

    @staticmethod
    def embed_invis(**kwargs):
        return discord.Embed(color=0x2F3136, **kwargs)
