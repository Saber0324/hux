from datetime import datetime
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


async def serverEmbed(interaction: discord.Interaction) -> discord.Embed:
    server = interaction.guild
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


async def roleListEmbed(interaction: discord.Interaction) -> discord.Embed:
    if interaction.guild is None:
        raise commands.NoPrivateMessage
    embed = discord.Embed(title="Role List", color=discord.Color.blue())
    embed.set_thumbnail(
        url=interaction.guild.icon.url if interaction.guild.icon else None
    )
    embed.add_field(
        name="Roles",
        value="\n".join([r.mention for r in interaction.guild.roles][1:][::-1]),
        inline=False,
    )
    return embed


def correctUsageEmbed(language: str) -> discord.Embed:
    description = ""
    embed = discord.Embed(
        title=f"{language} correct usage",
        color=discord.Color.green(),
        description=description,
    )
    if language == "Python":
        description = "!e" + "\n" + r"\`\`\`py" + "\ncode here \n" + r"\`\`\`"
        embed.add_field(
            name="Example", value='```py\nprint("Hello, World!") \n```', inline=False
        )

    elif language == "Go":
        description = (
            "!e" + "\n" + r"\`\`\`go" + "\npackage main \ncode here \n" + r"\`\`\`"
        )
        embed.add_field(
            name="Example",
            value="```go\npackage main \n\nimport 'fmt' \n\nfunc main() {\n  fmt.Println('Hello, World!') \n} \n```",
            inline=False,
        )

    elif language == "Brainfuck":
        description = "!e" + "\n" + r"\`\`\`bf" + "\ncode here \n" + r"\`\`\`"
        embed.add_field(
            name="Example",
            value="```bf\n++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.\n```",
            inline=False,
        )

    elif language == "Rust":
        description = "!e" + "\n" + r"\`\`\`rs" + "\ncode here \n" + r"\`\`\`"
        embed.add_field(
            name="Example",
            value='```rs\nfn main() {\n  println!("Hello, World!");\n}\n```',
            inline=False,
        )
    elif language == "C":
        description = "!e" + "\n" + r"\`\`\`c" + "\ncode here \n" + r"\`\`\`"
        embed.add_field(
            name="Example",
            value='```c\n#include <stdio.h>\n\nint main(void) {\n    puts("Hello, world!");\n}```',
            inline=False,
        )
    elif language == "C++":
        description = "!e" + "\n" + r"\`\`\`cpp" + "\ncode here \n" + r"\`\`\`"
        embed.add_field(
            name="Example",
            value='```cpp\n#include <iostream>\n\nint main(void) {\n  std::cout << "Hello, world!";\n}```',
            inline=False,
        )
    elif language == "C#":
        description = "!e" + "\n" + r"\`\`\`cs" + "\ncode here \n" + r"\`\`\`"
        embed.add_field(
            name="Example",
            value='```cs\nConsole.WriteLine("Hello World!");```',
            inline=False,
        )

    return embed


def github_repo_embed(repo: dict):
    if repo is not None:
        date = int(
            datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        )
        embed = discord.Embed(
            title=f"{repo['name']}",
            url=repo["url"],
            color=discord.Color.random(),
            description=f"{repo['description']}\n\nCreated at <t:{date}:D>",
        )
        embed.set_thumbnail(url=repo["owner_avatar"])
        embed.set_footer(text=repo["license_name"])
        return embed


def github_user_embed(user: dict) -> discord.Embed:
    if user is not None:
        embed = discord.Embed(
            title=user["login"],
            url=user["url"],
            description=user["bio"],
            color=discord.Color.random(),
        )
        embed.set_thumbnail(url=user["avatar"])
        embed.set_footer(text=f"Public repos: {user['repos']}")
        return embed
