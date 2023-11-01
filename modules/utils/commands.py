# commands.py
# am borrowing this from Tom until I can figure it out


from __future__ import annotations
from typing import TYPE_CHECKING, Dict, TypedDict, List, Union

from discord.ext import commands

if TYPE_CHECKING:
    from bot import Bot
    from .context import Context
    from .parse import Actions, Group
    from .dispatch import Dispatch


def setup(bot: Bot):
    bot.add_cog(Commands(bot))


class PartialCommand(TypedDict):
    id: int
    cfg_id: int
    name: str
    help: str
    action_ids: List[int]
    permission_group: str


class CommandArgument(TypedDict):
    id: int
    name: str
    type: str
    optional: bool


class Command(PartialCommand):
    arguments: List[CommandArgument]
    actions: List[Actions]


class Commands(commands.Cog):
    """
    Custom command related commands.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.command_cache: Dict[int, Dict[int, Union[PartialCommand, Command]]] = {}
        self.command_lookup: Dict[int, Dict[str, int]] = {}

    async def dispatch_hook(self, ctx: Context) -> None:
        # if ctx.guild.id not in self.command_cache:
        #    await self.lazy_load_cache(ctx.guild.id)

        # if ctx.invoked_with not in self.command_lookup[ctx.guild.id]:
        #    return

        cmd = self.command_cache[ctx.guild.id][self.command_lookup[ctx.guild.id][ctx.invoked_with]]

        dispatch: Dispatch = self.bot.get_cog("Dispatch")  # type: ignore
        await dispatch.filled.wait()

        if not await self.can_run(ctx, cmd):
            return await ctx.reply(
                "You do not have permission to run this command", mention_author=False, delete_after=3
            )

        parser = await dispatch.get_context(ctx.guild.id)

        await parser.run_command(ctx)

    async def can_run(self, ctx: Context, cmd: Union[PartialCommand, Command]) -> bool:
        if not cmd["permission_group"]:
            return True

        dispatch: Dispatch = self.bot.get_cog("Dispatch")  # type: ignore
        if not dispatch:
            return False

        group: Group = dispatch.cached_triggers["groups"][ctx.guild.id][cmd["permission_group"]]
        if ctx.author.id in group["users"]:
            return True

        elif any(ctx.author._roles.has(x) for x in group["roles"]):  # noqa
            return True

        return False
