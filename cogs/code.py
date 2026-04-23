import discord
from discord.ext import commands
import subprocess


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["e"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def eval(self, ctx: commands.Context, *, code: str = None) -> None:
        if code is None:
            await ctx.send("Correct usage: \n\`\`\`py \n<code here>\n\`\`\`")
        elif code.startswith("```py"):
            docker_sub = subprocess.run(
                [
                    "docker", "run",
                    "--network" , "none",
                    "--rm",
                    "--memory=50m",
                    "--memory-swap=50m",
                    "--cpus=0.5",
                    "--security-opt", "no-new-privileges",
                    "--read-only",
                    "--tmpfs", "/tmp:size=5m",
                    "--user", "1000:1000",
                    "python:3.12-slim",
                    "python",
                    "-c",
                    f"{code[6:-3]}",
                ],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = docker_sub.stdout or docker_sub.stderr
            await ctx.send(
                f"Return code: {docker_sub.returncode}. \n Output: ```{output[:1900]}```"
            )
        else:
            await ctx.send("Please, use the proper formatting.")


async def setup(bot) -> None:
    await bot.add_cog(Eval(bot))
