import discord
from discord.ext import commands


class PollCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title="Nouveau sondage", description=question, color=discord.Color.green())
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")


async def setup(bot):
    await bot.add_cog(PollCommands(bot))