import discord
from discord.ext import commands
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        pages = []

        # ---------- PAGE 1 : FUN ----------
        embed1 = discord.Embed(
            title="🌙 Luna Help — Fun Commands",
            description="Fun, chaotic, and personality-based commands",
            color=0x9b59b6
        )
        embed1.add_field(name="$luna", value="Talk to Luna without a prefix", inline=False)
        embed1.add_field(name="$fortune", value="Get your fortune told", inline=False)
        embed1.add_field(name="$moonfact", value="Random moon-related facts", inline=False)
        embed1.add_field(name="$roast", value="Roast yourself or others", inline=False)
        embed1.add_field(name="$cosmic", value="Cosmic messages from Luna", inline=False)
        embed1.add_field(name="$luck", value="Check your luck today", inline=False)
        embed1.add_field(name="$comfort", value="Luna comforts you emotionally", inline=False)
        embed1.add_field(name="$prophecy", value="Receive a mysterious prophecy", inline=False)
        pages.append(embed1)

        # ---------- PAGE 2 : SOCIAL ----------
        embed2 = discord.Embed(
            title="💞 Luna Help — Social Commands",
            description="Relationships, drama, and chaos",
            color=0xe84393
        )
        embed2.add_field(name="$ship", value="Ship two users together", inline=False)
        embed2.add_field(name="$marry", value="Marry another user", inline=False)
        embed2.add_field(name="$divorce", value="Divorce your current spouse", inline=False)
        embed2.add_field(name="$spouse", value="Check who you're married to", inline=False)
        pages.append(embed2)

        # ---------- PAGE 3 : ECONOMY ----------
        embed3 = discord.Embed(
            title="💰 Luna Help — Economy Commands",
            description="Money, rewards, and grinding",
            color=0xf1c40f
        )
        embed3.add_field(name="$bal / $balance / $networth", value="Check your balance", inline=False)
        embed3.add_field(name="$daily", value="Claim daily rewards", inline=False)
        embed3.add_field(name="$pay", value="Send money to another user", inline=False)
        embed3.add_field(name="$leaderboard / $lb / $top", value="Top richest users", inline=False)
        pages.append(embed3)

        # ---------- PAGE 4 : GAMBLING ----------
        embed4 = discord.Embed(
            title="🎰 Luna Help — Gambling Commands",
            description="High risk, high reward",
            color=0xe67e22
        )
        embed4.add_field(name="$d", value="Roll a dice", inline=False)
        embed4.add_field(name="$cf", value="Coinflip gamble", inline=False)
        embed4.add_field(name="$bj", value="Play blackjack", inline=False)
        embed4.add_field(name="$sw", value="Slot machine gamble", inline=False)
        embed4.add_field(name="$fish", value="Go fishing for rewards", inline=False)
        pages.append(embed4)

        # ---------- PAGE 5 : MODERATION ----------
        embed5 = discord.Embed(
            title="🛡️ Luna Help — Moderation Commands",
            description="Admin & staff tools",
            color=0xe74c3c
        )
        embed5.add_field(name="$kick", value="Kick a member", inline=False)
        embed5.add_field(name="$ban", value="Ban a member", inline=False)
        embed5.add_field(name="$unban", value="Unban a user", inline=False)
        embed5.add_field(name="$mute", value="Mute a member", inline=False)
        embed5.add_field(name="$unmute", value="Unmute a member", inline=False)
        embed5.add_field(name="$clear / $purge", value="Delete messages", inline=False)
        pages.append(embed5)

        # ---------- PAGE 6 : UTILITY ----------
        embed6 = discord.Embed(
            title="⚙️ Luna Help — Utility Commands",
            description="Useful info & tools",
            color=0x1abc9c
        )
        embed6.add_field(name="$ping", value="Check bot latency", inline=False)
        embed6.add_field(name="$help", value="Show this help menu", inline=False)
        pages.append(embed6)

        # ---------- PAGE 7 : STATISTICS ----------
        embed7 = discord.Embed(
        title="📊 Luna Help — Statistics Commands",
        description="User activity & server analytics",
        color=0x3498db
        )

        embed7.add_field(
        name="$activity [user]",
        value="Shows how many messages a user has sent and their voice time",
        inline=False
        )

        embed7.add_field(
        name="$messages / $msgstop / $topmessages",
        value="Displays the top users by message count",
        inline=False
        )

        pages.append(embed7)

        current = 0
        msg = await ctx.send(embed=pages[current])

        reactions = ["◀️", "▶️", "❌"]
        for r in reactions:
            await msg.add_reaction(r)

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == msg.id
                and str(reaction.emoji) in reactions
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=check
                )

                if str(reaction.emoji) == "▶️":
                    current = (current + 1) % len(pages)
                    await msg.edit(embed=pages[current])

                elif str(reaction.emoji) == "◀️":
                    current = (current - 1) % len(pages)
                    await msg.edit(embed=pages[current])

                elif str(reaction.emoji) == "❌":
                    await msg.delete()
                    break

                await msg.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break


async def setup(bot):
    await bot.add_cog(Help(bot))