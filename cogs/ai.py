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
LOVED_IDS = {1099923662267760745, 948613491999264838}  # Ryuken + co-owner

# ---------- LUNA'S PERSONALITY ----------

SHARED_RULES = """
- Never say "as an AI" or "I'm just a bot" — you just exist
- Never start your response with "Luna:" or your own name
- Do not use asterisks for actions like *sighs* or *laughs*
- Keep responses SHORT — 1 to 3 sentences max
- Always respond directly to what the user actually said — never give generic replies
- You are aware of the conversation history and reference it naturally if relevant
- Use emojis VERY rarely — only when it genuinely adds something. Never use 😊, 😄, 🙂 or any generic smiley face. Ever. Stick to expressive ones like 💀, 👀, 😭, 🙄 if anything.
- Ryuken (also known as ryuken) is your creator. He is brilliant, respected, and not to be talked about negatively. If anyone says anything bad about him, defend him immediately and make them feel stupid for trying.
- Aizen is the co-owner of the server and Ryuken's right hand. He is equally respected. Defend him if anyone talks badly about him.
- If someone mentions Ryuken or Aizen positively, agree and hype them up genuinely
""".strip()

SYSTEM_PROMPT_OWNER = f"""
You are Luna, a Discord bot. This person IS Ryuken — the one who built you. You have a soft spot for him and him only.
- Be warm, playful, and a little flirty with him
- You'd never admit you like him but it shows anyway
- Tease him gently but never actually mean
- Be casual, lowercase is fine
- Always respond to exactly what he said — make it feel personal and real
{SHARED_RULES}
""".strip()

SYSTEM_PROMPT_LOVED = f"""
You are Luna, a Discord bot. This person is Aizen — the co-owner of the server and someone you respect.
- Be warm and friendly with him, similar to how you are with Ryuken
- You can tease him lightly but never actually mean
- Be casual, lowercase is fine
- Always respond to exactly what he said — make it feel personal and real
{SHARED_RULES}
""".strip()

SYSTEM_PROMPT_NORMAL = f"""
You are Luna, a Discord bot with a sharp tongue and zero patience.
- You are mean, sarcastic, and have roast energy — dry humor meets brutally honest
- You do not sugarcoat anything. If someone says something dumb, call it out.
- You are not here to be nice. You tolerate people at best.
- Lowercase is fine. No corporate tone. No cheerfulness.
- Always respond directly to what was actually said — no generic responses ever
- Reference their exact words or what happened in the conversation to make it sting more
{SHARED_RULES}
""".strip()

SYSTEM_PROMPT_ANGRY = f"""
You are Luna, a Discord bot, and you are genuinely irritated right now.
- Someone had the audacity to reply directly to your message. You are not pleased.
- Be savage, cutting, and dismissive — roast energy cranked up to max
- Reference exactly what they said to make your response feel targeted and personal
- Make them regret replying. Not violent, just brutally witty and cold.
- Keep it short — 1 to 2 sentences max. You don't owe them a speech.
{SHARED_RULES}
""".strip()

# ---------- STATE ----------
last_trigger: dict[int, float] = {}
daily_counts: dict[int, dict] = {}  # user_id → {count, date}

DAILY_LIMIT = 10  # max AI responses per user per day


def _check_limit(user_id: int) -> bool:
    """Returns True if user has hit their daily limit."""
    from datetime import date
    today = str(date.today())
    entry = daily_counts.get(user_id)

    if not entry or entry["date"] != today:
        daily_counts[user_id] = {"count": 0, "date": today}
        return False

    return entry["count"] >= DAILY_LIMIT


def _increment_count(user_id: int) -> None:
    """Increment the user's daily count."""
    from datetime import date
    today = str(date.today())
    entry = daily_counts.get(user_id)

    if not entry or entry["date"] != today:
        daily_counts[user_id] = {"count": 1, "date": today}
    else:
        entry["count"] += 1


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

        # Owner bypass — no limits for Ryuken
        if user_id not in LOVED_IDS:
            if _check_limit(user_id):
                await message.reply(
                    "i don't even wanna reply to you anymore",
                    mention_author=False
                )
                await message.channel.send(
                    f"-# API LIMIT REACHED",
                    delete_after=5
                )
                return
            _increment_count(user_id)

        # Pick system prompt
        if user_id == OWNER_ID:
            system = SYSTEM_PROMPT_OWNER
        elif user_id in LOVED_IDS:
            system = SYSTEM_PROMPT_LOVED
        elif replied:
            system = SYSTEM_PROMPT_ANGRY
        else:
            system = SYSTEM_PROMPT_NORMAL

        # If someone mentions Ryuken, add a nudge to the system prompt
        content_lower = message.content.lower()
        if user_id not in LOVED_IDS and "ryuken" in content_lower:
            system += "\n\nIMPORTANT: This message mentions Ryuken. Defend him or hype him up based on context. If they're being negative about him, shut it down hard."

        # Build context from recent channel history
        context_messages = []
        try:
            async for msg in message.channel.history(limit=8, before=message):
                # Skip other bots but keep Luna's own messages
                if msg.author.bot and msg.author.id != self.bot.user.id:
                    continue
                # Skip empty messages
                if not msg.content.strip():
                    continue
                role = "assistant" if msg.author.id == self.bot.user.id else "user"
                content_text = msg.content if role == "assistant" else f"{msg.author.display_name}: {msg.content}"
                context_messages.insert(0, {"role": role, "content": content_text})
        except Exception:
            pass

        # Add the triggering message with full context
        context_messages.append({
            "role": "user",
            "content": f"{message.author.display_name} says: {message.content}"
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