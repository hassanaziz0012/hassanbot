import discord
import random
from discord.ext import commands
import requests
from config import token

client = commands.Bot(command_prefix='.')

responses = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes – definitely.',
    'You may rely on it.',

    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',

    'Reply hazy, try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',

    'Don\'t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.',
]


@client.event
async def on_ready():
    print("Bot is ready!")


@client.event
async def on_member_join(member):
    print(f"{member} has joined a server.")


@client.event
async def on_member_remove(member):
    print(f"{member} has left a server.")


@client.command(aliases=['download-attachments', 'dl-attachments'])
async def download_attachments(ctx, channel: discord.TextChannel):
    async for message in channel.history(limit=200):
        for attachment in message.attachments:
            url = attachment.url
            response = requests.get(url)
            with open(attachment.filename, 'wb+') as file:
                file.write(response.content)


@client.command()
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} was kicked for the following reason:\n{reason}')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

client.load_extension('wishlist.wishlist')
client.load_extension('note_taking.note_taking')
client.load_extension('reminders.reminders')

if __name__ == '__main__':
    client.run(token)
