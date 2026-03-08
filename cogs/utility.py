import discord
from discord.ext import commands
from typing import Optional
import random

# ---------- AFK STORAGE ----------
afk_users = {}



class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="punch")
    async def punch(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("❌ Punch who? Mention someone.")

        embed = discord.Embed(
            description=f"🥊 **{ctx.author.mention} punched {member.mention}!**",
            color=discord.Color.red()
        )
        embed.set_image(
            url="https://media.tenor.com/6a42QlkVsCEAAAAC/anime-punch.gif"
        )

        await ctx.send(embed=embed)

    @commands.command(name="kiss")
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("❌ Kiss who? Mention someone.")

        embed = discord.Embed(
            description=f"💋 **{ctx.author.mention} kissed {member.mention}!**",
            color=discord.Color.pink()
        )
        embed.set_image(
            url="https://media1.tenor.com/m/L-NTpww8HTUAAAAC/kiss-anime-anime-kiss.gif"
        )

        await ctx.send(embed=embed)

    @commands.command(name="hug")
    async def hug(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("❌ Hug who? Mention someone.")

        embed = discord.Embed(
            description=f"🤗 **{ctx.author.mention} hugged {member.mention}!**",
            color=discord.Color.green()
        )
        embed.set_image(
            url="https://media.tenor.com/7W6E-6Y1xXQAAAAC/anime-hug.gif"
        )

        await ctx.send(embed=embed)

    @commands.command(name="slap")
    async def slap(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("❌ Slap who? Mention someone.")

        embed = discord.Embed(
            description=f"👋 **{ctx.author.mention} slapped {member.mention}!**",
            color=discord.Color.dark_red()
        )
        embed.set_image(
            url="https://media.tenor.com/9VZ5Gv7ZC4sAAAAC/anime-slap.gif"
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def afk(self, ctx, *, reason: str = "No Reason Provided"):
        afk_users[ctx.author.id] = {
            "reason": reason,
            "time": discord.utils.utcnow()
        }

        embed = discord.Embed(
            title="💤 AFK Enabled",
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.add_field(name="👤 User", value=ctx.author.mention, inline=False)
        embed.add_field(name="📌 Reason", value=reason, inline=False)
        embed.set_footer(text="I’ll let others know when they mention you 👀")

        await ctx.send(embed=embed)

    # ✅ LISTENER MUST BE HERE — NOT INSIDE afk
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # 1️⃣ AFK mention check
        for user in message.mentions:
            if user.id in afk_users:
                data = afk_users[user.id]

                embed = discord.Embed(
                    title="😭 They are afk, you dumbo",
                    color=discord.Color.orange()
                )
                embed.set_thumbnail(url=user.display_avatar.url)
                embed.add_field(name="👤 User", value=user.mention, inline=False)
                embed.add_field(name="📌 Reason", value=data["reason"], inline=False)

                await message.channel.send(embed=embed)

        # 2️⃣ Ignore commands for AFK removal
        if message.content.startswith(self.bot.command_prefix):
            return

        # 3️⃣ Normal message = AFK removed
        if message.author.id in afk_users:
            afk_users.pop(message.author.id)

            embed = discord.Embed(
                title="🎀 Welcome back cutiee!",
                description="Your AFK status has been removed.",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)

            await message.channel.send(embed=embed)

    @commands.command(aliases=["avatar", "pfp"])
    async def av(self, ctx, member: Optional[discord.Member] = None):
        user = member or ctx.author

        embed = discord.Embed(
            title=f"🖼️ {user.name}'s Avatar",
            color=discord.Color.blurple()
        )

        embed.set_image(url=user.display_avatar.url)

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)
    
# ---------- REQUIRED SETUP ----------
async def setup(bot):
    await bot.add_cog(Utility(bot))