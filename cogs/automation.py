import random
import discord
from discord.ext import commands, tasks

FUN_FACTS = [
    "🌙 The Moon drifts away from Earth by ~3.8 cm every year.",
    "🧠 Your brain burns ~20% of your body’s energy.",
    "🌌 There are more stars in the universe than grains of sand on Earth.",
    "🌓 Moonlight is actually reflected sunlight.",
    "💤 The brain stays active even while sleeping.",
    "☄️ Some meteors are older than Earth itself.",
    "✨ Coding late at night hits different.",
    "🌙 Luna is always watching. Always."
]

class AutoMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_fun_fact.start()  # 🔥 start loop

    def cog_unload(self):
        self.send_fun_fact.cancel()

    @tasks.loop(minutes=30)
    async def send_fun_fact(self):
        channel_id = 1463136856374906887  
        channel = self.bot.get_channel(channel_id)
        if random.randint(1, 100) == 1:
         message = "👁️ Luna has been awake for too long."
        if not channel:
            return

        embed = discord.Embed(
            title="🌙 Luna Says",
            description=random.choice(FUN_FACTS),
            color=discord.Color.blurple()
        )

        embed.set_footer(text="MoonLight • Automated wisdom ✨")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await channel.send(embed=embed)

    @send_fun_fact.before_loop
    async def before_send(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AutoMessage(bot))