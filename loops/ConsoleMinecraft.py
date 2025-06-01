from discord.ext import commands, tasks
import discord
import os
import re
import subprocess
from config import DISCORD_CHANNEL_ID_CONSOLE_MC, LATEST_LOGS_PATH


class ConsoleMinecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_position = 0
        self.server_was_online = False
        self.monitor_log.start()
        self.check_server_status.start()

    def cog_unload(self):
        self.monitor_log.cancel()
        self.check_server_status.cancel()

    @tasks.loop(seconds=2)
    async def monitor_log(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID_CONSOLE_MC)
        if channel is None or not self.server_was_online:
            return

        if not os.path.exists(LATEST_LOGS_PATH):
            return

        with open(LATEST_LOGS_PATH, "r", encoding="utf-8") as log_file:
            log_file.seek(self.last_position)
            lines = log_file.readlines()
            self.last_position = log_file.tell()

        for line in lines:
            if "<" in line and ">" in line:
                match = re.search(r']:\s*<(.+?)>\s*(.+)', line)
                if match:
                    user, message = match.groups()
                    await channel.send(f"💬 **{user}** : {message}")

                match = re.search(r'\[Server\]\s*<(.+?)>\s*(.+)', line)
                if match:
                    user, message = match.groups()
                    await channel.send(f"📢 **{user}** : {message}")

    @tasks.loop(seconds=10)
    async def check_server_status(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID_CONSOLE_MC)
        if channel is None:
            return

        try:
            status = subprocess.check_output(
                ["systemctl", "is-active", "minecraft.service"],
                stderr=subprocess.STDOUT
            ).decode().strip()
            server_online = (status == "active")
        except subprocess.CalledProcessError:
            server_online = False

        if self.server_was_online and not server_online:
            self.server_was_online = False
            await self.clear_discord_channel(channel)

        elif server_online:
            self.server_was_online = True

    async def clear_discord_channel(self, channel):
        try:
            await channel.purge(limit=None)
            await channel.send(":broom: Salon vidé suite à l’arrêt du serveur Minecraft.")
        except Exception as e:
            print(f"Erreur lors de la purge du salon : {e}")

    @monitor_log.before_loop
    async def before_monitor_log(self):
        await self.bot.wait_until_ready()

    @check_server_status.before_loop
    async def before_check_server_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ConsoleMinecraft(bot))
