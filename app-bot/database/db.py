# This file is used to interact with the database
from discord.ext import commands
from cns import *
import asyncpg
import asyncio

class Db(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._pool: asyncpg.Pool | None = None

    @property
    def pool(self) -> asyncpg.Pool:
        """Property for easier access to attr."""
        assert self._pool is not None

        return self._pool
    
    async def do_query(self, sql: str, *args) -> list[asyncpg.Record]:
        try:
            response = await self.bot.pool.fetch(sql, *args, timeout=60)
            return response
        except asyncio.TimeoutError:
            return []

async def setup(bot):
    await bot.add_cog(Db(bot))
