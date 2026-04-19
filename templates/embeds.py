import discord
from discord.ext import commands


async def userEmbed(user: discord.Member):
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


async def serverEmbed(ctx: commands.Context):
    server = ctx.guild
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


async def roleEmbed(target: discord.Role = None):
    embed = discord.Embed(title="Role Info", color=target.color)
    embed.add_field(name="Role Name", value=target.mention, inline=True)
    embed.add_field(name="Role ID", value=target.id, inline=False)
    embed.add_field(name="Member Count", value=len(target.members), inline=False)
    embed.add_field(name="Role Color", value=str(target.color), inline=False)
    return embed


async def roleListEmbed(ctx: commands.Context):
    embed = discord.Embed(title="Role List", color=discord.Color.blue())
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
    embed.add_field(
        name="Roles",
        value="\n".join([r.mention for r in ctx.guild.roles][1:][::-1]),
        inline=False,
    )
    return embed
