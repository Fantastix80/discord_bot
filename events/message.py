from discord.ext import commands
from config import FORBIDDEN_WORDS


class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Répondre 'feur !' si le message fini par 'quoi'
        if message.content.endswith("quoi"):
            await message.channel.send("feur !")

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))