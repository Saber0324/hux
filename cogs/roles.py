import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING

from templates import embeds

if TYPE_CHECKING:
    from main import Hux

logger = logging.getLogger(__name__)


class Roles(commands.Cog):
    role_group = app_commands.Group(
        name="role", description="provides information about roles."
    )

    def __init__(self, bot: Hux) -> None:
        self.bot = bot

    @role_group.command(
        name="role", description="Displays information about a given role."
    )
    @app_commands.describe(role="Role which information will be displayed.")
    async def role(
        self, interaction: discord.Interaction, role: discord.Role | None = None
    ) -> None:
        if role is not None:
            logger.info(f"{interaction.user} requested information about role {role}")
            await interaction.response.send_message(embed=await embeds.roleEmbed(role))
        else:
            await interaction.response.send_message("Role not found.")

    @role_group.command(
        name="list", description="Shows a list all of the server's roles."
    )
    async def role_list(self, interaction: discord.Interaction) -> None:
        logger.info(f"{interaction.user} requested list of roles")
        await interaction.response.send_message(
            embed=await embeds.roleListEmbed(interaction)
        )

    @role_group.command(description="Adds a role to an user.")
    @app_commands.describe(
        user="User that will get a role added.", role="Role that will be added to user."
    )
    async def add(
        self, interaction: discord.Interaction, user: discord.Member, role: discord.Role
    ) -> None:
        if interaction.permissions.manage_roles:
            logging.info(f"{interaction.user} has added role {role} to {user}")
            await user.add_roles(role)
            await interaction.response.send_message(
                f"The role {role.name} has been added to {user.name}."
            )
        else:
            raise app_commands.MissingPermissions(["manage_roles"])

    @role_group.command(description="Removes a role from an user.")
    @app_commands.describe(
        user="User that will get a role removed.",
        role="Role that will be removed from user.",
    )
    async def remove(
        self, interaction: discord.Interaction, user: discord.Member, role: discord.Role
    ) -> None:
        if interaction.permissions.manage_roles:
            logging.info(f"{interaction.user} has removed role {role} to {user}")
            await user.remove_roles(role)
            await interaction.response.send_message(
                f"The role {role.name} has been removed from {user.name}."
            )
        else:
            raise app_commands.MissingPermissions(["manage_roles"])


async def setup(bot: Hux) -> None:
    await bot.add_cog(Roles(bot))
