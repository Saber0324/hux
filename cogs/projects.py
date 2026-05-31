import os
import discord


from typing import TYPE_CHECKING
from pathlib import Path
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from aiohttp import ClientSession

from templates.embeds import github_repo_embed, github_user_embed

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
        name="repo", description="Search for a specified github repository"
    )
    async def repo_search(
        self,
        interaction: discord.Interaction,
        repository: str,
        user: str | None = None,
    ) -> None:
        searched_repo = Request(user, repository)
        data = await searched_repo.get_data()
        if data != "Not found":
            if repository is not None:
                if data is not None:
                    embed = github_repo_embed(data)
                    await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "The searched repository was not found."
            )


class Request:
    def __init__(self, user: str | None = None, repo: str | None = None) -> None:
        self.user = user
        self.repo = repo
        self.headers = {"Authorization": str(os.getenv("github_token"))}

    def get_url(self) -> str | None:
        if not self.repo:
            print("Repository must be speficied.")
            return
        elif self.user and self.repo:
            url = f"https://api.github.com/repos/{self.user}/{self.repo}"
            return url
        elif self.repo:
            url = f"https://api.github.com/search/repositories?q={self.repo}&sort=stars&order=desc"
            return url
        elif self.user:
            url = f"https://api.github.com/users/{self.user}"
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
                    repo["id"]: {
                        "name": repo["name"],
                        "license_name": (repo["license"] or {}).get(
                            "name", "no license"
                        ),
                        "url": repo["html_url"],
                        "description": repo["description"] or "No description",
                        "created_at": repo["created_at"],
                        "owner_avatar": repo["owner"]["avatar_url"],
                    }
                    for repo in data["items"][0]
                }
            elif "bio" in data:
                return {
                    "login": data["login"],
                    "url": data["html_url"],
                    "bio": data["bio"] or "No bio",
                    "avatar": data["avatar_url"],
                    "repos": data["public_repos"],
                }
            else:
                return {
                    "name": data["name"],
                    "license_name": (data["license"] or {}).get("name", "no license"),
                    "url": data["html_url"],
                    "description": data["description"],
                    "created_at": data["created_at"],
                    "owner_avatar": data["owner"]["avatar_url"],
                }
        else:
            return "Not found"


async def setup(bot: Hux) -> None:
    await bot.add_cog(Projects(bot))
