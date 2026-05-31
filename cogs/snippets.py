import discord
from discord.ext import commands
from discord import app_commands
from templates.models import Snippet

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Hux


class Snippets(commands.Cog):
    snippets_group = app_commands.Group(
        name="snippets", description="Commands use to interact with snippets."
    )

    def __init__(self, bot: Hux):
        self.bot = bot

    async def get_snippet(
        self, interaction: discord.Interaction, title: str, silent: bool = False
    ) -> Snippet | None:
        result = await self.bot.db.get_one("snippets", "title", title)
        if result is None:
            if not silent:
                await interaction.response.send_message("Snippet not found. ")
                return
        else:
            snippet = Snippet(*result)
            return snippet

    def message_list_builder(self, results: list) -> str:
        message = ""
        for result in results:
            snippet = Snippet(*result)
            if snippet.locked:
                message += f"— {snippet.title} :lock: \n\n"
            else:
                message += f"— {snippet.title} \n\n"
        return message

    @snippets_group.command(description="Sends a snippet to the chat.")
    @app_commands.describe(title="Title of the snippet to be displayed.")
    async def display(
        self, interaction: discord.Interaction, title: str | None = None
    ) -> None:
        if title is not None:
            snippet = await self.get_snippet(interaction, title)
            if snippet is not None:
                message = f"""***`{snippet.title} ->`{":lock:" if snippet.locked else ""}*** \n{snippet.description}
                \n-# — Written by {await self.bot.fetch_user(snippet.author_id)}
                """
            else:
                message = "Snipet not found."
            await interaction.response.send_message(message)

    @snippets_group.command(description="Adds a snippet to Hux.")
    @app_commands.describe(
        title="Title of the snippet to be created.",
        description="Content of the snippet to be created.",
        locked="Status of the snippet to be created",
    )
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
        *,
        description: str,
        locked: int = 0,
    ) -> None:
        author = interaction.user.id
        snippet = await self.get_snippet(interaction, title, silent=True)
        if snippet is not None:
            await interaction.response.send_message("This snippet already exists! ")
        else:
            await self.bot.db.insert("snippets", (title, description, author, locked))
            await interaction.response.send_message(f"Snippet {title} created! ")

    @snippets_group.command(description="Edits a snippet.")
    @app_commands.describe(
        title="Title of the snippet to be edited.",
        description="New content of the snippet.",
    )
    async def edit(
        self, interaction: discord.Interaction, title: str, *, description: str
    ) -> None:
        snippet = await self.get_snippet(interaction, title)
        if snippet is not None:
            if snippet.locked:
                await interaction.response.send_message(
                    "This snippet is closed. Ask a moderator to unlock if you want to edit it. "
                )
            elif snippet.author_id == interaction.user.id:
                await self.bot.db.update(
                    "snippets", "description", description, "title", title
                )
                await interaction.response.send_message(
                    f"Snippet {title} updated succesfully."
                )
            else:
                await interaction.response.send_message(
                    "This snippet is not yours. Ask the author if you want to edit it."
                )
        else:
            await interaction.response.send_message("Snippet not found.")

    @snippets_group.command(description="Deletes a snippet.")
    @app_commands.describe(title="Title of the snippet to be deleted.")
    async def delete(self, interaction: discord.Interaction, title: str) -> None:
        snippet = await self.get_snippet(interaction, title)
        if snippet is not None:
            if snippet.locked:
                await interaction.response.send_message(
                    "This snippet is locked. Ask the author or a moderator to unlock it. "
                )
            elif (
                snippet.author_id == interaction.user.id
                or interaction.permissions.manage_messages
            ):
                await self.bot.db.delete("snippets", "title", title)
                await interaction.response.send_message(
                    f"Snippet {title} deleted succesfully. "
                )
            else:
                await interaction.response.send_message(
                    f"You're not the author of {title} and don't have permission to do this. "
                )
        else:
            await interaction.response.send_message("Snippet not found.")

    @snippets_group.command(
        description="Locks a snippet so it can't be edited or deleted."
    )
    @app_commands.describe(title="Title of the snippet to be locked.")
    async def lock(self, interaction: discord.Interaction, title: str) -> None:
        snippet = await self.get_snippet(interaction, title)
        if snippet is not None:
            if (
                snippet.author_id != interaction.user.id
                and not interaction.permissions.manage_messages
            ):
                await interaction.response.send_message(
                    f"You're not the author of {title} and don't have permission to do this. "
                )
            elif snippet.locked:
                await interaction.response.send_message(
                    "This snippet is already locked. "
                )
            else:
                await self.bot.db.update("snippets", "locked", True, "title", title)
                await interaction.response.send_message(
                    f"Snippet {title} has been locked. "
                )
        else:
            await interaction.response.send_message("Snippet not found.")

    @snippets_group.command(
        description="Unlocks a snippet so it can be edited or deleted."
    )
    @app_commands.describe(title="Title of the snippet to be unlocked.")
    async def unlock(self, interaction: discord.Interaction, title: str) -> None:
        snippet = await self.get_snippet(interaction, title)
        if snippet is not None:
            if (
                snippet.author_id != interaction.user.id
                and not interaction.permissions.manage_messages
            ):
                await interaction.response.send_message(
                    f"You're not the author of {title} and don't have permission to do this. "
                )
            elif not snippet.locked:
                await interaction.response.send_message(
                    "This snippet is already unlocked. "
                )
            else:
                await self.bot.db.update("snippets", "locked", False, "title", title)
                await interaction.response.send_message(
                    f"Snippet {title} has been unlocked. "
                )
        else:
            await interaction.response.send_message("Snippet not found.")

    @snippets_group.command(name="list", description="Sends a list of all snippets.")
    async def snippet_list(self, interaction: discord.Interaction) -> None:
        result_list = await self.bot.db.get_all("snippets")
        message = self.message_list_builder(result_list)
        await interaction.response.send_message(message)

    # @snippets_group.command()
    # @commands.has_permissions(moderate_members=True)
    # async def ban(self, interaction: discord.Interaction, user: discord.Member) -> None:
    #     pass

    # @snippets_group.command(aliases=["ub"])
    # @commands.has_permissions(moderate_members=True)
    # async def unban(
    #     self, interaction: discord.Interaction, user: discord.Member
    # ) -> None:
    #     pass

    @snippets_group.command(description="Sends a list of all snippets made by an user.")
    @app_commands.describe(user="User whose snippets will be listed.")
    async def author(
        self, interaction: discord.Interaction, user: discord.Member
    ) -> None:
        group_result = await self.bot.db.get_all_where("snippets", "author_id", user.id)
        if group_result == []:
            message = "This user hasn't made any snippets. "
        else:
            message = self.message_list_builder(group_result)
        await interaction.response.send_message(message)


async def setup(bot: Hux) -> None:
    await bot.add_cog(Snippets(bot))
