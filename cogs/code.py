import discord
from discord.ext import commands
import subprocess

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["e"])
    async def eval(self, ctx: commands.Context, *, code: str = None) -> None:
        if code is None:
            await ctx.send("Correct usage: \n\`\`\`py \n<code here>\n\`\`\`")
        elif code.startswith("```py"):
            docker_sub = subprocess.run(["docker", "run", "--rm", "python:3.12-slim", "python", "-c", f"{code[6:-4]}"], capture_output=True, text=True)
            await ctx.send(docker_sub.returncode)


async def setup(bot) -> None:
    await bot.add_cog(Eval(bot))