import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING, cast

from hux.templates import embeds

if TYPE_CHECKING:
    from hux.main import Hux

logger = logging.getLogger(__name__)


class Roles(commands.Cog):
    role_group = app_commands.Group(
        name="role", description="provides information about roles."
    )

    def __init__(self, bot: Hux) -> None:
        self.bot = bot

    @role_group.command(
        name="info", description="Displays information about a given role."
    )
    @app_commands.describe(role="Role which information will be displayed.")
    async def role(self, interaction: discord.Interaction, role: discord.Role) -> None:
        logger.info(f"{interaction.user} requested information about role {role}")
        await interaction.response.send_message(embed=await embeds.roleEmbed(role))

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
        member = cast(discord.Member, interaction.user.id)
        if interaction.permissions.manage_roles and member.top_role > role:
            if role not in user.roles:
                await user.add_roles(role)
                logging.info(f"{interaction.user} has added role {role} to {user}")
                await interaction.response.send_message(
                    f"The role {role.mention} has been added to {user.mention}.",
                    allowed_mentions=discord.AllowedMentions.none(),
                )
            else:
                await interaction.response.send_message(
                    f"{user.mention} already has the role {role.mention}",
                    allowed_mentions=discord.AllowedMentions.none(),
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
            if role in user.roles:
                await user.remove_roles(role)
                logging.info(f"{interaction.user} has removed role {role} to {user}")
                await interaction.response.send_message(
                    f"The role {role.mention} has been removed from {user.mention}.",
                    allowed_mentions=discord.AllowedMentions.none(),
                )
            else:
                await interaction.response.send_message(
                    f"{user.mention} didn't have the role {role.mention}.",
                    allowed_mentions=discord.AllowedMentions.none(),
                )
        else:
            raise app_commands.MissingPermissions(["manage_roles"])


async def setup(bot: Hux) -> None:
    await bot.add_cog(Roles(bot))
