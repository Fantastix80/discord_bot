from discord.ext import commands, tasks
import os
import re
from config import DISCORD_CHANNEL_ID_CONSOLE_MC, LATEST_LOGS_PATH

CHAT_LINE_REGEX = re.compile(r'<(.+?)> (.+)')

class ConsoleMinecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_position = 0
        self.monitor_log.start()

    def cog_unload(self):
        self.monitor_log.cancel()

    @tasks.loop(seconds=2)
    async def monitor_log(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID_CONSOLE_MC)
        if channel is None:
            return

        if not os.path.exists(LATEST_LOGS_PATH):
            return

        with open(LATEST_LOGS_PATH, "r", encoding="utf-8") as log_file:
            log_file.seek(self.last_position)
            lines = log_file.readlines()
            self.last_position = log_file.tell()

        for line in lines:
            if "<" in line and ">" in line:
                # Extrait le texte entre les <> et le message
                match = re.search(r']:\s*<(.+?)>\s*(.+)', line)
                if match:
                    user, message = match.groups()
                    await channel.send(f"💬 **{user}** : {message}")

                # Extrait le texte entre les <> et le message envoyé par le bot discord
                match = re.search(r'\[Server\] \s*<(.+?)>\s*(.+)', line)
                if match:
                    user, message = match.groups()
                    await channel.send(f"📢 **{user}** : {message}")

    @monitor_log.before_loop
    async def before_monitor_log(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ConsoleMinecraft(bot))
