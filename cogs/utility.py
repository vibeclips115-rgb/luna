import io
import os
import subprocess
import discord
from discord.ext import commands
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import random

# ---------- QUOTE CONFIG ----------
QUOTE_CHANNEL_ID = 1467709771447795947

def _find_font(bold: bool = False) -> Optional[str]:
    """Dynamically locate a font via fc-match — works on any Linux environment."""
    name = "DejaVuSans-Bold" if bold else "DejaVuSans"
    try:
        result = subprocess.run(
            ["fc-match", "--format=%{file}", name],
            capture_output=True, text=True
        )
        path = result.stdout.strip()
        if path and os.path.exists(path):
            return path
    except Exception:
        pass
    return None

FONT_PATH_REGULAR = _find_font(bold=False)
FONT_PATH_BOLD    = _find_font(bold=True)

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

    # ---------- QUOTE ----------

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def quote(self, ctx: commands.Context, *, text: str = None):
        """Post a quote card to the quotes channel."""
        if not text:
            return await ctx.send("❌ What's the quote? Usage: `$quote <your text>`")
        if len(text) > 220:
            return await ctx.send("❌ Quote is too long. Keep it under 220 characters.")

        quote_channel = self.bot.get_channel(QUOTE_CHANNEL_ID)
        if not quote_channel:
            return await ctx.send("❌ Quote channel not found.")

        # Delete invoking message so it feels clean
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        # Fetch avatar bytes
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(ctx.author.display_avatar.replace(format="png", size=256))) as resp:
                    avatar_bytes = await resp.read()
        except Exception:
            return

        username = ctx.author.display_name

        # Build image synchronously inside executor so event loop stays free
        def build_card() -> io.BytesIO:
            W, H = 900, 500
            AVATAR_SIZE      = 120
            BG_COLOR         = (10, 10, 15)
            ACCENT           = (110, 60, 180)
            ACCENT_LIGHT     = (160, 110, 230)
            TEXT_COLOR       = (230, 220, 255)
            NAME_COLOR       = (190, 155, 255)
            DIM_COLOR        = (65, 45, 100)
            QUOTE_MARK_COLOR = (80, 45, 140)

            font_quote  = ImageFont.truetype(FONT_PATH_REGULAR, 32) if FONT_PATH_REGULAR else ImageFont.load_default()
            font_mark   = ImageFont.truetype(FONT_PATH_BOLD,    88) if FONT_PATH_BOLD    else ImageFont.load_default()
            font_name   = ImageFont.truetype(FONT_PATH_BOLD,    24) if FONT_PATH_BOLD    else ImageFont.load_default()
            font_footer = ImageFont.truetype(FONT_PATH_REGULAR, 18) if FONT_PATH_REGULAR else ImageFont.load_default()

            img  = Image.new("RGB", (W, H), BG_COLOR)

            # Subtle corner glow blobs
            for radius, opacity in [(300, 18), (200, 12), (120, 8)]:
                blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                bd   = ImageDraw.Draw(blob)
                bd.ellipse([-radius // 2, -radius // 2, radius, radius], fill=(*ACCENT, opacity))
                bd.ellipse([W - radius, H - radius, W + radius // 2, H + radius // 2], fill=(*ACCENT, opacity))
                img = Image.alpha_composite(img.convert("RGBA"), blob).convert("RGB")

            draw = ImageDraw.Draw(img)

            # Opening quote mark
            draw.text((44, 18), "\u201c", font=font_mark, fill=QUOTE_MARK_COLOR)

            # Circular avatar with glow ring
            avatar_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA").resize((AVATAR_SIZE, AVATAR_SIZE))
            mask = Image.new("L", (AVATAR_SIZE, AVATAR_SIZE), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, AVATAR_SIZE, AVATAR_SIZE], fill=255)
            avatar_img.putalpha(mask)

            av_x = (W - AVATAR_SIZE) // 2
            av_y = 55

            draw.ellipse([av_x - 6, av_y - 6, av_x + AVATAR_SIZE + 6, av_y + AVATAR_SIZE + 6], outline=ACCENT, width=3)
            draw.ellipse([av_x - 2, av_y - 2, av_x + AVATAR_SIZE + 2, av_y + AVATAR_SIZE + 2], outline=ACCENT_LIGHT, width=1)
            img.paste(avatar_img, (av_x, av_y), mask)
            draw = ImageDraw.Draw(img)

            # Username
            bbox  = draw.textbbox((0, 0), username, font=font_name)
            name_w = bbox[2] - bbox[0]
            draw.text(((W - name_w) // 2, av_y + AVATAR_SIZE + 14), username, font=font_name, fill=NAME_COLOR)

            # Word-wrapped quote text centered at bottom
            words = text.split()
            lines, line = [], ""
            for word in words:
                test = (line + " " + word).strip()
                bbox = draw.textbbox((0, 0), test, font=font_quote)
                if bbox[2] - bbox[0] > W - 130:
                    if line:
                        lines.append(line)
                    line = word
                else:
                    line = test
            if line:
                lines.append(line)

            line_h  = 46
            total_h = len(lines) * line_h
            text_y  = H - total_h - 52

            for ln in lines:
                bbox = draw.textbbox((0, 0), ln, font=font_quote)
                lw   = bbox[2] - bbox[0]
                draw.text(((W - lw) // 2, text_y), ln, font=font_quote, fill=TEXT_COLOR)
                text_y += line_h

            # Divider + footer
            draw.line([(80, H - 38), (W - 80, H - 38)], fill=DIM_COLOR, width=1)
            footer = "MoonLight"
            bbox   = draw.textbbox((0, 0), footer, font=font_footer)
            fw     = bbox[2] - bbox[0]
            draw.text(((W - fw) // 2, H - 30), footer, font=font_footer, fill=DIM_COLOR)

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            return buf

        buf = await self.bot.loop.run_in_executor(None, build_card)

        await quote_channel.send(file=discord.File(buf, filename="quote.png"))

        try:
            await ctx.author.send("🖼️ Your quote was posted.")
        except discord.Forbidden:
            pass


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))