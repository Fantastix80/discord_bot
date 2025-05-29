from discord.ext import commands


class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(f"Bienvenue sur le serveur {member.name} !")


async def setup(bot):
    await bot.add_cog(MemberEvents(bot))