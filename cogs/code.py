import discord
from discord.ext import commands
import subprocess
import asyncio
import functools
import re

from typing import TYPE_CHECKING

from templates.view import BaseView, CorrectUsageMenu

if TYPE_CHECKING:
    from main import Hux


class Eval(commands.Cog):
    def __init__(self, bot: Hux):
        self.bot = bot

    async def eval_logic(self, code: str) -> tuple[str, int]:
        if code.startswith("```py"):
            loop = asyncio.get_event_loop()
            docker_sub = await loop.run_in_executor(
                None, functools.partial(run_python, code)
            )
        elif code.startswith("```go"):
            loop = asyncio.get_event_loop()
            docker_sub = await loop.run_in_executor(
                None, functools.partial(run_go, code)
            )
        else:
            return "Please, use proper formatting", 1

        output = docker_sub.stdout
        return_code = docker_sub.returncode

        if docker_sub.stderr:
            output += f"\nstderr: {docker_sub.stderr}"

        if len(output) >= 500:
            output = f"{output[:500]} \n\nOutput limited to 500 characters."

        else:
            output = output or "(No output)"

        return output, return_code

    def _format_output(self, output: str, return_code: int) -> str:
        if return_code == 0:
            return f"Your eval was succesful. \n```\n{output}\n```"
        return (
            f"Your eval returned with error code: {return_code}. \n```\n{output}\n```"
        )

    @commands.command(aliases=["e"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def eval(self, ctx: commands.Context, *, code: str | None = None) -> None:
        view = BaseView(ctx.author, timeout=30.0)
        delete_button = discord.ui.Button(
            label="Delete", style=discord.ButtonStyle.danger
        )

        async def delete_callback(interaction: discord.Interaction):
            await bot_message.delete()
            view._disable_all()

        delete_button.callback = delete_callback
        view.add_item(delete_button)

        if code is None:
            view = CorrectUsageMenu(ctx.author)
            view.message = await ctx.send(view=view)
            return

        output, return_code = await self.eval_logic(code)

        message = self._format_output(output=output, return_code=return_code)

        bot_message = await ctx.send(
            message,
            allowed_mentions=discord.AllowedMentions.none(),
            view=view,
        )
        view.message = bot_message

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> None:
        if before.content.startswith("!e"):
            await after.add_reaction("\U0001f501")

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, user: discord.User | discord.Member
    ) -> None:
        if user.bot:
            return
        if not (
            reaction.message.content.startswith("!e")
            and str(reaction.emoji) == "\U0001f501"
        ):
            return

        code = None
        match = re.match(r"^!(?:eval|e)\s+([\s\S]+)", reaction.message.content)
        if match is None:
            return

        code = match.group(1).strip()

        if code is None:
            return

        old_response = None
        async for msg in reaction.message.channel.history(limit=20):
            if msg.author == self.bot.user:
                old_response = msg
                break

        output, return_code = await self.eval_logic(code)

        if old_response:
            message = self._format_output(output=output, return_code=return_code)

            await old_response.edit(
                content=message, allowed_mentions=discord.AllowedMentions.none()
            )
        await reaction.message.clear_reactions()


def run_python(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "run",
            "--network",
            "none",
            "--rm",
            "--memory=100m",
            "--memory-swap=101m",
            "--cpus=2",
            "--security-opt",
            "no-new-privileges",
            "--read-only",
            "--tmpfs",
            "/tmp:size=50m,noexec",
            "--tmpfs",
            "/dev/shm:size=10m,noexec,nosuid",
            "--user",
            "1000:1000",
            "--pids-limit",
            "50",
            "--cap-drop",
            "all",
            "python:3.12-slim",
            "timeout",
            "15",
            "python",
            "-c",
            f"{code[6:-3]}",
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )


def run_go(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "run",
            "--network",
            "none",
            "--rm",
            "--memory=512m",
            "--memory-swap=513m",
            "--cpus=2",
            "--security-opt",
            "no-new-privileges",
            "--tmpfs",
            "/tmp:size=200m,exec",
            "--tmpfs",
            "/dev/shm:size=10m,noexec,nosuid",
            "--user",
            "1000:1000",
            "--pids-limit",
            "100",
            "--cap-drop",
            "all",
            "-e",
            "HOME=/tmp",
            "-e",
            "GOCACHE=/tmp/go-cache",
            "-e",
            "GOPATH=/tmp/gopath",
            "-i",
            "golang:alpine",
            "timeout",
            "45",
            "/bin/sh",
            "-c",
            "cat > /tmp/code.go && go run /tmp/code.go",
        ],
        input=code[6:-3],
        capture_output=True,
        text=True,
        timeout=50,
    )


async def setup(bot: Hux) -> None:
    await bot.add_cog(Eval(bot))
