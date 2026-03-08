import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = 1463136856374906887  

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="🎉 Welcome to the server!",
            description=(
                f"Hey {member.mention}, welcome to **{member.guild.name}**!\n\n"
                "We’re glad to have you here. Make sure to read the rules "
                "and enjoy your stay 🌙"
            ),
            color=discord.Color.blurple()
        )

        # 👤 User profile picture
        embed.set_thumbnail(url=member.display_avatar.url)

        # 📌 Extra info (optional)
        embed.add_field(
            name="👤 Member",
            value=member.display_name,
            inline=False
        )

        embed.add_field(
            name="📅 Joined",
            value=discord.utils.format_dt(member.joined_at, style="R"),
            inline=False
        )

        embed.set_footer(
            text=f"You are member #{member.guild.member_count}"
        )

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))