# Contains the commands for the note-taking features of the bot.
import sqlite3
from typing import List, Tuple
import discord
from discord.ext import commands


class Database:
    "This class contains all the methods that involve interacting and working with the database. The bot commands simply call these methods to perform operations on the database."

    @staticmethod
    def create_connection(db_file=r'database\notes.db') -> sqlite3.Connection:
        "Create a database connection to a SQLite database. Returns an sqlite3.Connection object."
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
    def create_required_tables(conn: sqlite3.Connection):
        """
        Creates a table called 'notes' in the database. Takes in a 'sqlite.Connection' object and executes the SQL code to create the necessary tables.
        This function is automatically called as soon as a connection is created, in the Database.create_connection() function.
        """
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
    def check_notes(user: str) -> List:
        """
        Retrieves the 'notes' from the database which belong to the given user and returns them as a List object.
        param <user>: A string that contains the User's name and discord tag, for example Hassan#3557.
        """
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
    def read_note(user: str, title: str) -> Tuple:
        """
        Returns a 'note' tuple from the database which matches the given parameters.

        param <user>: A string that contains the User's name and discord tag, for example Hassan#3557.
        param <title>: A string that uniquely identifies the note. Each note has a title.
        """
        try:
            conn = Database.create_connection()

            c = conn.cursor()
            sql_code = f"""SELECT * FROM notes WHERE user=? AND title=?"""
            c.execute(sql_code, (user, title))

            note = c.fetchone()
            return note

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def add_note(user: str, title: str, content: str):
        """
        Creates a 'note' in the database and returns the Row ID of that note.

        param <user>: A string that contains the User's name and discord tag, for example Hassan#3557.
        param <title>: A string that uniquely identifies the note. Each note has a title.
        param <content>: A string that contains all the content in the note.
        """
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
        """
        Removes a 'note' from the database.

        param <title>: A string that uniquely identifies the note. Each note has a title.
        param <user>: A string that contains the User's name and discord tag, for example Hassan#3557.
        """
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
    note = Database.read_note(user=str(ctx.message.author), title=title)
    if note:
        embed = discord.Embed(description=f"**{note[2]}**\n\n{note[3]}")
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=discord.Embed(description="Either this note does not exist or you entered the wrong title. Try again."))


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
