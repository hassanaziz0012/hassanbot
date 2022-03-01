import discord
from discord.ext import commands
from config import token
import asyncio

from reminders.reminders import check_for_due_reminders, remove_due_reminders

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=".", intents=intents)


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


# Loading all bot extensions...
client.load_extension("wishlist.wishlist")
client.load_extension("google.google_apis")
client.load_extension("note_taking.note_taking")
client.load_extension("reminders.reminders")
client.load_extension("misc.misc")
client.load_extension("text_removal.remover")

if __name__ == "__main__":
    client.run(token)
