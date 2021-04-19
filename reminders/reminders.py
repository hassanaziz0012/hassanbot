import discord
from discord.ext import commands
from datetime import date, datetime
import sqlite3


class Database:

    @staticmethod
    def create_connection(db_file=r'database\reminders.db'):
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

            sql_code = """CREATE TABLE IF NOT EXISTS reminders (
                id integer PRIMARY KEY,
                user text NOT NULL,
                reminder text NOT NULL,
                time text NOT NULL
                );"""

            c.execute(sql_code)
            conn.commit()

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def check_reminders(user: str):
        try:
            conn = Database.create_connection()

            c = conn.cursor()
            sql_code = f"""SELECT * FROM reminders WHERE user=?"""
            c.execute(sql_code, (user,))

            rows = c.fetchall()
            return rows

        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def add_reminder(user: str, reminder: str, time: str):
        try:
            conn = Database.create_connection()
            c = conn.cursor()
            sql_code = f"""INSERT INTO reminders(user,reminder,time) VALUES(?,?,?)"""
            values = (reminder, time, user)

            c.execute(sql_code, values)
            conn.commit()
            conn.close()

            return c.lastrowid
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def remove_reminder(reminder: str, user: str):
        try:
            conn = Database.create_connection()
            c = conn.cursor()
            sql_code = f"""DELETE FROM reminders WHERE reminder = ? AND user = ?"""

            c.execute(sql_code, (reminder, user,))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(e)


@commands.command(aliases=["reminder"])
async def create_reminder(ctx, time, reminder):
    # Database.add_reminder(user=str(ctx.message.author), reminder=reminder, time=time)
    if 'd' in time:
        i_of_d = time.index('d')
        days_1 = int(time[i_of_d - 1])
        try:
            days_2 = int(time[i_of_d - 2])
            final_days = int(str(days_2) + str(days_1))
            print(final_days)
        except NameError as e:
            final_days = days_1
            print(final_days)


    embed = discord.Embed(
        description=f"Created reminder *\"{reminder}\"* due in **{time}**")
    await ctx.send(embed=embed)


@commands.command(aliases=["reminders"])
async def check_reminders(ctx):
    rows = Database.check_reminders(user=str(ctx.message.author))
    items = []

    if rows:
        for row in rows:
            items.append(f"({row[0]}) {row[2]} due at **{row[3]}**")
    embed = discord.Embed(
        description=f"**Reminders for {ctx.message.author.mention}**\n\n" + '\n'.join(items))
    await ctx.send(embed=embed)


@commands.command(aliases=["rm-reminder"])
async def remove_reminder(ctx, reminder):
    pass


def setup(client):
    client.add_command(check_reminders)
    client.add_command(create_reminder)
    client.add_command(remove_reminder)
