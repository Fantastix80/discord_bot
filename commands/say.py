from discord.ext import commands
import subprocess


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message: str):
        try:
            # Vérifier si le service Minecraft est actif
            service_status = subprocess.check_output(
                ["systemctl", "is-active", "minecraft.service"],
                stderr=subprocess.STDOUT
            ).decode().strip()
        except subprocess.CalledProcessError as e:
            service_status = "unknown"

        if service_status != "active":
            await ctx.reply("❌ La serveur minecraft n'est pas allumé.")
            return

        # Envoyer la commande "list" dans la console du serveur Minecraft
        minecraft_command = f"say <{ctx.author}> {message}\n"
        result = subprocess.run(["screen", "-S", "mc", "-p", "0", "-X", "stuff", minecraft_command], capture_output=True, text=True)

        if result.returncode == 0:
            await ctx.reply("✅ Votre message a bien été envoyé dans le serveur Minecraft.")
        else:
            await ctx.reply(f"❌ Une erreur est survenue lors de l'envoi de la commande.")


async def setup(bot):
    await bot.add_cog(Say(bot))