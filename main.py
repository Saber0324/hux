import logging
import os
import asyncio
import discord
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

from data.database import Database
from log_manager.logging_manager import setup_loggin

logger = logging.getLogger(__name__)

load_dotenv(Path(__file__).parent / ".env")

COGS = [
    "cogs.info",
    "cogs.moderation",
    "cogs.fun",
    "cogs.projects",
    "cogs.snippets",
    "cogs.warns",
    "cogs.testing",
    "cogs.code",
    "cogs.roles",
]


class Hux(commands.Bot):
    db: Database

    def __init__(self, prefix: str):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.typing = True
        intents.presences = True
        intents.guilds = True
        intents.moderation = True
        self.prefix = prefix

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.prefix), intents=intents
        )

    async def on_ready(self) -> None:
        logger.info(f"{self.user} is ready and online!")

    async def setup_hook(self) -> None:
        setup_loggin()
        self.db = Database("data/bot.db")
        await self.db.setup()

        for cog in COGS:
            await self.load_extension(cog)

        synced = await self.tree.sync()
        logger.info(f"Synced {len(synced)} commands.")

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        if interaction.command is not None:
            command_name = interaction.command.name
        else:
            command_name = "Unkown command name"

        logger.error(f"Error in app command {command_name}. {error}")

        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original

        match error:
            case app_commands.MissingPermissions():
                await interaction.response.send_message(
                    "You don't have permission to do this!"
                )
            case discord.Forbidden():
                await interaction.response.send_message(
                    "I don't have permission to do that."
                )
            case app_commands.CommandOnCooldown():
                await interaction.response.send_message(
                    f"The command {command_name} is still on cooldown."
                )
            case app_commands.NoPrivateMessage():
                await interaction.response.send_message(
                    f"The command {command_name} can only be used in a server"
                )
            case app_commands.CommandNotFound():
                await interaction.response.send_message(
                    f"The command {command_name} was not found."
                )

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if ctx.command is not None:
            command_name = ctx.command.name
        else:
            command_name = "Unkown command name"

        logger.error(f"Error in command {command_name}. {error}")

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        match error:
            case commands.CommandInvokeError():
                error = error.original
            case commands.MissingAnyRole():
                await ctx.send("You're missing a role required to access this command.")


async def main() -> None:
    token = os.getenv("TOKEN")
    if token is not None:
        async with Hux("!") as hux:
            await hux.start(token)
    else:
        logger.error("TOKEN not found.")


asyncio.run(main())
