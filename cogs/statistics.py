import discord
from discord.ext import commands
from datetime import datetime
import time

from moonlight.database import (
    add_message,
    add_voice_time,
    get_user_activity,
    get_message_leaderboard
)


class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_sessions = {}

    # ---------------- MESSAGE TRACKING ----------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        add_message(message.author.id)

    # ---------------- VOICE TRACKING ----------------
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        now = time.time()

        # Joined VC
        if before.channel is None and after.channel is not None:
            self.voice_sessions[member.id] = now

        # Left VC
        elif before.channel is not None and after.channel is None:
            start = self.voice_sessions.pop(member.id, None)
            if start:
                duration = int(now - start)
                add_voice_time(member.id, duration)

    # ---------------- USER ACTIVITY ----------------
    @commands.command()
    async def activity(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        messages, voice = get_user_activity(member.id)

        embed = discord.Embed(
            title=f"📊 Activity Stats — {member}",
            color=member.color,
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="💬 Messages Sent", value=messages, inline=True)
        embed.add_field(
            name="🎙️ Voice Time",
            value=f"{voice // 3600}h {(voice % 3600) // 60}m",
            inline=True
        )

        embed.set_footer(text="Luna • Statistics")

        await ctx.send(embed=embed)

    # ---------------- MESSAGE LEADERBOARD ----------------
    @commands.command(aliases=["msgstop", "topmessages"])
    async def messages(self, ctx):
        rows = get_message_leaderboard(10)

        if not rows:
            await ctx.send("No message data yet.")
            return

        lines = []
        for i, (user_id, count) in enumerate(rows, start=1):
            user = self.bot.get_user(user_id)
            name = user.name if user else f"User {user_id}"
            lines.append(f"**#{i}** {name} — `{count}` messages")

        embed = discord.Embed(
            title="💬 Message Leaderboard",
            description="\n".join(lines),
            color=0x5865F2,
            timestamp=datetime.utcnow()
        )

        embed.set_footer(text="Luna • Message Stats")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Statistics(bot))