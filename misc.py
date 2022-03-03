from discord.ext import commands
import discord
import random
import os
import psycopg2


@commands.command()
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)


@commands.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} was kicked for the following reason:\n{reason}")


@commands.command(aliases=["8ball"])
async def _8ball(ctx, *, question=None):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
    ]

    if question is not None:
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")
    else:
        await ctx.send(
            embed=discord.Embed(
                description="**8 Ball:** You need to give a question as well."
            )
        )


@commands.command(aliases=["test-db"])
async def test_db(ctx):
    DATABASE_URL = os.environ.get("DATABASE_URL")
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()

    await ctx.send("Successfully connected to Postgres database.")
    await ctx.send(str(cur))

def setup(client):
    client.add_command(clear)
    client.add_command(kick)
    client.add_command(_8ball)
    client.add_command(test_db)
