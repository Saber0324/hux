from datetime import datetime, timezone
import logging
import discord
from discord.ext import commands
from discord import app_commands
from templates.models import Warn

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Hux


class Warns(commands.Cog):
    warn_group = app_commands.Group(
        name="warn", description="Commands used to manage warns."
    )

    def __init__(self, bot: Hux):
        self.bot = bot

    @warn_group.command(name="give", description="Warns an user.")
    @app_commands.describe(user="User to be warned.", reason="Reason for the warn.")
    async def warn(
        self,
        interaction: discord.Interaction,
        user: discord.Member | None = None,
        *,
        reason: str | None = None,
    ) -> None:
        current_date = datetime.now(timezone.utc).strftime("%y-%m-%d")
        moderator = interaction.user
        if user:
            if interaction.permissions.moderate_members:
                logging.info(f"{interaction.user} has warned {user} for {reason}")
                await self.bot.db.insert(
                    "warns", (user.id, reason, moderator.id, current_date, None)
                )
                embed = discord.Embed(title="_*Warning*_", color=discord.Color.red())
                embed.set_thumbnail(
                    url="https://raw.githubusercontent.com/Saber0324/projects-bot/main/assets/warn.png?v=2"
                )
                embed.add_field(name="Reason", value=reason, inline=True)
                embed.set_footer(text=f"Warned by {moderator.name} at {current_date}")
                await interaction.response.send_message(embed=embed)
                return
            else:
                raise app_commands.MissingPermissions(["moderate_members"])

    @warn_group.command(
        name="list", description="Displays a list of all warns given to an user."
    )
    @app_commands.describe(user="User to display warns from.")
    async def warn_list(
        self, interaction: discord.Interaction, user: discord.Member
    ) -> None:
        warning_list = await self.bot.db.get_all_where("warns", "user_id", user.id)
        if not warning_list:
            await interaction.response.send_message(
                f"{user.name} doesn't have any warns. "
            )
            return
        message = ""
        for warning in warning_list:
            warn = Warn(*warning)
            message += f"_*Warn ID: {warn.warn_id}.*_ \n_*{warn.reason}*_ \nat {warn.date} \nBy {await self.bot.fetch_user(warn.moderator_id)}\n\n"
        embed = discord.Embed(title="Warning List", color=discord.Color.red())
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="User", value=user.display_name, inline=False)
        embed.add_field(name="Warnings", value=message, inline=False)
        await interaction.response.send_message(embed=embed)

    @warn_group.command(description="Deletes a warn by its id.")
    @app_commands.describe(warn_id="ID of the warn to be deleted.")
    async def delete(self, interaction: discord.Interaction, warn_id: int) -> None:
        result = await self.bot.db.get_one("warns", "warn_id", warn_id)
        if result is not None:
            if interaction.permissions.moderate_members:
                warn = Warn(*result)
                await self.bot.db.delete("warns", "warn_id", warn_id)
                logging.info(f"{interaction.user} has deleted warn id {warn.warn_id}")
                await interaction.response.send_message(
                    f"Warning ID:{warn.warn_id} for {warn.reason} deleted from {await self.bot.fetch_user(warn.user_id)}"
                )
            else:
                raise app_commands.MissingPermissions(["moderate_members"])
        else:
            await interaction.response.send_message("This warning does not exist. ")
            return


async def setup(bot: Hux) -> None:
    await bot.add_cog(Warns(bot))
