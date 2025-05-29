import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

secret_role = "test_bot"

@bot.event
async def on_ready():
    print(f"Hello à tous, je suis {bot.user.name}. Au plaisir de pouvoir vous servir !")

@bot.event
async def on_member_join(member):
    await member.send(f"Bienvenue sur le serveur {member.name} !")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.endswith("quoi"):
        await message.channel.send(f"feur !")

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, pas de grossièretés ici !")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention} !")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"Le rôle {role.name} vous a été attribué, {ctx.author.mention} !")
    else:
        await ctx.send(f"Le rôle {secret_role} n'existe pas sur ce serveur.")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"Le rôle {role.name} vous a été retiré, {ctx.author.mention} !")
    else:
        await ctx.send(f"Le rôle {secret_role} n'existe pas sur ce serveur.")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"Tu as dit: {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply(f"Voici une réponse à ta commande.")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Nouveau sondage", description=question, color=discord.Color.green())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send(f"Voici le message secret: prout !")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"Vous devez avoir le rôle {secret_role} pour utiliser cette commande.")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)