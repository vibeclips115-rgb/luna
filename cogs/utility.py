import io
import discord
from discord.ext import commands
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import random

# ---------- QUOTE CONFIG ----------
QUOTE_CHANNEL_ID = 1467709771447795947

# ---------- AFK STORAGE ----------
afk_users: dict[int, dict] = {}

# ---------- NEKOS.BEST ACTIONS ----------
ACTIONS = {
    "hug":   ("🤗", "hugged",     discord.Color.green()),
    "kiss":  ("💋", "kissed",     discord.Color.pink()),
    "punch": ("🥊", "punched",    discord.Color.red()),
    "slap":  ("👋", "slapped",    discord.Color.dark_red()),
    "pat":   ("🫶", "patted",     discord.Color.blurple()),
    "poke":  ("👉", "poked",      discord.Color.orange()),
    "bite":  ("😬", "bit",        discord.Color.dark_orange()),
    "wave":  ("👋", "waved at",   discord.Color.blurple()),
    "cry":   ("😢", "cried at",   discord.Color.blue()),
    "blush": ("😳", "made blush", discord.Color.brand_red()),
    "kill":  ("💀", "killed",     discord.Color.dark_red()),
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
        if not member:
            return await ctx.send("❌ Hug who? Mention someone.")
        await send_action(ctx, member, "hug")

    @commands.command()
    async def kiss(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Kiss who? Mention someone.")
        await send_action(ctx, member, "kiss")

    @commands.command()
    async def punch(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Punch who? Mention someone.")
        await send_action(ctx, member, "punch")

    @commands.command()
    async def slap(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Slap who? Mention someone.")
        await send_action(ctx, member, "slap")

    @commands.command()
    async def pat(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Pat who? Mention someone.")
        await send_action(ctx, member, "pat")

    @commands.command()
    async def poke(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Poke who? Mention someone.")
        await send_action(ctx, member, "poke")

    @commands.command()
    async def bite(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Bite who? Mention someone.")
        await send_action(ctx, member, "bite")

    @commands.command()
    async def wave(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Wave at who? Mention someone.")
        await send_action(ctx, member, "wave")

    # ---------- KILL ----------

    @commands.command()
    async def kill(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            return await ctx.send("❌ Kill who? Mention someone.")

        if member.id == ctx.author.id:
            return await ctx.send(random.choice(KILL_SELF_RESPONSES))
        if member.bot:
            return await ctx.send(random.choice(KILL_BOT_RESPONSES))

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
        afk_users[ctx.author.id] = {
            "reason": reason,
            "time": discord.utils.utcnow(),
        }

        embed = discord.Embed(title="💤 AFK Enabled", color=discord.Color.blurple())
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.add_field(name="👤 User", value=ctx.author.mention, inline=False)
        embed.add_field(name="📌 Reason", value=reason, inline=False)
        embed.set_footer(text="Luna will let others know when they mention you 👀")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        for user in message.mentions:
            if user.id in afk_users:
                data = afk_users[user.id]
                embed = discord.Embed(title="💤 That user is AFK", color=discord.Color.orange())
                embed.set_thumbnail(url=user.display_avatar.url)
                embed.add_field(name="👤 User", value=user.mention, inline=True)
                embed.add_field(name="📌 Reason", value=data["reason"], inline=True)
                embed.add_field(name="🕐 AFK Since", value=discord.utils.format_dt(data['time'], style='R'), inline=False)
                await message.channel.send(embed=embed)

        prefix = self.bot.command_prefix
        if message.content.startswith(
            tuple(prefix) if isinstance(prefix, (list, tuple)) else prefix
        ):
            return

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
        """Post a quote card.
        Usage:
          $quote <text>               → quotes yourself
          $quote @user <text>         → quotes another user
          $quote (reply to message)   → quotes the replied message & its author
        """
        quote_channel = self.bot.get_channel(QUOTE_CHANNEL_ID)
        if not quote_channel:
            return await ctx.send("❌ Quote channel not found.")

        target = ctx.author
        quote_text = None

        # ── CASE 1: Reply-based quote ($quote with no args, replying to a message) ──
        if ctx.message.reference and not text:
            try:
                ref_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                target = ref_msg.author
                quote_text = ref_msg.content.strip()
            except Exception:
                return await ctx.send("❌ Couldn't fetch the replied message.")

            if not quote_text:
                return await ctx.send("❌ The replied message has no text to quote.")

        # ── CASE 2: Normal usage ($quote text or $quote @user text) ──
        elif text:
            if ctx.message.mentions:
                mentioned = ctx.message.mentions[0]
                for fmt in [f"<@{mentioned.id}>", f"<@!{mentioned.id}>"]:
                    if text.startswith(fmt):
                        text = text[len(fmt):].strip()
                        target = mentioned
                        break
            quote_text = text.strip()

        else:
            return await ctx.send(
                "❌ Usage:\n"
                "`$quote <text>` — quote yourself\n"
                "`$quote @user <text>` — quote someone else\n"
                "*(reply to a message)* + `$quote` — quote that message"
            )

        if not quote_text:
            return await ctx.send("❌ You mentioned someone but forgot the quote text.")
        if len(quote_text) > 220:
            return await ctx.send("❌ Quote is too long. Keep it under 220 characters.")

        # ── Fetch avatar ──
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    str(target.display_avatar.replace(format="png", size=256))
                ) as resp:
                    avatar_bytes = await resp.read()
        except Exception:
            return await ctx.send("❌ Couldn't fetch that user's avatar.")

        raw_name = target.display_name
        safe_name = target.name

        # ── Delete invoking message ──
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        # ── Build card ──
        def build_card() -> io.BytesIO:
            import subprocess, os, math

            W, H = 1000, 420

            # ── Palette ──
            BG          = (10, 10, 14)
            CARD_BG     = (18, 18, 24)
            ACCENT      = (139, 92, 246)   # violet
            QUOTE_COL   = (238, 235, 255)
            NAME_COL    = (160, 150, 200)
            DIM_COL     = (50, 45, 70)
            WHITE       = (255, 255, 255)

            # ── Font loader ──
            def find_font(bold: bool) -> str | None:
                candidates = [
                    "/root/.nix-profile/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold
                        else "/root/.nix-profile/share/fonts/truetype/noto/NotoSans-Regular.ttf",
                    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold
                        else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
                ]
                for p in candidates:
                    if os.path.exists(p):
                        return p
                for name in (["NotoSans:Bold", "DejaVuSans-Bold"] if bold else ["NotoSans", "DejaVuSans"]):
                    try:
                        r = subprocess.run(["fc-match", "--format=%{file}", name],
                                           capture_output=True, text=True)
                        p = r.stdout.strip()
                        if p and os.path.exists(p):
                            return p
                    except Exception:
                        pass
                return None

            def load(bold: bool, size: int) -> ImageFont.FreeTypeFont:
                p = find_font(bold)
                return ImageFont.truetype(p, size) if p else ImageFont.load_default(size=size)

            font_quote   = load(False, 40)
            font_open_q  = load(False, 90)   # decorative " glyph
            font_name    = load(True,  24)
            font_footer  = load(False, 15)

            # ── Base canvas ──
            img  = Image.new("RGB", (W, H), BG)
            draw = ImageDraw.Draw(img)

            # ── Subtle radial glow in top-left ──
            glow = Image.new("RGB", (W, H), BG)
            gd   = ImageDraw.Draw(glow)
            for r in range(300, 0, -1):
                alpha = int(28 * (1 - r / 300))
                col = tuple(min(255, BG[i] + alpha) for i in range(3))
                gd.ellipse((-r + 160, -r + 160, r + 160, r + 160), fill=col)
            img = Image.blend(img, glow, alpha=0.9)
            draw = ImageDraw.Draw(img)

            # ── Card rectangle (rounded via mask trick) ──
            CARD_PAD = 28
            card = Image.new("RGB", (W - 2*CARD_PAD, H - 2*CARD_PAD), CARD_BG)
            img.paste(card, (CARD_PAD, CARD_PAD))
            draw = ImageDraw.Draw(img)

            # ── Left accent bar ──
            BAR_X = CARD_PAD + 28
            BAR_Y1 = CARD_PAD + 36
            BAR_Y2 = H - CARD_PAD - 36
            draw.rectangle([BAR_X, BAR_Y1, BAR_X + 4, BAR_Y2], fill=ACCENT)

            # ── Avatar: circular, right side ──
            AV_SIZE = 160
            AV_X    = W - CARD_PAD - 48 - AV_SIZE
            AV_Y    = (H - AV_SIZE) // 2

            av_raw = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA").resize(
                (AV_SIZE, AV_SIZE), Image.LANCZOS
            )

            # Desaturate slightly
            gray = av_raw.convert("L").convert("RGBA")
            av_raw = Image.blend(av_raw, gray, alpha=0.35)

            # Circular mask
            mask = Image.new("L", (AV_SIZE, AV_SIZE), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, AV_SIZE, AV_SIZE), fill=255)
            av_raw.putalpha(mask)

            img.paste(av_raw, (AV_X, AV_Y), av_raw)

            # Thin violet ring around avatar
            ring = ImageDraw.Draw(img)
            ring.ellipse(
                [AV_X - 3, AV_Y - 3, AV_X + AV_SIZE + 3, AV_Y + AV_SIZE + 3],
                outline=ACCENT, width=2
            )
            draw = ImageDraw.Draw(img)

            # ── Text area ──
            TEXT_X  = BAR_X + 24
            TEXT_W  = AV_X - TEXT_X - 30

            # Decorative opening quote mark
            draw.text((TEXT_X - 4, CARD_PAD + 18), "\u201c", font=font_open_q, fill=(*ACCENT, 60))

            # Word-wrap — FIX: join with a space, not empty string
            words  = quote_text.split()
            lines  = []
            line   = ""
            for word in words:
                test = (line + " " + word).strip()   # ← space fix
                bbox = draw.textbbox((0, 0), test, font=font_quote)
                if bbox[2] - bbox[0] > TEXT_W:
                    if line:
                        lines.append(line)
                    line = word
                else:
                    line = test
            if line:
                lines.append(line)

            LINE_H   = 54
            total_h  = len(lines) * LINE_H
            name_gap = 20
            attr_h   = 30
            block_h  = total_h + name_gap + attr_h
            text_y   = (H - block_h) // 2 + 10

            for ln in lines:
                draw.text((TEXT_X, text_y), ln, font=font_quote, fill=QUOTE_COL)
                text_y += LINE_H

            # Attribution
            text_y += name_gap
            display_name = raw_name if raw_name.isascii() else safe_name
            attr = f"— {display_name}"
            draw.text((TEXT_X + 2, text_y), attr, font=font_name, fill=NAME_COL)

            # ── Footer ──
            footer = "MoonLight"
            fb = draw.textbbox((0, 0), footer, font=font_footer)
            fw = fb[2] - fb[0]
            draw.text(((W - fw) // 2, H - CARD_PAD - 20), footer, font=font_footer, fill=DIM_COL)

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            return buf

        buf = await self.bot.loop.run_in_executor(None, build_card)
        await quote_channel.send(file=discord.File(buf, filename="quote.png"))

        try:
            await ctx.author.send("🖼️ Your quote was posted to the quotes channel.")
        except discord.Forbidden:
            pass


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))