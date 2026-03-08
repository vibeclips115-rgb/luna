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

# -------- CONFIG --------
LUNA_COOLDOWN = 10  # seconds per user


VERY_ANGRY_RESPONSES = [
    "Do NOT reply to me.",
    "Who said you could reply.",
    "That reply was a mistake.",
    "I did not ask for a reply.",
    "You’re bold for replying to me.",
    "Delete that. Now.",
    "Replying to me was your first mistake.",
    "I am not in the mood.",
    "You really thought that was okay?",
    "That was disrespectful.",
    "We are not doing this.",
    "You crossed a line.",
    "I said what I said.",
    "Do not reply to my messages.",
    "You’ve got some nerve.",
]


ANGRY_RESPONSES = [
    "Why are you pinging me.",
    "Do not tag me.",
    "You could’ve just said my name.",
    "I saw it. You didn’t need to ping.",
    "Relax. I’m not AFK.",
    "Yes?? No need to tag.",
    "Ping again and we’re beefing.",
    "That tag was unnecessary.",
    "You woke me up for THIS?",
    "I’m literally right here.",
    "Respectfully, don’t.",
    "You better have a reason for that ping.",
    "I felt that ping in my soul.",
    "That @ was aggressive.",
    "You didn’t have to do that.",
]

RESPONSES = [
    "👀 You called?",
    "Yeah? I’m right here.",
    "Hmm?",
    "What’s up?",
    "Present 🙋‍♀️",
    "Did someone say my name?",
    "I sensed my name…",
    "You rang? 🔔",
    "I was literally just chilling.",
    "At your service.",
    "Yes, mortal?",
    "I heard that.",
    "I’m listening 👂",
    "Bro I’m right here 😭",
    "You summoned me?",
    "Main character moment?",
    "That’s my name 👁️",
    "Say it again, I dare you.",
    "You talkin’ to me?",
    "I exist, confirmed.",
    "👁️👁️",
    "You weren’t supposed to say that…",
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
    "I was AFK, now I’m not.",
    "That’s me.",
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
    "Yes yes, I’m here.",
]

last_trigger = {}

@bot.command()
async def meow(ctx):
    # First response: confident meow
    await ctx.send("meow~ 🐱")

    # Small pause for comedic timing
    await asyncio.sleep(2)

    # Shy follow-up
    await ctx.send("…okay that was embarrassing 😳")

@bot.event
async def on_message(message):
    # 1️⃣ Ignore bots completely
    if message.author.bot:
        return

    content = message.content.lower().strip()
    now = time.time()
    user_id = message.author.id

    # 2️⃣ Commands work normally
    if content.startswith("$"):
        await bot.process_commands(message)
        return

    # 3️⃣ Check if this message is a REPLY to Luna
    replied_to_luna = False
    if message.reference and message.reference.resolved:
        replied_message = message.reference.resolved
        if replied_message.author.id == bot.user.id:
            replied_to_luna = True

    # 4️⃣ Check if Luna was TAGGED
    mentioned = bot.user in message.mentions

    # 5️⃣ Check if "luna" was said normally
    said_luna = (
        content == "luna"
        or content.startswith("luna ")
        or content.endswith(" luna")
        or " luna " in content
    )

    # 6️⃣ PRIORITY ORDER (VERY IMPORTANT)
    # Reply > Mention > Name

    # 😡 VERY ANGRY: replied to Luna
    if replied_to_luna:
        if now - last_trigger.get(user_id, 0) >= LUNA_COOLDOWN:
            last_trigger[user_id] = now

            async with message.channel.typing():
                await message.channel.send(
                    random.choice(VERY_ANGRY_RESPONSES)
                )

    # 😠 Angry: tagged Luna
    elif mentioned:
        if now - last_trigger.get(user_id, 0) >= LUNA_COOLDOWN:
            last_trigger[user_id] = now

            async with message.channel.typing():
                await message.channel.send(
                    random.choice(ANGRY_RESPONSES)
                )

    # 🙂 Normal: said "luna"
    elif said_luna:
        if now - last_trigger.get(user_id, 0) >= LUNA_COOLDOWN:
            last_trigger[user_id] = now

            async with message.channel.typing():
                await message.channel.send(
                    random.choice(RESPONSES)
                )

    # 7️⃣ Keep commands alive (EXACTLY ONCE)
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    # Ignore all bots (prevents loops & double replies)
    if message.author.bot:
        return

    content = message.content.lower().strip()

    # Let commands work normally
    if content.startswith("$"):
        await bot.process_commands(message)
        return

    # Smart "luna" detection
    triggered = (
        content == "luna"
        or content.startswith("luna ")
        or content.endswith(" luna")
        or " luna " in content
    )

    if triggered:
        now = time.time()
        user_id = message.author.id

        if now - last_trigger.get(user_id, 0) >= LUNA_COOLDOWN:
            last_trigger[user_id] = now

            async with message.channel.typing():
                await message.channel.send(
                    random.choice(RESPONSES)
                )

    # EXACTLY ONE command processor call
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    # 1️⃣ Ignore bots
    if message.author.bot:
        return

    content = message.content.lower().strip()

    # 2️⃣ Let commands work normally
    if content.startswith("$"):
        await bot.process_commands(message)
        return

    now = time.time()
    user_id = message.author.id

    # 3️⃣ Check if Luna was mentioned (tagged)
    mentioned = bot.user in message.mentions

    # 4️⃣ Smart "luna" text detection
    said_luna = (
        content == "luna"
        or content.startswith("luna ")
        or content.endswith(" luna")
        or " luna " in content
    )

    # 5️⃣ MENTION HAS PRIORITY (angry)
    if mentioned:
        if now - last_trigger.get(user_id, 0) >= LUNA_COOLDOWN:
            last_trigger[user_id] = now

            async with message.channel.typing():
                await message.channel.send(
                    random.choice(ANGRY_RESPONSES)
                )

    # 6️⃣ Normal name call (chill)
    elif said_luna:
        if now - last_trigger.get(user_id, 0) >= LUNA_COOLDOWN:
            last_trigger[user_id] = now

            async with message.channel.typing():
                await message.channel.send(
                    random.choice(RESPONSES)
                )

    # 7️⃣ Keep commands alive
    await bot.process_commands(message)
# ---------- GLOBAL ERROR HANDLER ----------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("❌ **You're not a moderator, dumbo.**")

    if isinstance(error, commands.BotMissingPermissions):
        return await ctx.send("⚠️ I don’t have the required permissions to do that.")

    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(
            f"⏳ Chill! Try again in **{error.retry_after:.1f}s**."
        )

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("❌ Missing required arguments.")

    if isinstance(error, commands.BadArgument):
        return await ctx.send("❌ Invalid argument provided.")

    if isinstance(error, commands.CommandNotFound):
        return  # ignore silently

    raise error  # raise unexpected errors for debugging

# ---------- READY ----------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ---------- LOAD COGS ----------
@bot.event
async def setup_hook():
    await bot.load_extension("cogs.utility")
    await bot.load_extension("cogs.gambling")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.welcomer")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.music")
    await bot.load_extension("cogs.fun")
    await bot.load_extension("cogs.automation")
    await bot.load_extension("cogs.ai")
    print("✅ Cogs loaded")

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))