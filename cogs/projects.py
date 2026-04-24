from discord.ext import commands


class Projects(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Example data (you can expand this)
        self.projects = {
            "lufus": {
                "repo": "<https://github.com/Hog185/Lufus>",
                "release": "<https://github.com/Hog185/Lufus/releases/latest>",
            },
            "hux-bot": {
                "repo": "<https://github.com/Saber0324/projects-bot>",
                "release": "<https://github.com/Saber0324/projects-bot/releases/latest>",
            },
        }

    # base command: !projects
    @commands.group(invoke_without_command=True)
    async def projects(self, ctx: commands.Context) -> None:
        await ctx.send("Use `!projects help` to see available commands.")

    # !projects help/h
    @projects.command(aliases=["h"])
    async def help(self, ctx: commands.Context) -> None:
        await ctx.send(
            "**Projects Commands:**\n"
            "`!projects list` → list all projects\n"
            "`!projects release <name>` → get latest release\n"
            "`!projects help` → show this message"
        )

    # !projects list/l
    @projects.command(aliases=["l"])
    async def list(self, ctx: commands.Context) -> None:
        msg = "**Current Projects:**\n"
        for name, data in self.projects.items():
            msg += f"- **{name}** → {data['repo']}\n"

        await ctx.send(msg)

    # !projects release <project_name>
    @projects.command(aliases=["rel"])
    async def release(self, ctx: commands.Context, project_name: str) -> None:
        project_name = project_name.lower()
        if project_name not in self.projects:
            await ctx.send("Project not found.")
            return
        link = self.projects[project_name]["release"]
        await ctx.send(f"Latest release for **{project_name}**:\n{link}")


async def setup(bot):
    await bot.add_cog(Projects(bot))
