from discord.ext import commands
from config import FORBIDDEN_WORDS


class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Réponse "feur" à "quoi"
        if message.content.endswith("quoi"):
            await message.channel.send(f"feur !")

        # Modération des mots interdits
        for word in FORBIDDEN_WORDS:
            if word in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention}, pas de grossièretés ici !")
                break

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))