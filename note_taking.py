# Contains the commands for the note-taking features of the bot.
import sqlite3
from typing import List, Tuple
import discord
from discord.ext import commands


class Database:
    "This class contains all the methods that involve interacting and working with the database. The bot commands simply call these methods to perform operations on the database."

    @staticmethod
    def create_connection(db_file=r"database\notes.db") -> sqlite3.Connection:
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
                user_id integer NOT NULL,
                title text NOT NULL,
                note text NOT NULL
                );"""

            c.execute(sql_code)
            conn.commit()

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def check_notes(user_id: int) -> List:
        """
        Retrieves the 'notes' from the database which belong to the given user and returns them as a List object.

        param <user_id>: An integer that contains the user's ID, which is like a very long number.
        """
        try:
            conn = Database.create_connection()

            c = conn.cursor()
            sql_code = f"""SELECT * FROM notes WHERE user_id=?"""
            c.execute(sql_code, (user_id,))

            rows = c.fetchall()
            return rows

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def read_note(user_id: int, title: str) -> Tuple:
        """
        Returns a 'note' tuple from the database which matches the given parameters.

        param <user_id>: An integer that contains the user's ID, which is like a very long number.
        param <title>: A string that uniquely identifies the note. Each note has a title.
        """
        try:
            conn = Database.create_connection()

            c = conn.cursor()
            sql_code = f"""SELECT * FROM notes WHERE user_id=? AND title=?"""
            c.execute(sql_code, (user_id, title))

            note = c.fetchone()
            return note

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def add_note(user_id: int, user: str, title: str, content: str):
        """
        Creates a 'note' in the database and returns the Row ID of that note.

        param <user>: A string that contains the User's name and discord tag, for example Hassan#3557.
        param <user_id>: An integer that contains the user's ID, which is like a very long number.
        param <title>: A string that uniquely identifies the note. Each note has a title.
        param <content>: A string that contains all the content in the note.
        """
        try:
            conn = Database.create_connection()
            c = conn.cursor()
            sql_code = f"""INSERT INTO notes(title,note,user_id,user) VALUES(?,?,?,?)"""
            values = (title, content, user_id, user)

            c.execute(sql_code, values)
            conn.commit()
            conn.close()

            return c.lastrowid
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def remove_note(title: str, user_id: int):
        """
        Removes a 'note' from the database.

        param <title>: A string that uniquely identifies the note. Each note has a title.
        param <user_id>: An integer that contains the user's ID, which is like a very long number.
        """
        try:
            conn = Database.create_connection()
            c = conn.cursor()
            sql_code = f"""DELETE FROM notes WHERE title = ? AND user_id = ?"""

            c.execute(
                sql_code,
                (
                    title,
                    user_id,
                ),
            )
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(e)

class NotesCog(commands.Cog, name="Notes"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(aliases=["notes"])
    async def check_notes(ctx):
        "This command will retrieve all notes from the Database that belong to the user who sent the command."
        rows = Database.check_notes(user_id=int(ctx.message.author.id))

        items = []
        if rows:
            for row in rows:
                items.append(f"({row[0]}) {row[3]}")

        embed = discord.Embed(description="**YOUR NOTES:**\n\n" + "\n".join(items))
        await ctx.send(embed=embed)


    @commands.command(aliases=["note"])
    async def read_note(ctx, title: str = None):
        """
        This function retrieves a single note which matches the given 'title' and belongs to the user who sent the command.

        param <title>: A string that uniquely identifies the note. Each note has a title.
        """
        if title is not None:
            note = Database.read_note(user_id=int(ctx.message.author.id), title=title)
            if note:
                embed = discord.Embed(description=f"**{note[3]}**\n\n{note[4]}")
                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    embed=discord.Embed(
                        description="Either this note does not exist or you entered the wrong title. Try again."
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    description="You forgot to enter a title. You need to type the title of the note."
                )
            )


    @commands.command(aliases=["writenote"])
    async def write_note(ctx, title: str = None, *, content: str = None):
        """
        This function calls the add_note() function in the Database class to create a new note. It takes the following parameters:

        param <title>: A string that uniquely identifies the note. Each note has a title.
        param <content>: A string that contains all the content in the note.
        """
        if title is not None and content is not None:
            Database.add_note(
                user=str(ctx.message.author),
                user_id=int(ctx.message.author.id),
                title=title,
                content=content,
            )

            embed = discord.Embed(description=f"**{title}**\n\n{content}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                embed=discord.Embed(
                    description="""
                        You forgot to enter either a title or some content for this note. Please try again and enter both a title and the content for this note. 
                        \nRemember that the title should be enclosed in double quotes, such as, "Title goes here". You don\'t have to enclose the content in double quotes.
                        """
                )
            )


    @commands.command(aliases=["removenote"])
    async def remove_note(ctx, title=None):
        """
        This function is used to remove a note from the database.

        param <title>: A string that uniquely identifies the note. Each note has a title.
        """
        if title is not None:
            selected_note = Database.read_note(
                user_id=int(ctx.message.author.id), title=title
            )
            if selected_note is not None:
                Database.remove_note(title=title, user_id=int(ctx.message.author.id))
            else:
                await ctx.send(
                    embed=discord.Embed(
                        description="The title you entered does not match any existing note. Please try again."
                    )
                )
                return

            embed = discord.Embed(description=f"**{title}** has been removed!")
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                embed=discord.Embed(
                    description="You did not enter a title. Please enter the title of the note you want to delete."
                )
            )


def setup(client):
    client.add_cog(NotesCog(client))
