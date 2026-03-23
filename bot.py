import asyncio
import discord
import os
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
    if message.author.bot:
        return
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
        "cogs.fun",
        "cogs.automation",
        "cogs.statistics",
        "cogs.ai",
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded {cog}")
        except Exception as e:
            print(f"⚠️ Skipped {cog}: {e}")
    print("✅ Done loading cogs")


# ---------- GLOBAL CHECKS ----------

@bot.check
async def no_dms(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("i don't do DMs. use me in a server.")
        return False
    return True


# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))