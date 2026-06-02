import logging
import discord
from discord.ext import commands
from discord import app_commands
from templates import embeds

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Hux

logger = logging.getLogger(__name__)


class Info(commands.Cog):
    info_group = app_commands.Group(
        name="info", description="Displays various types of information."
    )

    def __init__(self, bot: Hux) -> None:
        self.bot = bot

    @info_group.command(name="ping", description="Shows the bot's latency.")
    async def ping(self, interaction: discord.Interaction) -> None:
        logger.info(
            f"Ping command requested by {interaction.user} at {interaction.channel}"
        )
        await interaction.response.send_message(
            content=f"Pong {round(number=self.bot.latency * 1000, ndigits=2)} ms!"
        )

    @info_group.command()
    async def user(
        self, interaction: discord.Interaction, user: discord.Member
    ) -> None:
        logger.info(f"{interaction.user} requested information about {user}")
        await interaction.response.send_message(embed=await embeds.userEmbed(user))

    @info_group.command()
    async def server(self, interaction: discord.Interaction) -> None:
        logger.info(f"{interaction.user} requested server information.")
        await interaction.response.send_message(
            embed=await embeds.serverEmbed(interaction)
        )


async def setup(bot: Hux) -> None:
    await bot.add_cog(Info(bot))
