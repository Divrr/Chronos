import disnake
from disnake.ext import commands
import logging
import os

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


@time.sub_command()
async def start(inter: disnake.ApplicationCommandInteraction):
    """
    Starts a timer for you
    """
    now = inter.created_at.timestamp()
    user = inter.user

    await inter.response.send_message(f"Starting timer for {user.mention} at <t:{int(now)}:t>")


bot.run(os.getenv('DISCORD_TOKEN'))
