import discord
from discord.ext import commands
from datetime import timedelta, datetime
from collections import defaultdict

# ---------- IN-MEMORY STORES ----------
sniped_messages: dict[int, dict] = {}          # channel_id → last deleted message
edited_messages: dict[int, dict] = {}          # channel_id → last edited message
warnings: dict[int, list[dict]] = defaultdict(list)  # user_id → list of warnings


# ---------- HELPERS ----------

def _mod_embed(title: str, color: discord.Color, fields: list[tuple]) -> discord.Embed:
    embed = discord.Embed(title=title, color=color, timestamp=datetime.utcnow())
    for name, value in fields:
        embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text="MoonLight Moderation 🛡️")
    return embed


# ---------- COG ----------

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------- KICK ----------

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(embed=_mod_embed(
            "👢 Member Kicked",
            discord.Color.orange(),
            [("👤 Member", member.mention), ("📝 Reason", reason), ("🔧 Moderator", ctx.author.mention)]
        ))

    # ---------- BAN ----------

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(embed=_mod_embed(
            "🔨 Member Banned",
            discord.Color.red(),
            [("👤 Member", str(member)), ("📝 Reason", reason), ("🔧 Moderator", ctx.author.mention)]
        ))

    # ---------- UNBAN ----------

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user_id: int):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(embed=_mod_embed(
                "✅ Member Unbanned",
                discord.Color.green(),
                [("👤 User", str(user)), ("🔧 Moderator", ctx.author.mention)]
            ))
        except discord.NotFound:
            await ctx.send("❌ User not found or not banned.")

    # ---------- SOFTBAN ----------

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        """Ban then immediately unban — deletes recent messages without a permanent ban."""
        await member.ban(reason=f"Softban: {reason}", delete_message_days=1)
        await ctx.guild.unban(member, reason="Softban unban")
        await ctx.send(embed=_mod_embed(
            "🧹 Member Softbanned",
            discord.Color.orange(),
            [("👤 Member", member.mention), ("📝 Reason", reason), ("🔧 Moderator", ctx.author.mention)]
        ))

    # ---------- TIMEOUT ----------

    @commands.command(aliases=["mute"])
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx: commands.Context, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
        if minutes <= 0:
            return await ctx.send("❌ Duration must be greater than 0 minutes.")
        if minutes > 40320:  # Discord max: 28 days
            return await ctx.send("❌ Max timeout is **28 days** (40,320 minutes).")

        until = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)

        h, m = divmod(minutes, 60)
        duration_str = f"{h}h {m}m" if h else f"{m}m"

        await ctx.send(embed=_mod_embed(
            "⏳ Member Timed Out",
            discord.Color.yellow(),
            [
                ("👤 Member", member.mention),
                ("⏱️ Duration", duration_str),
                ("📝 Reason", reason),
                ("🔧 Moderator", ctx.author.mention),
            ]
        ))

    # ---------- UNTIMEOUT ----------

    @commands.command(aliases=["unmute", "untimeout"])
    @commands.has_permissions(moderate_members=True)
    async def removetimeout(self, ctx: commands.Context, member: discord.Member):
        """Remove an active timeout from a member."""
        await member.timeout(None)
        await ctx.send(embed=_mod_embed(
            "✅ Timeout Removed",
            discord.Color.green(),
            [("👤 Member", member.mention), ("🔧 Moderator", ctx.author.mention)]
        ))

    # ---------- WARN ----------

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided"):
        entry = {
            "reason": reason,
            "moderator": str(ctx.author),
            "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }
        warnings[member.id].append(entry)
        count = len(warnings[member.id])

        await ctx.send(embed=_mod_embed(
            f"⚠️ Warning Issued (#{count})",
            discord.Color.yellow(),
            [
                ("👤 Member", member.mention),
                ("📝 Reason", reason),
                ("🔢 Total Warnings", str(count)),
                ("🔧 Moderator", ctx.author.mention),
            ]
        ))

    # ---------- WARNINGS ----------

    @commands.command(aliases=["warns", "infractions"])
    @commands.has_permissions(moderate_members=True)
    async def warnings(self, ctx: commands.Context, member: discord.Member):
        """View all warnings for a member."""
        user_warns = warnings.get(member.id, [])

        if not user_warns:
            return await ctx.send(f"✅ {member.mention} has no warnings.")

        embed = discord.Embed(
            title=f"⚠️ Warnings — {member.display_name}",
            color=discord.Color.yellow(),
            timestamp=datetime.utcnow(),
        )
        for i, w in enumerate(user_warns, 1):
            embed.add_field(
                name=f"#{i} — {w['time']}",
                value=f"📝 {w['reason']}\n🔧 By: {w['moderator']}",
                inline=False,
            )
        embed.set_footer(text="MoonLight Moderation 🛡️")
        await ctx.send(embed=embed)

    # ---------- CLEAR WARNINGS ----------

    @commands.command(aliases=["clearwarns"])
    @commands.has_permissions(moderate_members=True)
    async def clearwarnings(self, ctx: commands.Context, member: discord.Member):
        """Clear all warnings for a member."""
        count = len(warnings.pop(member.id, []))
        await ctx.send(embed=_mod_embed(
            "🧹 Warnings Cleared",
            discord.Color.green(),
            [("👤 Member", member.mention), ("🗑️ Removed", f"{count} warning(s)"), ("🔧 Moderator", ctx.author.mention)]
        ))

    # ---------- CLEAR / PURGE ----------

    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, *, arg: str):
        MAX_SCAN = 100
        MAX_DELETE = 50

        await ctx.message.delete()
        arg_lower = arg.lower().strip()

        # $clear bots — delete bot messages
        if arg_lower in ("bots", "contains bots"):
            deleted = []
            async for msg in ctx.channel.history(limit=MAX_SCAN):
                if msg.author.bot:
                    deleted.append(msg)
                    if len(deleted) >= MAX_DELETE:
                        break
            if not deleted:
                return await ctx.send("🤖 No recent bot messages found.", delete_after=3)
            await ctx.channel.delete_messages(deleted)
            return await ctx.send(f"🤖 Deleted **{len(deleted)}** bot messages.", delete_after=3)

        # $clear user @member — delete a specific user's messages
        if arg_lower.startswith("user "):
            raw = arg[5:].strip()
            member_id = None
            if ctx.message.mentions:
                member_id = ctx.message.mentions[0].id
            else:
                try:
                    member_id = int(raw.strip("<@!>"))
                except ValueError:
                    return await ctx.send("❌ Mention a valid user.")

            deleted = []
            async for msg in ctx.channel.history(limit=MAX_SCAN):
                if msg.author.id == member_id:
                    deleted.append(msg)
                    if len(deleted) >= MAX_DELETE:
                        break
            if not deleted:
                return await ctx.send("🔍 No recent messages from that user.", delete_after=3)
            await ctx.channel.delete_messages(deleted)
            return await ctx.send(f"🔍 Deleted **{len(deleted)}** messages from that user.", delete_after=3)

        # $clear contains <keyword>
        if arg_lower.startswith("contains "):
            keyword = arg[9:].strip().lower()
            if not keyword:
                return await ctx.send("❌ Provide a keyword.")
            deleted = []
            async for msg in ctx.channel.history(limit=MAX_SCAN):
                if keyword in msg.content.lower():
                    deleted.append(msg)
                    if len(deleted) >= MAX_DELETE:
                        break
            if not deleted:
                return await ctx.send(f"🔍 No messages found containing **'{keyword}'**.", delete_after=3)
            await ctx.channel.delete_messages(deleted)
            return await ctx.send(f"🔍 Deleted **{len(deleted)}** messages containing **'{keyword}'**.", delete_after=3)

        # $clear <number>
        try:
            amount = int(arg)
        except ValueError:
            return await ctx.send(
                "❌ Invalid usage.\n"
                "`$clear <amount>`\n"
                "`$clear bots`\n"
                "`$clear user @member`\n"
                "`$clear contains <keyword>`"
            )

        if amount <= 0 or amount > 100:
            return await ctx.send("❌ Enter a number between 1 and 100.")

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Deleted **{len(deleted)}** messages.", delete_after=3)

    # ---------- LOCK / UNLOCK ----------

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Prevent members from sending messages in a channel."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=_mod_embed(
            "🔒 Channel Locked",
            discord.Color.red(),
            [("📺 Channel", channel.mention), ("🔧 Moderator", ctx.author.mention)]
        ))

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Restore member messaging in a channel."""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(embed=_mod_embed(
            "🔓 Channel Unlocked",
            discord.Color.green(),
            [("📺 Channel", channel.mention), ("🔧 Moderator", ctx.author.mention)]
        ))

    # ---------- SLOWMODE ----------

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx: commands.Context, seconds: int, channel: discord.TextChannel = None):
        """Set slowmode delay in a channel. Use 0 to disable."""
        channel = channel or ctx.channel
        if not (0 <= seconds <= 21600):
            return await ctx.send("❌ Slowmode must be between **0** and **21600** seconds.")
        await channel.edit(slowmode_delay=seconds)
        msg = f"**{seconds}s** delay set." if seconds > 0 else "Slowmode **disabled**."
        await ctx.send(embed=_mod_embed(
            "🐢 Slowmode Updated",
            discord.Color.blurple(),
            [("📺 Channel", channel.mention), ("⏱️ Delay", msg), ("🔧 Moderator", ctx.author.mention)]
        ))

    # ---------- NICK ----------

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx: commands.Context, member: discord.Member, *, nickname: str = None):
        """Change or reset a member's nickname."""
        old_nick = member.display_name
        await member.edit(nick=nickname)
        await ctx.send(embed=_mod_embed(
            "✏️ Nickname Changed",
            discord.Color.blurple(),
            [
                ("👤 Member", member.mention),
                ("📛 Before", old_nick),
                ("📛 After", nickname or "*reset*"),
                ("🔧 Moderator", ctx.author.mention),
            ]
        ))

    # ---------- USERINFO ----------

    @commands.command(aliases=["ui", "whois"])
    async def userinfo(self, ctx: commands.Context, member: discord.Member = None):
        """Display detailed info about a member."""
        member = member or ctx.author
        roles = [r.mention for r in member.roles[1:]] or ["None"]  # skip @everyone

        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color if member.color.value else discord.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="🆔 ID", value=str(member.id), inline=True)
        embed.add_field(name="🤖 Bot", value="Yes" if member.bot else "No", inline=True)
        embed.add_field(
            name="📅 Account Created",
            value=discord.utils.format_dt(member.created_at, style="R"),
            inline=False,
        )
        embed.add_field(
            name="📥 Joined Server",
            value=discord.utils.format_dt(member.joined_at, style="R") if member.joined_at else "Unknown",
            inline=False,
        )
        embed.add_field(
            name=f"🎭 Roles ({len(member.roles) - 1})",
            value=" ".join(roles[:10]) + (" …" if len(roles) > 10 else ""),
            inline=False,
        )
        warns = len(warnings.get(member.id, []))
        embed.add_field(name="⚠️ Warnings", value=str(warns), inline=True)
        embed.set_footer(text="MoonLight Moderation 🛡️")
        await ctx.send(embed=embed)

    # ---------- SERVERINFO ----------

    @commands.command(aliases=["si", "server"])
    async def serverinfo(self, ctx: commands.Context):
        """Display info about the current server."""
        g = ctx.guild
        embed = discord.Embed(
            title=f"🏠 {g.name}",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow(),
        )
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="🆔 ID", value=str(g.id), inline=True)
        embed.add_field(name="👑 Owner", value=g.owner.mention if g.owner else "Unknown", inline=True)
        embed.add_field(name="👥 Members", value=str(g.member_count), inline=True)
        embed.add_field(name="📺 Channels", value=str(len(g.channels)), inline=True)
        embed.add_field(name="🎭 Roles", value=str(len(g.roles)), inline=True)
        embed.add_field(name="😀 Emojis", value=str(len(g.emojis)), inline=True)
        embed.add_field(
            name="📅 Created",
            value=discord.utils.format_dt(g.created_at, style="R"),
            inline=False,
        )
        embed.set_footer(text="MoonLight Moderation 🛡️")
        await ctx.send(embed=embed)

    # ---------- SNIPE ----------

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        sniped_messages[message.channel.id] = {
            "author": message.author,
            "content": message.content or "*[No text content]*",
            "time": datetime.utcnow(),
            "avatar": message.author.display_avatar.url,
        }

    @commands.command(aliases=["snipe"])
    @commands.has_permissions(manage_messages=True)
    async def s(self, ctx: commands.Context):
        data = sniped_messages.get(ctx.channel.id)
        if not data:
            return await ctx.send("❌ Nothing to snipe here.")

        embed = discord.Embed(
            title="🎯 Sniped Message",
            description=data["content"],
            color=discord.Color.dark_purple(),
            timestamp=data["time"],
        )
        embed.set_author(name=str(data["author"]), icon_url=data["avatar"])
        embed.set_footer(text="MoonLight Moderation • Deleted message 🛡️")
        await ctx.send(embed=embed)

    # ---------- EDIT SNIPE ----------

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot or before.content == after.content:
            return
        edited_messages[before.channel.id] = {
            "author": before.author,
            "before": before.content or "*[No text]*",
            "after": after.content or "*[No text]*",
            "time": datetime.utcnow(),
            "avatar": before.author.display_avatar.url,
        }

    @commands.command(aliases=["esnipe", "editsnipe"])
    @commands.has_permissions(manage_messages=True)
    async def es(self, ctx: commands.Context):
        """Snipe the last edited message in this channel."""
        data = edited_messages.get(ctx.channel.id)
        if not data:
            return await ctx.send("❌ No recently edited messages here.")

        embed = discord.Embed(
            title="✏️ Edit Sniped",
            color=discord.Color.blurple(),
            timestamp=data["time"],
        )
        embed.set_author(name=str(data["author"]), icon_url=data["avatar"])
        embed.add_field(name="📝 Before", value=data["before"], inline=False)
        embed.add_field(name="✏️ After", value=data["after"], inline=False)
        embed.set_footer(text="MoonLight Moderation • Edited message 🛡️")
        await ctx.send(embed=embed)


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))