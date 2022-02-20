from utils import (
    change_file_permissions_to_anyone,
    delete_downloaded_files,
    delete_file_from_google_drive,
    download_attachment,
    upload_to_gdrive,
)
import discord
import random
from discord.errors import HTTPException
from discord.ext import commands
import requests
from config import token
from zipfile import ZipFile
import asyncio
import os
import psycopg2
import re

from reminders.reminders import check_for_due_reminders, remove_due_reminders

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=".", intents=intents)

responses = [
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes – definitely.",
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


@client.event
async def on_ready():
    # We're basically using the on_ready event to check for due reminders.
    print("Bot is ready")
    while True:
        due_reminders = await check_for_due_reminders()
        if due_reminders is not None:
            general_channel = client.get_channel(832222029075447871)
            for reminder in due_reminders:
                user = client.get_user(int(reminder[2]))
                await general_channel.send(f"{reminder[3]} is due! {user.mention}")
                await remove_due_reminders(reminder)

        await asyncio.sleep(3)
        # print("Checking for reminders...")


@client.command(aliases=["download-attachments", "dl-attachments"])
async def download_attachments(ctx, channel: discord.TextChannel):
    await ctx.send(
        "Downloading attachments from this channel. This may take a long time. Please wait."
    )
    with ZipFile(f"{channel.name} - Attachments.zip", "w") as zip:
        async for message in channel.history(limit=200):
            for i, attachment in enumerate(message.attachments):
                file_name = download_attachment(i, attachment)
                print(f"Adding {file_name} to archive...")
                zip.write(file_name)
                asyncio.sleep(0.1)

        await ctx.send(
            "Downloaded and Archived all attachments from this channel. Uploading .zip archive to Discord..."
        )
        zip.close()

        # Discord only allows file uploads of 8MB maximum. So, we check if our file is too large. It will raise the HTTPException error if the filesize is too large.
        # If it is too large, we will upload to Google Drive instead, and will give the user a temporary link to download the file. This link will expire in 1 hour
        # and the file will be deleted.
        try:
            await ctx.send(file=discord.File(f"{channel.name} - Attachments.zip"))
        except HTTPException:
            await ctx.send(
                "File is too large to upload to Discord. Uploading to Google Drive..."
            )

            result = upload_to_gdrive(zip)
            await ctx.send(
                embed=discord.Embed(
                    description=f"Finished uploading to Google Drive. Please go to the following link to download the file:\n{result['download_link']}\n\nThis link will automatically expire after **1 hour**."
                )
            )

            # Change perms so anyone can see and download the file.
            change_file_permissions_to_anyone(result["file_id"])

            # Delete file from GDrive after one hour.
            await asyncio.sleep(86400)
            delete_file_from_google_drive(result["file_id"])

    # Deleting downloaded files so we don't waste precious space.
    delete_downloaded_files()

@client.command()
async def remove_urls(ctx):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=1000):
                regex = r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
                match = re.search(regex, message.content)
                if match:
                    await message.delete()
    print("Command finished.")

@client.command()
async def remove_text(ctx, text: str):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=1000):
                if text in message.content:
                    await message.delete()
    print("Command finished.")

@client.command()
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} was kicked for the following reason:\n{reason}")


@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question=None):
    if question is not None:
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")
    else:
        await ctx.send(
            embed=discord.Embed(
                description="**8 Ball:** You need to give a question as well."
            )
        )


@client.command(aliases=["test-db"])
async def test_db(ctx):
    DATABASE_URL = os.environ.get("DATABASE_URL")
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()

    await ctx.send("Successfully connected to Postgres database.")
    await ctx.send(str(cur))


client.load_extension("wishlist.wishlist")
client.load_extension("note_taking.note_taking")
client.load_extension("reminders.reminders")

if __name__ == "__main__":
    client.run(token)
