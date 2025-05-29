from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(f"Voici la liste des commandes disponibles :\n\n- !minecraft : Affiche l'état du serveur et les joueurs connectés'.\n")


async def setup(bot):
    await bot.add_cog(Help(bot))