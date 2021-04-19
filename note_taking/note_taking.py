# Contains the commands for the note-taking features of the bot.
import sqlite3
import discord
from discord.ext import commands


class Database:

    @staticmethod
    def create_connection(db_file=r'database\notes.db'):
        "Create a database connection to a SQLite database"
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            Database.create_required_tables(conn)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                return conn

    @staticmethod
    def create_required_tables(conn):
        try:
            c = conn.cursor()

            sql_code = """CREATE TABLE IF NOT EXISTS notes (
                id integer PRIMARY KEY,
                user text NOT NULL,
                title text NOT NULL,
                note text NOT NULL
                );"""

            c.execute(sql_code)
            conn.commit()

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def check_notes(user: str):
        try:
            conn = Database.create_connection()

            c = conn.cursor()
            sql_code = f"""SELECT * FROM notes WHERE user=?"""
            c.execute(sql_code, (user,))

            rows = c.fetchall()
            return rows

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def add_note(user: str, title: str, content: str):
        try:
            conn = Database.create_connection()
            c = conn.cursor()
            sql_code = f"""INSERT INTO notes(title,note,user) VALUES(?,?,?)"""
            values = (title, content, user)

            c.execute(sql_code, values)
            conn.commit()
            conn.close()

            return c.lastrowid
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def remove_note(title: str, user: str):
        try:
            conn = Database.create_connection()
            c = conn.cursor()
            sql_code = f"""DELETE FROM notes WHERE title = ? AND user = ?"""

            c.execute(sql_code, (title, user,))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(e)


@commands.command(aliases=['notes'])
async def check_notes(ctx):
    rows = Database.check_notes(user=str(ctx.message.author))

    items = []
    if rows:
        for row in rows:
            items.append(f"({row[0]}) {row[2]}")

    embed = discord.Embed(description="**YOUR NOTES:**\n\n" + '\n'.join(items))
    await ctx.send(embed=embed)


@commands.command(aliases=['note'])
async def read_note(ctx, title):
    embed = discord.Embed(description="And, on the third day...")
    await ctx.send(embed=embed)


@commands.command(aliases=['writenote'])
async def write_note(ctx, title, *, content):
    Database.add_note(user=str(ctx.message.author),
                      title=title, content=content)

    embed = discord.Embed(description=f"**{title}**\n\n{content}")
    await ctx.send(embed=embed)


@commands.command(aliases=['removenote'])
async def remove_note(ctx, title):
    Database.remove_note(title=title, user=str(ctx.message.author))

    embed = discord.Embed(description=f"**{title}** has been removed!")
    await ctx.send(embed=embed)


def setup(client):
    client.add_command(check_notes)
    client.add_command(read_note)
    client.add_command(write_note)
    client.add_command(remove_note)
