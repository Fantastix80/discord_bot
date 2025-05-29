from discord.ext import commands
from config import SECRET_ROLE


class SecretCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(SECRET_ROLE)
    async def secret(self, ctx):
        await ctx.send(f"Voici le message secret: prout !")

    @secret.error
    async def secret_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"Vous devez avoir le rôle {SECRET_ROLE} pour utiliser cette commande.")


async def setup(bot):
    await bot.add_cog(SecretCommands(bot))