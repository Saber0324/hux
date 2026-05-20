from asyncio import timeout
import discord
from discord import app_commands
from discord.ext import commands

from typing import TYPE_CHECKING

from templates.base_view import BaseView

if TYPE_CHECKING:
    from main import Hux


class Testing(commands.Cog):
    def __init__(self, bot: Hux):
        self.bot = bot

    @app_commands.command(name="test", description="Doing funny stuff.")
    @app_commands.describe(text="What the bot will say is a slash command")
    async def test(self, interaction: discord.Interaction, text: str = "This"):
        await interaction.response.send_message(f"{text} is a slash command!")

    @app_commands.command(name="viewtest", description="View testing.")
    async def viewtest(self, interaction: discord.Interaction) -> None:
        view = BaseView(interaction.user, timeout=10.0)
        view.add_item(
            discord.ui.Button(label="Testing", style=discord.ButtonStyle.blurple)
        )
        await interaction.response.send_message(
            "This is supposed to be a view!", view=view
        )
        view.message = await interaction.original_response()

    @app_commands.command(
        name="viewerror", description="Testing error display on the BaseView"
    )
    async def viewerror(self, interaction: discord.Interaction) -> None:
        view = BaseView(interaction.user, timeout=10.0)
        view.add_item(
            discord.ui.Button(label="Error me out!", style=discord.ButtonStyle.blurple)
        )

        async def callback(interaction: discord.Interaction):
            raise Exception(f"{interaction.user} errored me out, what a twat.")

        view.children[0].callback = callback
        await interaction.response.send_message("Click me for an error.", view=view)


async def setup(bot: Hux):
    await bot.add_cog(Testing(bot))

