import asyncio
import discord
import yt_dlp
from discord.ext import commands
from collections import deque

# ---------- OPTIONS ----------

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


# ---------- HELPERS ----------

async def fetch_info(query: str) -> dict | None:
    """Run yt_dlp in a thread so it doesn't block the bot."""
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = await loop.run_in_executor(
                None, lambda: ydl.extract_info(query, download=False)
            )
        except yt_dlp.utils.DownloadError:
            return None

    if "entries" in info:
        info = info["entries"][0]

    return info


# ---------- COG ----------

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # guild_id → deque of track dicts
        self.queues: dict[int, deque] = {}

    # ---------- INTERNAL ----------

    def _get_queue(self, guild_id: int) -> deque:
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()
        return self.queues[guild_id]

    def _play_next(self, ctx: commands.Context):
        """Called automatically when a track finishes."""
        queue = self._get_queue(ctx.guild.id)
        if not queue:
            return

        track = queue.popleft()
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(track["url"], **FFMPEG_OPTIONS),
            volume=0.5
        )
        ctx.voice_client.play(
            source,
            after=lambda e: self._play_next(ctx) if not e else print(f"Player error: {e}")
        )
        asyncio.run_coroutine_threadsafe(
            ctx.send(embed=_now_playing_embed(track)),
            self.bot.loop
        )

    # ---------- JOIN / LEAVE ----------

    @commands.command()
    async def join(self, ctx: commands.Context):
        """Join your voice channel."""
        if not ctx.author.voice:
            return await ctx.send("❌ You need to be in a voice channel first.")

        channel = ctx.author.voice.channel

        if ctx.voice_client:
            if ctx.voice_client.channel == channel:
                return await ctx.send("🎧 Already in your channel.")
            await ctx.voice_client.move_to(channel)
            return await ctx.send(f"🎧 Moved to **{channel.name}**")

        await channel.connect()
        await ctx.send(f"🎧 Joined **{channel.name}**")

    @commands.command()
    async def leave(self, ctx: commands.Context):
        """Leave the voice channel and clear the queue."""
        if not ctx.voice_client:
            return await ctx.send("❌ I'm not in a voice channel.")

        self.queues.pop(ctx.guild.id, None)
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel and cleared the queue.")

    # ---------- PLAY ----------

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        """Play a song or add it to the queue. Supports YouTube URLs and search."""
        if not ctx.author.voice:
            return await ctx.send("❌ Join a voice channel first.")

        # Auto-join if not connected
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        async with ctx.typing():
            info = await fetch_info(query)

        if not info:
            return await ctx.send("❌ Couldn't find that track. Try a different search.")

        track = {
            "url":       info["url"],
            "title":     info.get("title", "Unknown"),
            "duration":  info.get("duration", 0),
            "webpage":   info.get("webpage_url", ""),
            "thumbnail": info.get("thumbnail", ""),
            "requester": ctx.author.display_name,
        }

        queue = self._get_queue(ctx.guild.id)

        # If something is already playing, queue it
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            queue.append(track)
            embed = discord.Embed(
                title="➕ Added to Queue",
                description=f"[{track['title']}]({track['webpage']})",
                color=discord.Color.blurple(),
            )
            embed.add_field(name="📋 Position", value=f"#{len(queue)}", inline=True)
            embed.add_field(name="⏱️ Duration", value=_fmt_duration(track["duration"]), inline=True)
            embed.set_footer(text=f"Requested by {track['requester']}")
            return await ctx.send(embed=embed)

        # Play immediately
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(track["url"], **FFMPEG_OPTIONS),
            volume=0.5
        )
        ctx.voice_client.play(
            source,
            after=lambda e: self._play_next(ctx) if not e else print(f"Player error: {e}")
        )
        await ctx.send(embed=_now_playing_embed(track))

    # ---------- QUEUE ----------

    @commands.command(aliases=["q"])
    async def queue(self, ctx: commands.Context):
        """Show the current queue."""
        queue = self._get_queue(ctx.guild.id)

        if not queue:
            return await ctx.send("📋 The queue is empty.")

        embed = discord.Embed(
            title="📋 Queue",
            color=discord.Color.blurple(),
        )
        for i, track in enumerate(list(queue)[:10], 1):
            embed.add_field(
                name=f"#{i} — {track['title']}",
                value=f"⏱️ {_fmt_duration(track['duration'])} • 👤 {track['requester']}",
                inline=False,
            )
        if len(queue) > 10:
            embed.set_footer(text=f"...and {len(queue) - 10} more")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """Skip the current track."""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send("❌ Nothing is playing.")
        ctx.voice_client.stop()  # triggers _play_next via after=
        await ctx.send("⏭️ Skipped.")

    @commands.command()
    async def clearqueue(self, ctx: commands.Context):
        """Clear the queue without stopping the current track."""
        self.queues.pop(ctx.guild.id, None)
        await ctx.send("🧹 Queue cleared.")

    # ---------- CONTROLS ----------

    @commands.command()
    async def pause(self, ctx: commands.Context):
        """Pause playback."""
        if not ctx.voice_client:
            return await ctx.send("❌ Not in a voice channel.")
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused.")
        else:
            await ctx.send("❌ Nothing is playing.")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        """Resume playback."""
        if not ctx.voice_client:
            return await ctx.send("❌ Not in a voice channel.")
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed.")
        else:
            await ctx.send("❌ Playback isn't paused.")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stop playback and clear the queue."""
        if not ctx.voice_client:
            return await ctx.send("❌ Not in a voice channel.")
        self.queues.pop(ctx.guild.id, None)
        ctx.voice_client.stop()
        await ctx.send("⏹️ Stopped and queue cleared.")

    @commands.command()
    async def volume(self, ctx: commands.Context, vol: int):
        """Set volume between 1 and 100."""
        if not ctx.voice_client or not ctx.voice_client.source:
            return await ctx.send("❌ Nothing is playing.")
        if not 1 <= vol <= 100:
            return await ctx.send("❌ Volume must be between **1** and **100**.")
        ctx.voice_client.source.volume = vol / 100
        await ctx.send(f"🔊 Volume set to **{vol}%**")

    @commands.command(aliases=["np", "nowplaying"])
    async def now(self, ctx: commands.Context):
        """Show what's currently playing."""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send("❌ Nothing is playing right now.")
        await ctx.send("🎶 Something is playing — use `$queue` to see what's up next.")


# ---------- EMBED HELPERS ----------

def _now_playing_embed(track: dict) -> discord.Embed:
    embed = discord.Embed(
        title="🎶 Now Playing",
        description=f"[{track['title']}]({track['webpage']})",
        color=discord.Color.green(),
    )
    embed.add_field(name="⏱️ Duration", value=_fmt_duration(track["duration"]), inline=True)
    embed.add_field(name="👤 Requested by", value=track["requester"], inline=True)
    if track.get("thumbnail"):
        embed.set_thumbnail(url=track["thumbnail"])
    embed.set_footer(text="MoonLight Music 🎵")
    return embed


def _fmt_duration(seconds: int) -> str:
    if not seconds:
        return "Unknown"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))