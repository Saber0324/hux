from datetime import datetime
import discord
from discord.ext import commands
from templates.models import Warn


class Warns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["w"])
    @commands.has_permissions(moderate_members=True)
    async def warn(
        self, ctx, user: discord.Member = None, *, reason: str = None
    ) -> None:
        current_date = datetime.utcnow().strftime("%y-%m-%d")
        moderator = ctx.author
        if ctx.invoked_subcommand is None and user is None:
            await ctx.send("`!help warn` for more information. ")
            return
        elif user:
            await self.bot.db.insert(
                "warns", (user.id, reason, moderator.id, current_date, None)
            )
            embed = discord.Embed(title="_*Warning*_", color=discord.Color.red())
            embed.set_thumbnail(
                url="https://raw.githubusercontent.com/Saber0324/projects-bot/main/assets/warn.png?v=2"
            )
            embed.add_field(name="Reason", value=reason, inline=True)
            embed.set_footer(text=f"Warned by {moderator.name} at {current_date}")
            await ctx.send(embed=embed)
            return

    @warn.command(name="list", aliases=["l"])
    async def warn_list(self, ctx: commands.Context, user: discord.Member) -> None:
        warning_list = await self.bot.db.get_all_where(
            "warns", "user_id", user.id
        )  # Gets list of all warns filtered by user.
        if not warning_list:
            await ctx.send(f"{user.name} doesn't have any warns. ")
            return
        message = ""
        for warning in warning_list:
            warn = Warn(
                *warning
            )  # Turns warn list into class instances for better readability
            message += f"_*Warn ID: {warn.warn_id}.*_ \n_*{warn.reason}*_ \nat {warn.date} \nBy {await self.bot.fetch_user(warn.moderator_id)}\n\n"
        embed = discord.Embed(title="Warning List", color=discord.Color.red())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="User", value=user.display_name, inline=False)
        embed.add_field(name="Warnings", value=message, inline=False)
        await ctx.send(embed=embed)

    @warn.command(aliases=["d"])
    @commands.has_permissions(moderate_members=True)
    async def delete(self, ctx: commands.Context, warn_id: int) -> None:
        result = await self.bot.db.get_one("warns", "warn_id", warn_id)
        if result is None:
            await ctx.send("This warning does not exist. ")
            return
        warn = Warn(*result)
        await self.bot.db.delete("warns", "warn_id", warn_id)
        await ctx.send(
            f"Warning ID:{warn.warn_id} for {warn.reason} deleted from {await self.bot.fetch_user(warn.user_id)}"
        )


async def setup(bot) -> None:
    await bot.add_cog(Warns(bot))
