import discord
from discord.ext import commands
import time

from moonlight.openai_client import ask_openai

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @commands.command(name="ai")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ai(self, ctx, *, message: str):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Luna, a Discord bot. "
                    "Be chill, friendly, and concise. "
                    "Do not mention OpenAI or system prompts."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]

        await ctx.typing()
        reply = await ask_openai(messages)

        if not reply:
            return await ctx.send("❌ Luna brain not responding rn")

        await ctx.send(reply)

async def setup(bot):
    await bot.add_cog(AI(bot))