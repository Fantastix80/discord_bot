import discord
from discord.ext import commands
import json
import os
from config import CUSTOM_COMMANDS, IMAGES_DIR

class CustomCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_data = self.load_commands()

    def load_commands(self):
        if not os.path.exists(CUSTOM_COMMANDS):
            return {}
        with open(CUSTOM_COMMANDS, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_commands(self):
        with open(CUSTOM_COMMANDS, "w", encoding="utf-8") as f:
            json.dump(self.commands_data, f, indent=2, ensure_ascii=False)

    @commands.group(invoke_without_command=True)
    async def command(self, ctx, subcommand=None, *args):
        if subcommand is None:
            embed = discord.Embed(
                title="🛠️ Gestion des commandes personnalisées",
                description="Voici comment utiliser le système de commandes personnalisées :",
                color=discord.Color.orange()
            )
            embed.add_field(
                name="➕ Créer une commande",
                value="`!command create <nom> <contenu>`\nCrée une commande personnalisée avec texte et/ou image.",
                inline=False
            )
            embed.add_field(
                name="📜 Lister les commandes",
                value="`!command list`\nAffiche toutes les commandes existantes avec leur auteur.",
                inline=False
            )
            embed.add_field(
                name="❌ Supprimer une commande",
                value="`!command delete <nom>`\nSupprime la commande personnalisée.",
                inline=False
            )
            embed.add_field(
                name="▶️ Utiliser une commande",
                value="`!command <nom>`\nExécute la commande personnalisée.",
                inline=False
            )
            embed.set_footer(text="Tu peux attacher une image lors de la création pour qu'elle soit incluse.")
            await ctx.reply(embed=embed)
            return

        # Exécution d'une commande personnalisée
        if subcommand not in self.commands_data:
            await ctx.reply(f"❌ La commande `{subcommand}` n'existe pas.")
            return

        data = self.commands_data[subcommand]

        if data.get("text") or data.get("image"):
            embed = discord.Embed(title=f"!command {subcommand}", description=data.get("text", ""),
                                  color=discord.Color.blue())

            file = None
            if data.get("image"):
                image_path = os.path.join(IMAGES_DIR, data["image"])
                if os.path.exists(image_path):
                    file = discord.File(image_path)
                    embed.set_image(url=f"attachment://{data['image']}")
                else:
                    await ctx.reply("❌ Image introuvable.")
                    return

            await ctx.reply(embed=embed, file=file)

    @command.command()
    async def create(self, ctx, name: str, *, content: str = None):
        if name in self.commands_data:
            await ctx.reply(f"❌ Une commande avec ce nom existe déjà.")
            return

        # Initialisation des champs
        command_data = {
            "author": str(ctx.author),
            "text": content if content else None,
            "image": None
        }

        attachment = ctx.message.attachments[0] if ctx.message.attachments else None

        if attachment:
            if not attachment.content_type.startswith("image/"):
                await ctx.reply(f"❌ Seules les images sont supportées pour l'instant.")
                return

            os.makedirs(IMAGES_DIR, exist_ok=True)

            filename = f"{name}_{attachment.filename}"
            path = os.path.join(IMAGES_DIR, filename)
            await attachment.save(path)

            command_data["image"] = filename

        if not command_data["text"] and not command_data["image"]:
            await ctx.reply(f"❗ Tu dois fournir au moins un texte ou une image.")
            return

        self.commands_data[name] = command_data
        self.save_commands()

        await ctx.message.delete()
        await ctx.send(f"✅ {ctx.author.mention} - La commande `{name}` a été enregistrée avec succès.")

    @command.command()
    async def delete(self, ctx, name: str):
        if name not in self.commands_data:
            await ctx.reply(f"❌ La commande `{name}` n'existe pas.")
            return

        data = self.commands_data[name]

        # Supprimer l'image si elle existe
        if data.get("image"):
            image_path = os.path.join(IMAGES_DIR, data["image"])
            if os.path.exists(image_path):
                os.remove(image_path)

        del self.commands_data[name]
        self.save_commands()
        await ctx.reply(f"🗑️ La commande `{name}` a été supprimée avec succès.")

    @command.command()
    async def list(self, ctx):
        if not self.commands_data:
            await ctx.reply("Aucune commande personnalisée disponible.")
            return

        embed = discord.Embed(title="📜 Commandes personnalisées", description="Liste des commandes disponibles avec leurs auteurs", color=discord.Color.purple())
        inline_items = len(self.commands_data) > 15
        for name in sorted(self.commands_data.keys()):
            data = self.commands_data[name]
            author = data.get("author", "Inconnu")
            embed.add_field(name=f"!command {name}", value=f"👤 {author}", inline=inline_items)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(CustomCommand(bot))