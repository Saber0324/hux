import random
import discord
from discord.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Hux


class Fun(commands.Cog):
    def __init__(self, bot: Hux) -> None:
        self.bot = bot

    @commands.hybrid_group(name="fun", fallback="get")
    async def fun(self, ctx: commands.Context) -> None:
        await ctx.send(f"{ctx.author} is " + random.choice(["fun.", "not fun."]))

    @fun.command()
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.send("Hello, sunshine.")

    @fun.command()
    async def meow(self, ctx: commands.Context) -> None:
        await ctx.send("Meow too!")

    @fun.command()
    async def fuck_off_iva(self, ctx: commands.Context) -> None:
        await ctx.send("FUCK OFF IVA")

    @fun.command()
    async def hog(self, ctx: commands.Context) -> None:
        await ctx.send("All hail the supreme leader")

    @fun.command()
    @commands.has_role(1508140013345575133)
    async def say(self, ctx: commands.Context, *, arg: str) -> None:
        await ctx.send(arg, allowed_mentions=discord.AllowedMentions.none())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if self.bot.user in message.mentions:
            content = message.content.lower()

            if "is this true?" in content:
                text_responses = [
                    "Yes",
                    "No",
                    "Maybe",
                    "Ask Hog",
                    "Of course",
                    "I dont know",
                    "Probably",
                ]
                gif_responses = ["https://tenor.com/bU4oZ.gif"]

                if random.random() < 0.5:
                    await message.reply(random.choice(text_responses))
                else:
                    await message.reply(random.choice(gif_responses))


async def setup(bot: Hux) -> None:
    await bot.add_cog(Fun(bot))
