from discord.ext import commands
import discord


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="📖 Commandes disponibles",
            description="Voici la liste des commandes que tu peux utiliser :",
            color=discord.Color.blue()
        )
        embed.add_field(name="!minecraft", value="Affiche l’état du serveur Minecraft et les joueurs connectés.", inline=False)
        embed.add_field(name="!help", value="Affiche ce menu d'aide.", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))