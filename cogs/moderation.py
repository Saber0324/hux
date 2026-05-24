import logging
import discord
from discord import app_commands
from discord.ext import commands
import datetime
from templates.models import parse_time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Hux


class Moderation(commands.Cog):
    def __init__(self, bot: Hux):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        user: discord.Member,
        *,
        reason: str = "No reason provided.",
    ) -> None:
        await user.kick(reason=reason)
        await ctx.send(f"{user.name} has been kicked. \nReason: {reason}")

    @app_commands.command(
        name="timeout",
        description="times out an user for a determined period of time.",
    )
    @app_commands.describe(
        duration="The amount of time the user will be timed out.",
        reason="The reason for this user's time out",
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        duration: str,
        *,
        reason: str = "No reason provided.",
    ) -> None:
        logging.info(f"{ctx.author} has timed out {user}")
        await user.timeout(datetime.timedelta(**parse_time(duration)), reason=reason)
        await interaction.response.send_message(
            f"{user.name} has been timed out for {duration} minutes. \nReason: {reason}"
        )

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx: commands.Context, user: discord.Member) -> None:
        logging.info(f"{ctx.author} has untimedout {user}")
        await user.timeout(None)
        await ctx.send(f"{user.name} has been unmuted.")

    # Hog told me to not include it yet. Dont uncomment.
    # @commands.command()
    # @commands.has_permissions(ban_members = True)
    # async def ban(self, ctx: commands.Context, user: discord.Member, duration: int, *, reason: str = "No reason provided.") -> None:
    #     await user.ban(reason=reason)
    #     await ctx.send(f"{user.name} has been banned.")

    # @commands.command()
    # @commands.has_permissions(ban_members = True)
    # async def unban(self, ctx: commands.Context, user: discord.Member):
    #     user = await bot.fetch_user(user.id)
    #     await ctx.guild.unban(user.id)
    #     await ctx.send(f"{user.name} has been unbanned.")

    # Needs proper implementation.
    # @commands.command()
    # @commands.has_permissions(ban_members = True)
    # async def tempban(self, ctx: commands.Context, user: discord.Member, duration: int, *, reason: str = "No reason provided.") -> None:
    #     await user.ban(reason=reason)
    #     await ctx.send(f"{user.name} has been banned for {duration} days. Reason: {reason}")


async def setup(bot: Hux) -> None:
    await bot.add_cog(Moderation(bot))
