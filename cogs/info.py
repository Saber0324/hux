import discord
from discord.ext import commands
from templates import embeds


class Info(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
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
        await ctx.send(
        embed = await embeds.userEmbed(user)
        )

    @info.command()
    async def server(self, ctx: commands.Context) -> None:
        await ctx.send(
        embed = await embeds.serverEmbed(ctx)
        )

    @info.group(invoke_without_command=True)
    async def role(self, ctx: commands.Context, target: discord.Role = None) -> None:
        if ctx.invoked_subcommand is None:
            if target:
                await ctx.send(
                embed = await embeds.roleEmbed(target)
                    )
            else:
                await ctx.send(
                    content="Correct usage: \n`!info role @role` \n`!info role list` \n`!info role count (group)`"
                )

    @role.command(name="list")
    async def role_list(self, ctx: commands.Context) -> None:
        await ctx.send(embed = await embeds.roleListEmbed(ctx))

    @role.command()
    async def count(self, ctx: commands.Context, *, group: str = None) -> None:
        pass


async def setup(bot) -> None:
    await bot.add_cog(Info(bot))
