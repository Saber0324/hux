import logging
import os
import asyncio
import subprocess
import discord
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

from data.database import Database
from log_manager.logging_manager import setup_loggin

logger = logging.getLogger(__name__)

load_dotenv(Path(__file__).parent.parent / ".env")

COGS = [
    "cogs.info",
    "cogs.fun",
    "cogs.projects",
    "cogs.snippets",
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
        self.tree.on_error = self.on_app_command_error
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
            command_name = "Unknown command name"

        logger.error(
            f"Error in app command {command_name} invoked by {interaction.user}. {error}"
        )

        async def send(msg: str):
            if interaction.response.is_done():
                await interaction.followup.send(msg)
            else:
                await interaction.response.send_message(msg)

        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original

        match error:
            case app_commands.MissingPermissions():
                await send("You don't have permission to do this!")
            case discord.Forbidden():
                await send("I don't have permission to do that.")
            case app_commands.CommandOnCooldown():
                await send(f"The command {command_name} is still on cooldown.")
            case app_commands.NoPrivateMessage():
                await send(f"The command {command_name} can only be used in a server")
            case app_commands.CommandNotFound():
                await send(f"The command {command_name} was not found.")

            case _:
                await send("An unexpected error occurred")
                logger.error(f"Unhandled exception: {error}")

    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if ctx.command is not None:
            command_name = ctx.command.name
        else:
            command_name = "Unknown command name"

        logger.error(
            f"Error in command {command_name} invoked by user {ctx.author}. {error}"
        )

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        match error:
            case commands.MissingAnyRole() | commands.MissingRole():
                await ctx.send("You're missing a role required to access this command.")
            case commands.CommandNotFound():
                pass
            case subprocess.TimeoutExpired():
                await ctx.send("The command took too long to execute.")
            case commands.CommandOnCooldown():
                await ctx.send("The command is still in cooldown.")
            case _:
                await ctx.send("An unexpected error ocurred")
                logger.error(f"Unhandled exception: {error}")


async def main() -> None:
    token = os.getenv("TOKEN")
    if token is not None:
        async with Hux("!") as hux:
            await hux.start(token)
    else:
        logger.error("TOKEN not found.")


asyncio.run(main())
