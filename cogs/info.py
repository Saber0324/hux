import logging
import discord
from discord.ext import commands
from templates import embeds

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Hux

logger = logging.getLogger(__name__)


class Info(commands.Cog):
    def __init__(self, bot: Hux) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        logger.info(f"Ping command requested by {ctx.author} at {ctx.channel}")
        await ctx.send(
            content=f"Pong {round(number=self.bot.latency * 1000, ndigits=2)} ms!"
        )

    @commands.group()
    async def info(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Correct usage: \n`!info server` \n`!info user @user` \n`!info role (count/list/@role)`"
            )

    @info.command()
    async def user(self, ctx: commands.Context, user: discord.Member) -> None:
        logger.info(f"{ctx.author} requested information about {user}")
        await ctx.send(embed=await embeds.userEmbed(user))

    @info.command()
    async def server(self, ctx: commands.Context) -> None:
        logger.info(f"{ctx.author} requested server information.")
        await ctx.send(embed=await embeds.serverEmbed(ctx))

    @info.group(invoke_without_command=True)
    async def role(
        self, ctx: commands.Context, role: discord.Role | None = None
    ) -> None:
        if ctx.invoked_subcommand is None:
            if role:
                logging.info(f"{ctx.author} requested information about role {role}")
                await ctx.send(embed=await embeds.roleEmbed(role))
            else:
                await ctx.send(
                    content="Correct usage: \n`!info role @role` \n`!info role list` \n`!info role count (group)`"
                )

    @role.command(name="list")
    async def role_list(self, ctx: commands.Context) -> None:
        logging.info(f"{ctx.author} requested list of roles")
        await ctx.send(embed=await embeds.roleListEmbed(ctx))

    @role.command()
    async def count(self, ctx: commands.Context, *, group: str | None = None) -> None:
        pass


async def setup(bot: Hux) -> None:
    await bot.add_cog(Info(bot))
