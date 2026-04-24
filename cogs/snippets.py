import discord
from discord.ext import commands
from templates.models import Snippet


class Snippets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_snippet(
        self, ctx: commands.Context, title: str, silent: bool = False
    ) -> Snippet | None:
        result = await self.bot.db.get_one("snippets", "title", title)
        if result is None:
            if not silent:  # Add doesn't need to check existence.
                await ctx.send("Snippet not found. ")
                return
        else:
            snippet = Snippet(
                *result
            )  # Turns result into snippet.title/.description/.author/.lock
            return snippet

    def message_list_builder(
        self, results: list
    ) -> str:  # Doesn't use ctx because it doesn't take input directly from discord.
        message = ""
        for result in results:
            snippet = Snippet(*result)
            if snippet.locked:
                message += f"— {snippet.title} :lock: \n\n"  # Adds every title to the message. Planned to turn into a paginating embed later (fuck discord.py docs)
            else:
                message += f"— {snippet.title} \n\n"
        return message

    @commands.group(invoke_without_command=True, aliases=["s"])
    async def snippet(self, ctx: commands.Context, title: str = None) -> None:
        if ctx.invoked_subcommand is None and title is None:
            await ctx.send("`!help snippet` for more information. ")
        elif title is not None:
            snippet = await self.get_snippet(ctx, title)
            message = f"""***`{snippet.title} ->`{":lock:" if snippet.locked else ""}*** \n{snippet.description}
            \n-# — Written by {await self.bot.fetch_user(snippet.author_id)}
            """
            await ctx.send(message)

    @snippet.command(aliases=["a"])
    async def add(
        self, ctx: commands.Context, title: str, *, description: str, locked: int = 0
    ) -> None:
        author = ctx.author.id
        snippet = await self.get_snippet(ctx, title, silent=True)
        if snippet is not None:
            await ctx.send("This snippet already exists! ")
        else:
            await self.bot.db.insert("snippets", (title, description, author, locked))
            await ctx.send(f"Snippet {title} created! ")

    @snippet.command(aliases=["e"])
    async def edit(
        self, ctx: commands.Context, title: str, *, description: str
    ) -> None:
        snippet = await self.get_snippet(ctx, title)
        if snippet.locked:
            await ctx.send(
                "This snippet is closed. Ask a moderator to unlock if you want to edit it. "
            )
        elif snippet.author_id == ctx.author.id:
            await self.bot.db.update(
                "snippets", "description", description, "title", title
            )
            await ctx.send(f"Snippet {title} updated succesfully.")
        else:
            await ctx.send(
                "This snippet is not yours. Ask the author if you want to edit it."
            )

    @snippet.command(aliases=["d"])
    async def delete(self, ctx: commands.Context, title: str) -> None:
        snippet = await self.get_snippet(ctx, title)
        if snippet.locked:
            await ctx.send(
                "This snippet is locked. Ask the author or a moderator to unlock it. "
            )
        elif (
            snippet.author_id == ctx.author.id
            or ctx.author.guild_permissions.manage_messages
        ):
            await self.bot.db.delete("snippets", "title", title)
            await ctx.send(f"Snippet {title} deleted succesfully. ")
        else:
            await ctx.send(
                f"You're not the author of {title} and don't have permission to do this. "
            )

    @snippet.command(aliases=["lo"])
    async def lock(self, ctx: commands.Context, title: str) -> None:
        snippet = await self.get_snippet(ctx, title)
        if (
            snippet.author_id != ctx.author.id
            and not ctx.author.guild_permissions.manage_messages
        ):
            await ctx.send(
                f"You're not the author of {title} and don't have permission to do this. "
            )
        elif snippet.locked:
            await ctx.send("This snippet is already locked. ")
        else:
            await self.bot.db.update("snippets", "locked", True, "title", title)
            await ctx.send(f"Snippet {title} has been locked. ")

    @snippet.command(aliases=["ul"])
    async def unlock(self, ctx: commands.Context, title: str) -> None:
        snippet = await self.get_snippet(ctx, title)
        if (
            snippet.author_id != ctx.author.id
            and not ctx.author.guild_permissions.manage_messages
        ):
            await ctx.send(
                f"You're not the author of {title} and don't have permission to do this. "
            )
        elif not snippet.locked:
            await ctx.send("This snippet is already unlocked. ")
        else:
            await self.bot.db.update("snippets", "locked", False, "title", title)
            await ctx.send(f"Snippet {title} has been unlocked. ")

    @snippet.command(name="list", aliases=["l"])
    async def snippet_list(self, ctx: commands.Context) -> None:
        result_list = await self.bot.db.get_all("snippets")
        message = await self.message_list_builder(result_list)
        await ctx.send(message)

    @snippet.command(aliases=["b"])
    @commands.has_permissions(moderate_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member) -> None:
        pass

    @snippet.command(aliases=["ub"])
    @commands.has_permissions(moderate_members=True)
    async def unban(self, ctx: commands.Context, user: discord.Member) -> None:
        pass

    @snippet.command(aliases=["au"])
    async def author(self, ctx: commands.Context, user: discord.Member) -> None:
        group_result = await self.bot.db.get_all_where("snippets", "author_id", user.id)
        if group_result == []:
            message = "This user hasn't made any snippets. "
        else:
            message = self.message_list_builder(group_result)
        await ctx.send(message)


async def setup(bot) -> None:
    await bot.add_cog(Snippets(bot))
