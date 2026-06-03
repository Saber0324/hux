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
        self.eval_message_pairs = []

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
    async def reply(self, ctx: commands.Context, *, text: str) -> None:
        reply_message = await ctx.reply("Fake eval result\n```hello world```")
        self.eval_message_pairs.append((reply_message, ctx.message))
        logger.info(f"User msg: {ctx.message.id}, bot msg: {reply_message.id}")

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        for _, user_message in self.eval_message_pairs:
            if user_message.id == after.id:
                await after.add_reaction("\U0001f501")

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, user: discord.User | discord.Member
    ) -> None:
        if user.bot:
            return

        for bot_reply, user_message in reversed(self.eval_message_pairs):
            if reaction.emoji == "\U0001f501" and user.id == user_message.author.id:
                await bot_reply.reply(
                    f"reacted message is: {user_message.jump_url}\n"
                    f"bot's message is: {bot_reply.jump_url}"
                )
                await reaction.message.clear_reactions()
                break


async def setup(bot: Hux):
    await bot.add_cog(Testing(bot))
