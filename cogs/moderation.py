import discord
from discord.ext import commands
from datetime import timedelta
from datetime import datetime
from collections import defaultdict

message_stats = defaultdict(list)

STATS_WINDOW = timedelta(hours=24)

# channel_id -> message data
sniped_messages = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- KICK ----------------
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 **{member}** was kicked.\n📝 Reason: {reason}")

    # ---------------- BAN ----------------
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member}** was banned.\n📝 Reason: {reason}")

    # ---------------- UNBAN ----------------
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ **{user}** has been unbanned.")

    # ---------------- TIMEOUT ----------------
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
        if minutes <= 0:
            return await ctx.send("❌ Timeout duration must be greater than 0 minutes.")

        duration = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)

        await ctx.send(
            f"⏳ **{member}** has been muted for **{minutes} minutes**.\n"
            f"📝 Reason: {reason}"
        )

    # ---------------- CLEAR / PURGE ----------------
    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *, arg: str):
        MAX_SCAN = 100        # how far back to look
        MAX_DELETE = 5       # max messages to delete

        # ---------------- BOT MESSAGES ----------------
        if arg.lower().startswith("contains bots"):
        # 🔥 DELETE THE COMMAND MESSAGE ITSELF
         await ctx.message.delete()

         deleted = []

         async for message in ctx.channel.history(limit=MAX_SCAN):
          if message.author.bot:
            deleted.append(message)
            if len(deleted) >= MAX_DELETE:
                break

         if not deleted:
          return await ctx.send(
            "🤖 No recent bot messages found.",
            delete_after=3
        )

         await ctx.channel.delete_messages(deleted)

         return await ctx.send(
        f"🤖 Deleted **{len(deleted)}** bot messages.",
        delete_after=3
    )

        # ---------------- KEYWORD ----------------
        if arg.lower().startswith("contains "):
            keyword = arg[9:].strip().lower()
            deleted = []

            if not keyword:
                return await ctx.send("❌ Please provide a keyword.")

            async for message in ctx.channel.history(limit=MAX_SCAN):
                if keyword in message.content.lower():
                    deleted.append(message)
                    if len(deleted) >= MAX_DELETE:
                        break

            if not deleted:
                return await ctx.send(
                    f"🔍 No recent messages found containing **'{keyword}'**.",
                    delete_after=3
                )

            await ctx.channel.delete_messages(deleted)
            return await ctx.send(
                f"🔍 Deleted **{len(deleted)}** messages containing **'{keyword}'**.",
                delete_after=3
            )

        # ---------------- NUMBER ----------------
        try:
            amount = int(arg)
        except ValueError:
            return await ctx.send(
                "❌ Invalid usage.\n"
                "Use:\n"
                "`$clear <amount>`\n"
                "`$clear contains <keyword>`\n"
                "`$clear contains bots`"
            )

        if amount <= 0:
            return await ctx.send("❌ Enter a valid number of messages.")

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(
            f"🧹 Deleted **{len(deleted) - 1}** messages.",
            delete_after=3
        )
    # ---------------- WARN ----------------
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await ctx.send(
            f"⚠️ **{member.mention}** has been warned.\n📝 Reason: {reason}"
        )

    #----------------SNIPE------------------
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        sniped_messages[message.channel.id] = {
            "author": message.author,
            "content": message.content if message.content else "*[No text]*",
            "time": datetime.utcnow(),
            "avatar": message.author.display_avatar.url
        }

    @commands.command(name="s", aliases=["snipe"])
    @commands.has_permissions(manage_messages=True)
    async def snipe(self, ctx):
        data = sniped_messages.get(ctx.channel.id)

        if not data:
            return await ctx.send("❌ Nothing to snipe here.")

        embed = discord.Embed(
            title="🎯 Sniped Message",
            description=data["content"],
            color=discord.Color.dark_purple(),
            timestamp=data["time"]
        )

        embed.set_author(
            name=str(data["author"]),
            icon_url=data["avatar"]
        )

        embed.set_footer(text="MoonLight Moderation • Deleted message")

        await ctx.send(embed=embed)
   
async def setup(bot):
    await bot.add_cog(Moderation(bot))