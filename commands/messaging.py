from discord.ext import commands


class MessagingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self, ctx, *, msg):
        await ctx.author.send(f"Tu as dit: {msg}")


async def setup(bot):
    await bot.add_cog(MessagingCommands(bot))