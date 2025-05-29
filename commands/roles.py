import discord
from discord.ext import commands
from config import SECRET_ROLE


class RoleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def assign(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE)
        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f"Le rôle {role.name} vous a été attribué, {ctx.author.mention} !")
        else:
            await ctx.send(f"Le rôle {SECRET_ROLE} n'existe pas sur ce serveur.")

    @commands.command()
    async def remove(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=SECRET_ROLE)
        if role:
            await ctx.author.remove_roles(role)
            await ctx.send(f"Le rôle {role.name} vous a été retiré, {ctx.author.mention} !")
        else:
            await ctx.send(f"Le rôle {SECRET_ROLE} n'existe pas sur ce serveur.")


async def setup(bot):
    await bot.add_cog(RoleCommands(bot))