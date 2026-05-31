import os
import json
import discord


from typing import TYPE_CHECKING
from pathlib import Path
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from aiohttp import ClientSession

from templates.embeds import github_repo_embed

if TYPE_CHECKING:
    from main import Hux

load_dotenv(Path(__file__).parent.parent / ".env")


class Projects(commands.Cog):
    gh_group = app_commands.Group(
        name="github",
        description="Commands that search github users or repositories.",
    )

    def __init__(self, bot: Hux):
        self.bot = bot

    @gh_group.command(
        name="search", description="Search for a specified github user or repository"
    )
    async def search(
        self, interaction: discord.Interaction, user: str, repository: str | None = None
    ) -> None:
        searched_item = Request(user, repository)
        data = await searched_item.get_data()
        if repository is not None:
            if data is not None:
                embed = github_repo_embed(data)
                await interaction.response.send_message(embed=embed)
        else:
            if data is not None:
                await interaction.response.send_message(
                    f"```json\n{json.dumps(data, indent=4)}\n```"
                )


class Request:
    def __init__(self, user: str, repo: str | None = None) -> None:
        self.user = user
        self.repo = repo
        self.headers = {"Authorization": str(os.getenv("github_token"))}

    def get_url(self) -> str | None:
        if not self.user:
            print("User must be specified.")
            return
        elif self.user and self.repo:
            url = f"https://api.github.com/repos/{self.user}/{self.repo}"
            return url
        elif self.user:
            url = f"https://api.github.com/search/repositories?q=user:{self.user}"
            return url

    async def get_response(self, url):
        try:
            async with ClientSession() as session:
                response = await session.get(url=url, headers=self.headers)
                data = response.json()
                return await data
        except Exception:
            print("Missing url.")
            return

    async def get_data(self):
        data = await self.get_response(self.get_url())
        if data is not None and "message" not in data:
            if "items" in data:
                return {
                    repo["name"]: {
                        "created_at": repo["created_at"],
                        "license_name": (repo["license"] or {}).get(
                            "name", "No license"
                        ),
                        "url": repo["html_url"],
                        "description": repo["description"] or "No description",
                    }
                    for repo in data["items"]
                }
            else:
                return {
                    "name": data["name"],
                    "license_name": data["license"]["name"],
                    "url": data["url"],
                    "description": data["description"],
                    "created_at": data["created_at"],
                }


async def setup(bot: Hux) -> None:
    await bot.add_cog(Projects(bot))
