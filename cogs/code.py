import discord
from discord.ext import commands
import subprocess

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["e"])
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, code: str = None) -> None:
        if code is None:
            await ctx.send("Correct usage: \n\`\`\`py \n<code here>\n\`\`\`")
        elif code.startswith("```py"):
            docker_sub = subprocess.run(["docker", "run", "--rm", "--memory='50m'", "--network none", "python:3.12-slim", "python", "-c", f"{code[6:-4]}"], capture_output=True, text=True)
            await ctx.send(f"Return code: {docker_sub.returncode}. \n Output: ```{docker_sub.stdout or docker_sub.stderr}```")
        else:
            await ctx.send("Please, use the proper formatting.")


async def setup(bot) -> None:
    await bot.add_cog(Eval(bot))