from discord.ext import commands
import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hux.main import Hux

logger = logging.getLogger(__name__)


class Testing(commands.Cog):
    def __init__(self, bot: Hux):
        self.bot = bot

    @commands.command(name="leave_server")
    @commands.is_owner()
    async def leave_server(self, ctx: commands.Context, guild_id: int):
        guild = ctx.guild if guild_id is None else self.bot.get_guild(guild_id)
        logger.info(f"leave_server invoked by {ctx.author} in guild: {ctx.guild}")
        if guild is None:
            await ctx.send("Guild not found.")
            return
        await ctx.send(f"Leaving server **{guild.name}**")
        logger.info(f"Left the server {guild.name} with id {guild.id}")
        await guild.leave()

    @commands.command(name="replied")
    @commands.is_owner()
    async def reply(self, ctx: commands.Context, *, text: str) -> None:
        message = await ctx.reply(f"{ctx.author.mention} has just said \n\n{text}")
        logger.info(message)


async def setup(bot: Hux):
    await bot.add_cog(Testing(bot))
