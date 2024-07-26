import disnake
from disnake.ext import commands
import logging
import os
import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS time(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    userid INTEGER NOT NULL,
    start INTEGER NOT NULL,
    end INTEGER)
""")

logging.basicConfig(level=logging.INFO)
intents = disnake.Intents.all()
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(
    command_prefix='!',
    test_guilds=[1264261709900677180], # Optional
    command_sync_flags=command_sync_flags,
    intents=intents
)


@bot.slash_command(description="All things timer related")
async def time(inter):
    pass


@time.sub_command(description="Starts a timer for you")
async def start(inter: disnake.ApplicationCommandInteraction):
    start = int(inter.created_at.timestamp())
    user = inter.user

    # Make sure they have not started more than one timer
    result = cur.execute(f"SELECT id, start FROM time WHERE end IS NULL AND userid={user.id}").fetchone()
    if result is not None:
        start_time = result[1]
        await inter.response.send_message(f"You have already started a timer <t:{start_time}:R>.")
        return

    cur.execute(f"INSERT INTO time(userid, start) VALUES ({user.id}, {start})")
    con.commit()
    await inter.response.send_message(f"Starting timer for {user.mention} at <t:{start}:t>.")


@time.sub_command(description="Stops any previous timers")
async def stop(inter: disnake.ApplicationCommandInteraction):
    end = int(inter.created_at.timestamp())
    user = inter.user
    cur.execute(f"""
    UPDATE OR ROLLBACK time
        SET end = {end}
        WHERE userid = {user.id};
    """)
    con.commit()
    await inter.response.send_message(f"Stopped for {user.mention} at <t:{end}:t>.")


bot.run(os.getenv('DISCORD_TOKEN'))
