import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

from reminders import RemindersCog

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=".", intents=intents)

# TODO: Improve the help command. Organize all extensions into Cogs and fix the docstrings in all commands. That way, the default help command will work in our favor.
# TODO: Configure a Volume in the Dockerfile so you can store the DB files outside the container. This is for local DBs of course. It'll help you learn Docker Volumes.
# TODO: Set up a PostgreSQL DB and set up a docker-compose.yml file and configure all necessary services.

@client.event
async def on_ready():
    # We're basically using the on_ready event to check for due reminders.
    print("Bot is ready")
    while True:
        due_reminders = await RemindersCog.check_for_due_reminders()
        if due_reminders is not None:
            general_channel = client.get_channel(832222029075447871)
            for reminder in due_reminders:
                user = client.get_user(int(reminder[2]))
                await general_channel.send(f"{reminder[3]} is due! {user.mention}")
                await RemindersCog.remove_due_reminders(reminder)

        await asyncio.sleep(3)
        # print("Checking for reminders...")


# Loading all bot extensions...
client.load_extension("wishlist")
client.load_extension("google_apis")
client.load_extension("note_taking")
client.load_extension("reminders")
client.load_extension("misc")
client.load_extension("text_remover")

if __name__ == "__main__":
    load_dotenv()
    token = os.environ.get('TOKEN')
    client.run(token)
