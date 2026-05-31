import logging
import os
from pathlib import Path
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import discord

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

    async def on_command_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        if interaction.command is not None:
            command_name = interaction.command.name
        else:
            command_name = "Unkown command name"

        logging.error(f"Error in command: {command_name}. {error}")

        match error:
            case commands.CommandInvokeError():
                error = error.original
            case commands.MissingPermissions():
                await interaction.response.send_message(
                    "You don't have permission to do this!"
                )
            case commands.MemberNotFound():
                await interaction.response.send_message("User not found.")
            case commands.MissingRequiredArgument():
                await interaction.response.send_message(
                    f"Missing argument: `{error.param.name}`."
                )
            case discord.Forbidden():
                await interaction.response.send_message(
                    "I don't have permission to do that."
                )
            case commands.BadArgument():
                await interaction.response.send_message(
                    f"The command {command_name} has a bad argument. Check correct usage."
                )
            case commands.NotOwner():
                await interaction.response.send_message(
                    "Only the bot owner can access this command."
                )
            case commands.CommandOnCooldown():
                await interaction.response.send_message(f"The command {command_name}")
            case commands.NoPrivateMessage():
                await interaction.response.send_message(
                    f"The command {command_name} can only be used in a server"
                )
            case commands.CommandNotFound():
                pass


async def main() -> None:
    token = os.getenv("TOKEN")
    if token is not None:
        async with Hux("!") as hux:
            await hux.start(token)
    else:
        logger.error("TOKEN not found.")


asyncio.run(main())
