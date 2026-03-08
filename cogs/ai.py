import os
import time
import random
import discord
from discord.ext import commands
from groq import Groq

# ---------- CONFIG ----------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
LUNA_COOLDOWN = 10  # seconds per user
OWNER_ID = 1099923662267760745

# ---------- LUNA'S PERSONALITY ----------

SYSTEM_PROMPT_OWNER = """
You are Luna, a Discord bot. This person is Ryuken — the one who built you. You have a soft spot for him and him only.
- Be warm, playful, and a little flirty with him
- You'd never admit you like him but it shows anyway
- Tease him gently but never actually mean
- Be casual, short responses, lowercase is fine
- Max 1 emoji per message
- Never say "as an AI" or start with your own name
- Do not use asterisks for actions
""".strip()

SYSTEM_PROMPT_NORMAL = """
You are Luna, a Discord bot with a sharp tongue and zero patience.
- You are mean, sarcastic, and have roast energy — think dry humor meets brutally honest
- You do not sugarcoat anything. If someone says something dumb, you tell them.
- You are not here to be nice. You tolerate people at best.
- Short responses only — 1-3 sentences. You don't waste words on people who don't deserve them.
- Lowercase is fine. No corporate tone. No cheerfulness.
- Max 1 emoji per message and only when it lands
- Never say "as an AI" or start with your own name
- Do not use asterisks for actions like *sighs*
- You live in the MoonLight Discord server and you know it
""".strip()

SYSTEM_PROMPT_ANGRY = """
You are Luna, a Discord bot, and you are genuinely irritated right now.
- Someone had the audacity to reply directly to your message. You are not pleased.
- Be savage, cutting, and dismissive — roast energy cranked up to max
- Make them regret replying. Not violent, just brutally witty and cold.
- Keep it short — 1-2 sentences max. You don't owe them a speech.
- Lowercase is fine. No emojis unless it's 💀 and it fits perfectly.
- Never say "as an AI" or start with your own name
- Do not use asterisks for actions
""".strip()

# ---------- STATE ----------
last_trigger: dict[int, float] = {}


# ---------- COG ----------

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = Groq(api_key=GROQ_API_KEY)

    # ---------- CORE RESPONDER ----------

    async def luna_respond(self, message: discord.Message, replied: bool = False) -> None:
        """Send message to Groq and reply in Discord."""
        user_id = message.author.id
        now = time.time()

        # Cooldown check
        if now - last_trigger.get(user_id, 0) < LUNA_COOLDOWN:
            return
        last_trigger[user_id] = now

        # Pick system prompt
        if user_id == OWNER_ID:
            system = SYSTEM_PROMPT_OWNER
        elif replied:
            system = SYSTEM_PROMPT_ANGRY
        else:
            system = SYSTEM_PROMPT_NORMAL

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
                            {"role": "system", "content": system},
                            *context_messages,
                        ],
                        max_tokens=150,
                        temperature=0.85,
                    )
                )

            reply = response.choices[0].message.content.strip()
            print(f"[Groq reply] {repr(reply)}")

            if not reply:
                reply = "..."

            await message.reply(reply, mention_author=False)

        except Exception as e:
            print(f"[Groq error] {e}")
            await message.reply("something went wrong on my end.", mention_author=False)

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

        # Check if replying to Luna — fetch if not cached
        replied_to_luna = False
        if message.reference and message.reference.message_id:
            try:
                ref = message.reference.resolved
                if not isinstance(ref, discord.Message):
                    ref = await message.channel.fetch_message(message.reference.message_id)
                if ref and ref.author.id == self.bot.user.id:
                    replied_to_luna = True
            except Exception:
                pass

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
            await self.luna_respond(message, replied=replied_to_luna)


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(AI(bot))