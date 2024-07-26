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
    now = int(inter.created_at.timestamp())
    user = inter.user
    cur.execute(f"INSERT INTO time(userid, start) VALUES ({user.id}, {now})")
    con.commit()
    await inter.response.send_message(f"Starting timer for {user.mention} at <t:{now}:t>")


bot.run(os.getenv('DISCORD_TOKEN'))
