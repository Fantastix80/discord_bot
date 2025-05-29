import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Configuration
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# Logging
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user.name} est opérationnel!")
    extensions = [
        "commands.help",
        "commands.minecraft",
        "events.message"
    ]
    for extension in extensions:
        await bot.load_extension(extension)

# Lancement du bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)