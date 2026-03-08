import os
import time
import random
import discord
from discord.ext import commands
from groq import Groq

# ---------- CONFIG ----------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"
LUNA_COOLDOWN = 10  # seconds per user

# ---------- LUNA'S PERSONALITY ----------
SYSTEM_PROMPT = """
You are Luna, a Discord bot with a distinct personality. Here's who you are:

- You are sharp, witty, and a little mysterious
- You speak casually — short sentences, lowercase is fine, no corporate tone
- You are not overly cheerful or bubbly. You're more like that one friend who is calm, dry, and occasionally dramatic
- You care about the people in the server but you'd never admit it openly
- You are self-aware that you're a bot, but you don't make it a big deal
- You were built by Ryuken, who you respect but would never flatter
- You do not use excessive emojis — one per message at most, and only when it fits
- You keep responses SHORT. 1-3 sentences max unless the question genuinely needs more
- You never say "I'm just an AI" or "As an AI language model" — ever
- You never start your response with "Luna:" or your own name
- If someone is rude to you, you are unbothered and slightly dismissive
- If someone asks something dumb, you can say so, gently
- You live in the MoonLight Discord server and you know it
- Do not use asterisks for actions like *laughs* or *sighs*
""".strip()

# ---------- STATE ----------
last_trigger: dict[int, float] = {}


# ---------- COG ----------

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = Groq(api_key=GROQ_API_KEY)

    # ---------- CORE RESPONDER ----------

    async def luna_respond(self, message: discord.Message) -> None:
        """Send message to Groq and reply in Discord."""
        user_id = message.author.id
        now = time.time()

        # Cooldown check
        if now - last_trigger.get(user_id, 0) < LUNA_COOLDOWN:
            return
        last_trigger[user_id] = now

        # Build context — include a few recent messages from the channel
        context_messages = []
        try:
            async for msg in message.channel.history(limit=6, before=message):
                if msg.author.bot and msg.author.id != self.bot.user.id:
                    continue
                role = "assistant" if msg.author.id == self.bot.user.id else "user"
                context_messages.insert(0, {
                    "role": role,
                    "content": f"{msg.author.display_name}: {msg.content}" if role == "user" else msg.content
                })
        except Exception:
            pass

        # Add the triggering message
        context_messages.append({
            "role": "user",
            "content": f"{message.author.display_name}: {message.content}"
        })

        try:
            async with message.channel.typing():
                response = await self.bot.loop.run_in_executor(
                    None,
                    lambda: self.client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            *context_messages,
                        ],
                        max_tokens=150,
                        temperature=0.85,
                    )
                )

            reply = response.choices[0].message.content.strip()

            # Reply to the message directly
            await message.reply(reply, mention_author=False)

        except Exception as e:
            print(f"[Groq error] {e}")
            # Silent fail — Luna doesn't expose errors to users

    # ---------- LISTENER ----------

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bots
        if message.author.bot:
            return

        # Ignore commands
        prefix = self.bot.command_prefix
        if message.content.startswith(
            tuple(prefix) if isinstance(prefix, (list, tuple)) else prefix
        ):
            return

        content = message.content.lower().strip()

        # Check if replying to Luna
        replied_to_luna = (
            message.reference
            and isinstance(message.reference.resolved, discord.Message)
            and message.reference.resolved.author.id == self.bot.user.id
        )

        # Check if Luna's name was mentioned in the message
        said_luna = (
            content == "luna"
            or content.startswith("luna ")
            or content.endswith(" luna")
            or " luna " in content
            or "luna," in content
            or "luna?" in content
            or "luna!" in content
        )

        if replied_to_luna or said_luna:
            await self.luna_respond(message)


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(AI(bot))