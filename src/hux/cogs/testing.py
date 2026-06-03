import logging

import discord
from discord.ext import commands

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
        self.reply_message = await ctx.reply("Placeholder")
        self.user_message = ctx.message
        logger.info(self.reply_message.id)

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        logger.info(f"{before.id} was edited to {after.id}")
        await after.add_reaction("\U0001f501")

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, user: discord.User | discord.Member
    ) -> None:
        if user.bot:
            return
        if reaction.emoji == "\U0001f501":
            await reaction.message.reply(
                f"reacted message is: {self.user_message.jump_url}\nbot's message is {self.reply_message.jump_url}"
            )


async def setup(bot: Hux):
    await bot.add_cog(Testing(bot))
