from discord.ext import commands


class ReadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Hello à tous, je suis {self.bot.user.name}. Au plaisir de pouvoir vous servir !")


async def setup(bot):
    await bot.add_cog(ReadyEvent(bot))