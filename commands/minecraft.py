from discord.ext import commands
import discord
import subprocess
import time
import re
import os


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def minecraft(self, ctx):
        try:
            # Vérifier si le service Minecraft est actif
            service_status = subprocess.check_output(
                ["systemctl", "is-active", "minecraft.service"],
                stderr=subprocess.STDOUT
            ).decode().strip()
        except subprocess.CalledProcessError as e:
            service_status = "unknown"

        if service_status != "active":
            embed = discord.Embed(title="🟢 Serveur Minecraft", color=discord.Color.red())
            embed.add_field(name="Statut", value="Inactif", inline=False)

            await ctx.reply(embed=embed)
            return

        # Envoyer la commande "list" dans la console du serveur Minecraft
        subprocess.run(['screen', '-S', 'mc', '-p', '0', '-X', 'stuff', 'list\n'])

        time.sleep(1)

        # Puis on récupère la sortie de la commande dans le fichier de log
        log_path = "/sftp/serveur_mc/logs/latest.log"
        if not os.path.exists(log_path):
            await ctx.reply("❗ Impossible de trouver le fichier de log Minecraft.")
            return

        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Trouver la ligne avec la réponse à la commande "list"
        list_line = None
        for line in reversed(lines):
            if "There are" in line and "players online" in line:
                list_line = line
                break

        if not list_line:
            await ctx.reply("⚠️ Impossible de récupérer la liste des joueurs.")
            return

        # Extraire les infos
        match = re.search(r'There are (\d+) of a max of \d+ players online: (.*)', list_line)
        if match:
            count = match.group(1)
            players = match.group(2)
            players = players if players.strip() else "Aucun joueur connecté"
        else:
            count = "0"
            players = "Aucun joueur connecté"

        # Répondre sur Discord
        embed = discord.Embed(title="🟢 Serveur Minecraft", color=discord.Color.green())
        embed.add_field(name="Statut", value="Actif", inline=False)
        embed.add_field(name="Joueurs connectés", value=f"{count}", inline=False)
        embed.add_field(name="Noms", value=players, inline=False)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Minecraft(bot))