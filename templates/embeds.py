import discord
from discord.ext import commands


async def userEmbed(user: discord.Member) -> discord.Embed:
    embed = discord.Embed(title="User Information", color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="User Name", value=f"{user.name}", inline=True)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(
        name="Account Created",
        value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        inline=False,
    )
    embed.add_field(
        name="Roles",
        value=", ".join([r.mention for r in user.roles][1:][::-1]),
        inline=True,
    )
    return embed


async def serverEmbed(ctx: commands.Context) -> discord.Embed:
    server = ctx.guild
    if server is None:
        raise commands.NoPrivateMessage
    embed = discord.Embed(title="Server Information", color=discord.Color.blue())
    embed.set_thumbnail(url=server.icon.url if server.icon else None)
    embed.add_field(name="Server Name", value=f"{server.name}", inline=True)
    embed.add_field(name="Server ID", value=f"**{server.id}**", inline=True)
    embed.add_field(name="Owner", value=f"{server.owner}", inline=True)
    embed.add_field(name="Member Count", value=server.member_count, inline=True)
    embed.set_footer(
        text=f"Server created at: {server.created_at.strftime('%Y/%m/%d')}",
    )
    return embed


async def roleEmbed(target: discord.Role) -> discord.Embed:
    embed = discord.Embed(title="Role Info", color=target.color)
    embed.add_field(name="Role Name", value=target.mention, inline=True)
    embed.add_field(name="Role ID", value=target.id, inline=False)
    embed.add_field(name="Member Count", value=len(target.members), inline=False)
    embed.add_field(name="Role Color", value=str(target.color), inline=False)
    return embed


async def roleListEmbed(ctx: commands.Context) -> discord.Embed:
    if ctx.guild is None:
        raise commands.NoPrivateMessage
    embed = discord.Embed(title="Role List", color=discord.Color.blue())
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
    embed.add_field(
        name="Roles",
        value="\n".join([r.mention for r in ctx.guild.roles][1:][::-1]),
        inline=False,
    )
    return embed


def correctUsageEmbed(language: str) -> discord.Embed:
    embed = discord.Embed(
        title=f"{language} correct usage", color=discord.Color.green()
    )
    if language == "Python":
        embed.add_field(
            name="\u200b",
            value=r"\`\`\`py" + "\ncode here \n" + r"\`\`\`",
            inline=False,
        )
        embed.add_field(name="Example", value='```py\nprint("Hello, World!") \n```')

    elif language == "Go":
        embed.add_field(
            name="\u200b",
            value=r"\`\`\`go" + "\npackage main \ncode here \n" + r"\`\`\`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="```go\npackage main \n\nimport 'fmt' \n\nfunc main() {\n  fmt.Println('Hello, World!') \n} \n```",
            inline=False,
        )

    elif language == "Brainfuck":
        embed.add_field(
            name="\u200b",
            value=r"\`\`\`bf" + "\ncode here \n" + r"\`\`\`",
            inline=False,
        )
        embed.add_field(
            name="Example",
            value="```bf\n++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.\n```",
            inline=False,
        )

    return embed
