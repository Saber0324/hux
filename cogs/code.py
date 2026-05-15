import discord
from discord.ext import commands
import subprocess
import asyncio
import functools


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["e"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def eval(self, ctx: commands.Context, *, code: str | None = None) -> None:
        if code is None:
            await ctx.send(
                "Correct usage: \n\n"
                + r"\`\`\`py/go"
                + "\n"
                + "<code here>"
                + "\n"
                + r"\`\`\`"
            )
            return
        elif code.startswith("```py"):
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
            await ctx.send("Please, use the proper formatting.")
            return

        output = docker_sub.stdout
        if docker_sub.stderr:
            output += f"\nstderr: {docker_sub.stderr}"
        if len(output) >= 500:
            output = f"{output[:500]} \n\nOutput limited to 500 characters."
        else:
            output = output or "(No output)"
        await ctx.send(
            f"Your code returned with code: {docker_sub.returncode}. ```{output}```",
            allowed_mentions=discord.AllowedMentions.none(),
        )


def run_python(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "run",
            "--network",
            "none",
            "--rm",
            "--memory=50m",
            "--memory-swap=50m",
            "--cpus=0.5",
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
            "--memory=300m",
            "--memory-swap=301m",
            "--cpus=1",
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
            "30",
            "/bin/sh",
            "-c",
            "cat > /tmp/code.go && go run /tmp/code.go",
        ],
        input=code[6:-3],
        capture_output=True,
        text=True,
        timeout=35,
    )


async def setup(bot) -> None:
    await bot.add_cog(Eval(bot))
