from discord.ext import commands
import discord


@commands.command()
async def remove_urls(ctx):
    await ctx.send("Scanning server contents. May take a while...")
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=1000):
                regex = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
                match = re.search(regex, message.content)
                if match:
                    await message.delete()
    await ctx.send("Command finished.")

@commands.command()
async def copy_urls(ctx):
    await ctx.send("Scanning server contents. May take a while...")
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=1000):
                regex = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
                match = re.search(regex, message.content)
                if match:
                    await ctx.send(message.content)
    await ctx.send("Command finished.")

@commands.command()
async def remove_text(ctx, text: str):
    await ctx.send("Scanning server contents. May take a while...")
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=1000):
                if text in message.content:
                    await message.delete()
    await ctx.send("Command finished.")

def setup(client):
    client.add_command(remove_urls)
    client.add_command(copy_urls)
    client.add_command(remove_text)
