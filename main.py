import discord
from discord import app_commands
from discord.ext import commands
import logging
import os
import asyncio
import subprocess
from dotenv import load_dotenv
from data.database import Database

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
intents.presences = True
intents.guilds = True
intents.moderation = True

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
token = str(os.getenv("TOKEN"))

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is ready and online!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)


@bot.event
async def on_command_error(ctx: commands.Context, error) -> None:
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do this!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: `{error.param.name}`")
    elif isinstance(error, discord.Forbidden):
        await ctx.send("I don't have permission to do that.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Command has a bad argument. Check all parameter are correct.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("Only Saber can access this command.")
    elif isinstance(error, subprocess.TimeoutExpired):
        await ctx.send("Subprocess timed out.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send("The command is still in cooldown.")
    elif isinstance(error, commands.CommandNotFound):
        pass


async def main() -> None:
    discord.utils.setup_logging(handler=handler, level=logging.DEBUG)
    async with bot:
        bot.db = Database("data/bot.db")
        await bot.db.setup()
        for cogs in [
            "cogs.info",
            "cogs.moderation",
            "cogs.fun",
            "cogs.projects",
            "cogs.snippets",
            "cogs.warns",
            "cogs.testing",
            # "cogs.code",
        ]:
            await bot.load_extension(cogs)
        await bot.start(token)


asyncio.run(main())
