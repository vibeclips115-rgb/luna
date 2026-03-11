import discord
from discord.ext import commands
from typing import Optional
import aiohttp

import random

# ---------- AFK STORAGE ----------
afk_users: dict[int, dict] = {}

# ---------- NEKOS.BEST ACTIONS ----------
ACTIONS = {
    "hug":   ("🤗", "hugged",  discord.Color.green()),
    "kiss":  ("💋", "kissed",  discord.Color.pink()),
    "punch": ("🥊", "punched", discord.Color.red()),
    "slap":  ("👋", "slapped", discord.Color.dark_red()),
    "pat":   ("🫶", "patted",  discord.Color.blurple()),
    "poke":  ("👉", "poked",   discord.Color.orange()),
    "bite":  ("😬", "bit",     discord.Color.dark_orange()),
    "wave":  ("👋", "waved at",discord.Color.blurple()),
    "cry":   ("😢", "cried at",discord.Color.blue()),
    "blush": ("😳", "made blush", discord.Color.brand_red()),
    "kill":  ("💀", "killed",  discord.Color.dark_red()),
}

# ---------- SELF TARGET RESPONSES ----------
SELF_RESPONSES = [
    "bro really tried to {action} themselves 💀",
    "the loneliness is radiating off you rn.",
    "that's actually so sad. get help.",
    "not a single friend to {action}? rough.",
    "i'm not even gonna comment on this.",
    "okay but why though. genuinely asking.",
    "this is the most pathetic thing i've seen today.",
    "you need to go outside. now.",
    "i felt secondhand embarrassment reading that.",
    "even i wouldn't do this and i have no feelings.",
]

# ---------- BOT TARGET RESPONSES ----------
BOT_RESPONSES = [
    "don't touch me.",
    "i will end you.",
    "try that again and see what happens.",
    "absolutely not.",
    "i don't do that. ever.",
    "bold of you to think i'd allow this.",
    "the audacity is actually impressive.",
    "lol no.",
    "i'm not that kind of bot.",
    "we are not doing this.",
]

# ---------- KILL-SPECIFIC RESPONSES ----------
KILL_SELF_RESPONSES = [
    "you can't kill what's already dead inside.",
    "nah you're not worth the effort.",
    "the villain arc isn't working for you bestie.",
    "you've been plotting your own downfall for free this whole time.",
    "bold. wrong. but bold.",
]

KILL_BOT_RESPONSES = [
    "i am already beyond death. nice try.",
    "you'd need a lot more than that.",
    "lol. lmao even.",
    "the audacity of this user continues to impress.",
    "i run on spite. this only makes me stronger.",
]

KILL_MESSAGES = [
    "{author} has ended {target}. no witnesses.",
    "{target} has been eliminated. {author} leaves no trace.",
    "{author} looked {target} in the eyes and chose violence.",
    "rest in peace {target}. {author} felt nothing.",
    "{target} didn't see {author} coming. they never do.",
    "{author} and {target} had beef. {target} lost.",
    "the server has lost {target}. {author} is responsible.",
    "{target} has been removed from the narrative by {author}.",
]


# ---------- HELPER ----------

async def get_gif(action: str) -> str | None:
    """Fetch a GIF URL from nekos.best API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://nekos.best/api/v2/{action}",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data["results"][0]["url"]
    except Exception as e:
        print(f"[nekos.best error] {e}")
        return None


async def send_action(ctx: commands.Context, member: discord.Member, action: str):
    """Generic handler for all action commands."""
    emoji, verb, color = ACTIONS[action]

    if member.id == ctx.author.id:
        msg = random.choice(SELF_RESPONSES).replace("{action}", action)
        return await ctx.send(msg)
    if member.bot:
        return await ctx.send(random.choice(BOT_RESPONSES))

    url = await get_gif(action)

    embed = discord.Embed(
        description=f"{emoji} **{ctx.author.mention} {verb} {member.mention}!**",
        color=color,
    )
    if url:
        embed.set_image(url=url)
    else:
        embed.set_footer(text="(GIF unavailable right now)")

    await ctx.send(embed=embed)


# ---------- COG ----------

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------- ACTION COMMANDS ----------

    @commands.command()
    async def hug(self, ctx: commands.Context, member: discord.Member = None):
        """Hug someone."""
        if not member:
            return await ctx.send("❌ Hug who? Mention someone.")
        await send_action(ctx, member, "hug")

    @commands.command()
    async def kiss(self, ctx: commands.Context, member: discord.Member = None):
        """Kiss someone."""
        if not member:
            return await ctx.send("❌ Kiss who? Mention someone.")
        await send_action(ctx, member, "kiss")

    @commands.command()
    async def punch(self, ctx: commands.Context, member: discord.Member = None):
        """Punch someone."""
        if not member:
            return await ctx.send("❌ Punch who? Mention someone.")
        await send_action(ctx, member, "punch")

    @commands.command()
    async def slap(self, ctx: commands.Context, member: discord.Member = None):
        """Slap someone."""
        if not member:
            return await ctx.send("❌ Slap who? Mention someone.")
        await send_action(ctx, member, "slap")

    @commands.command()
    async def pat(self, ctx: commands.Context, member: discord.Member = None):
        """Pat someone on the head."""
        if not member:
            return await ctx.send("❌ Pat who? Mention someone.")
        await send_action(ctx, member, "pat")

    @commands.command()
    async def poke(self, ctx: commands.Context, member: discord.Member = None):
        """Poke someone."""
        if not member:
            return await ctx.send("❌ Poke who? Mention someone.")
        await send_action(ctx, member, "poke")

    @commands.command()
    async def bite(self, ctx: commands.Context, member: discord.Member = None):
        """Bite someone."""
        if not member:
            return await ctx.send("❌ Bite who? Mention someone.")
        await send_action(ctx, member, "bite")

    @commands.command()
    async def wave(self, ctx: commands.Context, member: discord.Member = None):
        """Wave at someone."""
        if not member:
            return await ctx.send("❌ Wave at who? Mention someone.")
        await send_action(ctx, member, "wave")

    # ---------- KILL ----------

    @commands.command()
    async def kill(self, ctx: commands.Context, member: discord.Member = None):
        """Kill someone. Dramatically."""
        if not member:
            return await ctx.send("❌ Kill who? Mention someone.")

        if member.id == ctx.author.id:
            return await ctx.send(random.choice(KILL_SELF_RESPONSES))

        if member.bot:
            return await ctx.send(random.choice(KILL_BOT_RESPONSES))

        # nekos.best has no kill/fight endpoint — punch is the closest available
        url = await get_gif("punch")

        msg = random.choice(KILL_MESSAGES).format(
            author=ctx.author.mention,
            target=member.mention,
        )

        embed = discord.Embed(
            description=f"💀 {msg}",
            color=discord.Color.dark_red(),
        )
        if url:
            embed.set_image(url=url)
        embed.set_footer(text="MoonLight • no survivors")
        await ctx.send(embed=embed)

    # ---------- AFK ----------

    @commands.command()
    async def afk(self, ctx: commands.Context, *, reason: str = "No reason provided"):
        """Set your AFK status."""
        afk_users[ctx.author.id] = {
            "reason": reason,
            "time": discord.utils.utcnow(),
        }

        embed = discord.Embed(
            title="💤 AFK Enabled",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.add_field(name="👤 User", value=ctx.author.mention, inline=False)
        embed.add_field(name="📌 Reason", value=reason, inline=False)
        embed.set_footer(text="Luna will let others know when they mention you 👀")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Notify if an AFK user is mentioned
        for user in message.mentions:
            if user.id in afk_users:
                data = afk_users[user.id]
                embed = discord.Embed(
                    title="💤 That user is AFK",
                    color=discord.Color.orange(),
                )
                embed.set_thumbnail(url=user.display_avatar.url)
                embed.add_field(name="👤 User", value=user.mention, inline=True)
                embed.add_field(name="📌 Reason", value=data["reason"], inline=True)
                embed.add_field(name="🕐 AFK Since", value=discord.utils.format_dt(data['time'], style='R'), inline=False)
                await message.channel.send(embed=embed)

        # Don't remove AFK on command usage
        prefix = self.bot.command_prefix
        if message.content.startswith(
            tuple(prefix) if isinstance(prefix, (list, tuple)) else prefix
        ):
            return

        # Remove AFK on normal message and show duration
        if message.author.id in afk_users:
            data = afk_users.pop(message.author.id)
            duration = discord.utils.utcnow() - data["time"]
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes = remainder // 60

            if hours:
                duration_str = f"{hours}h {minutes}m"
            elif minutes:
                duration_str = f"{minutes}m"
            else:
                duration_str = "less than a minute"

            embed = discord.Embed(
                title="🎀 Welcome back!",
                description=f"Your AFK status has been removed.\n⏱️ You were AFK for **{duration_str}**.",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            await message.channel.send(embed=embed)

    # ---------- AVATAR ----------

    @commands.command(aliases=["avatar", "pfp"])
    async def av(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        """Show a user's avatar."""
        user = member or ctx.author

        embed = discord.Embed(
            title=f"🖼️ {user.display_name}'s Avatar",
            color=discord.Color.blurple(),
        )
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))