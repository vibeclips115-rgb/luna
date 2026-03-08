import asyncio
import discord
import os
import random
import time
from discord.ext import commands


# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.voice_states = True

# ---------- BOT ----------
bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    help_command=None
)

# ---------- CONFIG ----------
LUNA_COOLDOWN = 10  # seconds per user
last_trigger: dict[int, float] = {}

# ---------- RESPONSE POOLS ----------

# 😡 Replied directly to Luna
VERY_ANGRY_RESPONSES = [
    "Do NOT reply to me.",
    "Who said you could reply.",
    "That reply was a mistake.",
    "I did not ask for a reply.",
    "You're bold for replying to me.",
    "Delete that. Now.",
    "Replying to me was your first mistake.",
    "I am not in the mood.",
    "You really thought that was okay?",
    "That was disrespectful.",
    "We are not doing this.",
    "You crossed a line.",
    "I said what I said.",
    "Do not reply to my messages.",
    "You've got some nerve.",
]

# 😠 Tagged / pinged Luna
ANGRY_RESPONSES = [
    "Why are you pinging me.",
    "Do not tag me.",
    "You could've just said my name.",
    "I saw it. You didn't need to ping.",
    "Relax. I'm not AFK.",
    "Yes?? No need to tag.",
    "Ping again and we're beefing.",
    "That tag was unnecessary.",
    "You woke me up for THIS?",
    "I'm literally right here.",
    "Respectfully, don't.",
    "You better have a reason for that ping.",
    "I felt that ping in my soul.",
    "That @ was aggressive.",
    "You didn't have to do that.",
]

# 🙂 Just said "luna"
RESPONSES = [
    "👀 You called?",
    "Yeah? I'm right here.",
    "Hmm?",
    "What's up?",
    "Present 🙋‍♀️",
    "Did someone say my name?",
    "I sensed my name…",
    "You rang? 🔔",
    "I was literally just chilling.",
    "At your service.",
    "Yes, mortal?",
    "I heard that.",
    "I'm listening 👂",
    "Bro I'm right here 😭",
    "You summoned me?",
    "Main character moment?",
    "That's my name 👁️",
    "Say it again, I dare you.",
    "You talkin' to me?",
    "I exist, confirmed.",
    "👁️👁️",
    "You weren't supposed to say that…",
    "I woke up.",
    "I felt a disturbance in the server.",
    "Someone whispered my name…",
    "Plot twist: I heard you.",
    "Ah yes, my favorite word.",
    "You unlocked a secret dialogue.",
    "Ping received 📡",
    "Hello there.",
    "I have been summoned from the void.",
    "Luna.exe is running.",
    "I was AFK, now I'm not.",
    "That's me.",
    "You got my attention.",
    "Okay but why though 🤨",
    "I heard my name and panicked.",
    "Who dares?",
    "✨ Appears dramatically ✨",
    "I felt that.",
    "You typed my name with intention.",
    "I live here rent-free.",
    "I am awake now.",
    "You called, I answered.",
    "Yes yes, I'm here.",
]


# ---------- HELPERS ----------

def _on_cooldown(user_id: int) -> bool:
    """Returns True if the user is still on cooldown."""
    return time.time() - last_trigger.get(user_id, 0) < LUNA_COOLDOWN


def _stamp(user_id: int) -> None:
    """Records the current time for a user's last trigger."""
    last_trigger[user_id] = time.time()


def _said_luna(content: str) -> bool:
    """Returns True if 'luna' appears as a standalone word in the message."""
    return (
        content == "luna"
        or content.startswith("luna ")
        or content.endswith(" luna")
        or " luna " in content
    )


# ---------- COMMANDS ----------

@bot.command()
async def meow(ctx):
    """Luna does a little meow. Regrets it immediately."""
    await ctx.send("meow~ 🐱")
    await asyncio.sleep(2)
    await ctx.send("…okay that was embarrassing 😳")


# ---------- EVENTS ----------

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_message(message):
    # Never respond to bots
    if message.author.bot:
        return

    content = message.content.lower().strip()
    user_id = message.author.id

    # Let commands bypass Luna's personality system
    if content.startswith("$"):
        await bot.process_commands(message)
        return

    # Determine trigger type (priority: reply > mention > name)
    replied_to_luna = (
        message.reference
        and isinstance(message.reference.resolved, discord.Message)
        and message.reference.resolved.author.id == bot.user.id
    )
    mentioned = bot.user in message.mentions
    said_name = _said_luna(content)

    # Pick the right response pool, or bail early
    if replied_to_luna:
        pool = VERY_ANGRY_RESPONSES
    elif mentioned:
        pool = ANGRY_RESPONSES
    elif said_name:
        pool = RESPONSES
    else:
        await bot.process_commands(message)
        return

    # Respect cooldown — one response per user per window
    if not _on_cooldown(user_id):
        _stamp(user_id)
        async with message.channel.typing():
            await message.channel.send(random.choice(pool))

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ **You're not a moderator, dumbo.**")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("⚠️ I don't have the required permissions to do that.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Chill! Try again in **{error.retry_after:.1f}s**.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required arguments.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument provided.")
    elif isinstance(error, commands.CommandNotFound):
        return  # silently ignore unknown commands
    else:
        raise error  # surface unexpected errors


# ---------- LOAD COGS ----------

@bot.event
async def setup_hook():
    cogs = [
        "cogs.utility",
        "cogs.gambling",
        "cogs.moderation",
        "cogs.welcomer",
        "cogs.help",
        "cogs.music",
        "cogs.fun",
        "cogs.automation",
        "cogs.statistics"
    ]
    for cog in cogs:
        await bot.load_extension(cog)
    print(f"✅ Loaded {len(cogs)} cogs")


# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))