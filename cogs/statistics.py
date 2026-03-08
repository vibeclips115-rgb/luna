import discord
from discord.ext import commands
from datetime import datetime
import time

from moonlight.database import (
    add_message,
    add_voice_time,
    get_user_activity,
    get_message_leaderboard,
)


# ---------- HELPERS ----------

def _fmt_voice(seconds: int) -> str:
    """Convert seconds into a readable duration string."""
    if seconds < 60:
        return f"{seconds}s"
    hours, remainder = divmod(seconds, 3600)
    minutes = remainder // 60
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def _activity_bar(value: int, max_value: int, length: int = 10) -> str:
    """Generate a visual progress bar."""
    if max_value == 0:
        filled = 0
    else:
        filled = min(length, round((value / max_value) * length))
    return "🟣" * filled + "⬛" * (length - filled)


def _rank_label(messages: int, voice: int) -> tuple[str, str]:
    """
    Returns (rank_title, rank_description) based on combined activity.
    """
    score = messages + (voice // 60)  # 1 point per message, 1 per minute in VC

    if score >= 10000:
        return "🌙 Moonlight Legend", "You are the server."
    elif score >= 5000:
        return "💎 Crystal Member", "Deeply embedded in this place."
    elif score >= 2000:
        return "⭐ Star Member", "A familiar face around here."
    elif score >= 500:
        return "🔥 Active Member", "You're showing up consistently."
    elif score >= 100:
        return "🌱 Rising Member", "You're finding your footing."
    else:
        return "👤 New Member", "Just getting started."


# ---------- COG ----------

class Statistics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_sessions: dict[int, float] = {}

    # ---------- MESSAGE TRACKING ----------

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        add_message(message.author.id)

    # ---------- VOICE TRACKING ----------

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if member.bot:
            return

        now = time.time()

        # Joined a channel
        if before.channel is None and after.channel is not None:
            self.voice_sessions[member.id] = now

        # Left a channel
        elif before.channel is not None and after.channel is None:
            start = self.voice_sessions.pop(member.id, None)
            if start:
                duration = int(now - start)
                add_voice_time(member.id, duration)

        # Moved between channels — restart session timer
        elif before.channel is not None and after.channel is not None:
            if before.channel != after.channel:
                start = self.voice_sessions.pop(member.id, None)
                if start:
                    duration = int(now - start)
                    add_voice_time(member.id, duration)
                self.voice_sessions[member.id] = now

    # ---------- ACTIVITY ----------

    @commands.command(aliases=["stats", "profile"])
    async def activity(self, ctx: commands.Context, member: discord.Member = None):
        """Show a user's full activity profile."""
        member = member or ctx.author
        messages, voice = get_user_activity(member.id)

        rank_title, rank_desc = _rank_label(messages, voice)

        # Leaderboard context
        top = get_message_leaderboard(50)
        user_rank = next((i + 1 for i, (uid, _) in enumerate(top) if uid == member.id), None)
        rank_str = f"**#{user_rank}** on the server" if user_rank else "Not ranked yet"

        embed = discord.Embed(
            title=rank_title,
            description=f"*{rank_desc}*",
            color=member.color if member.color.value else discord.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(
            name="💬 Messages",
            value=f"**{messages:,}**\n{_activity_bar(messages, 5000)}",
            inline=True,
        )
        embed.add_field(
            name="🎙️ Voice Time",
            value=f"**{_fmt_voice(voice)}**\n{_activity_bar(voice, 72000)}",
            inline=True,
        )
        embed.add_field(name="🏆 Leaderboard Rank", value=rank_str, inline=False)
        embed.set_footer(text="MoonLight • Activity Profile 📊")
        await ctx.send(embed=embed)

    # ---------- MESSAGE LEADERBOARD ----------

    @commands.command(aliases=["msgstop", "topmessages"])
    async def messages(self, ctx: commands.Context):
        """Top 10 users by message count."""
        rows = get_message_leaderboard(10)

        if not rows:
            return await ctx.send("📊 No message data yet.")

        medals = ["🥇", "🥈", "🥉"]
        lines = []

        for i, (user_id, count) in enumerate(rows, start=1):
            medal = medals[i - 1] if i <= 3 else f"`#{i}`"
            user = self.bot.get_user(user_id)
            name = user.display_name if user else f"Unknown ({user_id})"
            highlight = " ◀ you" if user_id == ctx.author.id else ""
            lines.append(f"{medal} **{name}** — `{count:,}` messages{highlight}")

        embed = discord.Embed(
            title="💬 Message Leaderboard",
            description="\n".join(lines),
            color=0x5865F2,
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(text="MoonLight • Message Stats 📊")
        await ctx.send(embed=embed)

    # ---------- SERVER STATS ----------

    @commands.command(aliases=["serverstats", "ss"])
    async def globalstats(self, ctx: commands.Context):
        """Show overall server activity stats."""
        rows = get_message_leaderboard(999)
        total_messages = sum(count for _, count in rows)
        total_tracked = len(rows)

        voice_now = sum(
            1 for vc in ctx.guild.voice_channels
            for m in vc.members if not m.bot
        )

        embed = discord.Embed(
            title=f"📊 {ctx.guild.name} — Server Stats",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="👥 Members", value=f"**{ctx.guild.member_count:,}**", inline=True)
        embed.add_field(name="💬 Total Messages Tracked", value=f"**{total_messages:,}**", inline=True)
        embed.add_field(name="📋 Tracked Users", value=f"**{total_tracked:,}**", inline=True)
        embed.add_field(name="🎙️ In Voice Right Now", value=f"**{voice_now}**", inline=True)
        embed.set_footer(text="MoonLight • Server Statistics 📊")
        await ctx.send(embed=embed)


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(Statistics(bot))