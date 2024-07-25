import disnake
import logging
import os

logging.basicConfig(level=logging.INFO)
intents = disnake.Intents.all()

client = disnake.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
        print(f'Message from {message.author}: {message.content}')

client.run(os.getenv('DISCORD_TOKEN'))