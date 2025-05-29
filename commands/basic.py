from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        print("Commande hello exécutée depuis Cog")
        await ctx.send(f"Hello {ctx.author.mention} !")

    @commands.command()
    async def reply(self, ctx):
        print("Commande reply exécutée depuis Cog")
        await ctx.reply(f"Voici une réponse à ta commande.")


async def setup(bot):
    await bot.add_cog(BasicCommands(bot))