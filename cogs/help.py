import asyncio
import discord
from discord.ext import commands
from datetime import datetime


# ---------- PAGE DEFINITIONS ----------
# Each page: (embed, category_emoji)

def build_pages(bot: commands.Bot) -> list[discord.Embed]:

    def page(title: str, description: str, color: int, fields: list[tuple[str, str]]) -> discord.Embed:
        embed = discord.Embed(title=title, description=f"*{description}*", color=color, timestamp=datetime.utcnow())
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        return embed

    pages = [
        # 0 — Overview
        page(
            "🌙 Luna — Command Index",
            "Navigate with ◀️ ▶️ • Close with ❌ • Jump with 1️⃣–7️⃣",
            0x9b59b6,
            [
                ("🎭 Page 1 — Fun",        "`$luna` `$fortune` `$moonfact` `$roast` `$compliment`\n`$cosmic` `$luck` `$comfort` `$prophecy` `$8ball` `$rate`"),
                ("💞 Page 2 — Social",     "`$ship` `$marry` `$divorce` `$spouse`"),
                ("💰 Page 3 — Economy",    "`$balance` `$daily` `$pay` `$leaderboard`"),
                ("🎰 Page 4 — Gambling",   "`$dice` `$cf` `$bj` `$sw` `$fish` `$slots` `$rob`"),
                ("🛡️ Page 5 — Moderation", "`$kick` `$ban` `$unban` `$softban` `$timeout` `$warn`\n`$warnings` `$clear` `$lock` `$unlock` `$slowmode` `$nick` `$userinfo` `$serverinfo` `$snipe` `$es`"),
                ("⚙️ Page 6 — Utility",    "`$ping` `$help`"),
                ("📊 Page 7 — Statistics", "`$activity` `$stats` `$messages` `$topmessages` `$globalstats`"),
            ]
        ),

        # 1 — Fun
        page(
            "🎭 Fun Commands",
            "Chaotic, personality-driven, and very Luna",
            0x9b59b6,
            [
                ("`$luna`",               "Luna introduces herself. Read it."),
                ("`$fortune`",            "Luna tells your fortune. May or may not be real."),
                ("`$moonfact`",           "A random fact about the Moon. Educational, barely."),
                ("`$roast [@user]`",      "Roast someone. Or yourself if you're brave."),
                ("`$compliment [@user]`", "Give someone a genuine compliment for once."),
                ("`$cosmic`",             "Luna reads your cosmic energy. Unsettling."),
                ("`$luck`",               "Your luck rating for today. Visual bar included."),
                ("`$comfort`",            "Luna says something kind. She means it."),
                ("`$prophecy`",           "A mysterious prophecy. It will happen."),
                ("`$8ball <question>`",   "Ask the oracle anything. Yes/no only."),
                ("`$rate <anything>`",    "Luna rates whatever you throw at her. Out of 10."),
            ]
        ),

        # 2 — Social
        page(
            "💞 Social Commands",
            "Relationships, proposals, and chaos",
            0xe84393,
            [
                ("`$ship [@u1] [@u2]`", "Calculate compatibility between two people. Results may hurt."),
                ("`$marry [@user]`",    "Propose to someone. They have 60s to accept or reject you."),
                ("`$divorce`",          "End your marriage. Luna witnesses it. Says nothing."),
                ("`$spouse [@user]`",   "Check who someone is married to. Or check yourself."),
            ]
        ),

        # 3 — Economy
        page(
            "💰 Economy Commands",
            "Build your MoonShards empire",
            0xf1c40f,
            [
                ("`$balance [@user]`",    "Check your wallet — or spy on someone else's."),
                ("`$daily`",              "Claim **5,000–15,000 MoonShards** every 24 hours."),
                ("`$pay [@user] <amt>`",  "Transfer MoonShards to another user."),
                ("`$leaderboard`",        "Top 10 richest players on the server. Are you on it?"),
            ]
        ),

        # 4 — Gambling
        page(
            "🎰 Gambling Commands",
            "High risk. Higher reward. Luna isn't responsible for your losses.",
            0xe67e22,
            [
                ("`$dice <amt> <n1> <n2>`", "Guess both dice rolls.\n> Match 1 → **+1x** | Match 2 → **+2x** | Miss → **-1x**"),
                ("`$cf <amt> <h/t>`",       "Coinflip. Heads or tails. 50/50.\n> Win → **+1x** | Lose → **-1x**"),
                ("`$bj <amt>`",             "Blackjack. Hit 🟢, Stand 🛑, Double Down ⚡.\n> Natural 21 → **+1.5x**"),
                ("`$sw <amt>`",             "Spin the wheel. Max **100,000**.\n> Multipliers: **-4x → +4x**"),
                ("`$fish <amt>`",           "Cast your line. Max **100,000**.\n> Trash → **-4x** | Legendary → **+4x**"),
                ("`$slots <amt>`",          "Pull the slot machine. Max **100,000**.\n> 🌙🌙🌙 → **+10x** jackpot"),
                ("`$rob [@user]`",          "Attempt to rob someone. **40% success rate**.\n> Success → steal up to 25% | Fail → pay a fine"),
            ]
        ),

        # 5 — Moderation
        page(
            "🛡️ Moderation Commands",
            "Staff-only tools. Requires appropriate permissions.",
            0xe74c3c,
            [
                ("`$kick [@user] [reason]`",          "Kick a member from the server."),
                ("`$ban [@user] [reason]`",           "Permanently ban a member."),
                ("`$unban <user_id>`",                "Unban a user by their ID."),
                ("`$softban [@user] [reason]`",       "Ban + unban to wipe recent messages without a permanent ban."),
                ("`$timeout [@user] <mins> [reason]`","Timeout a member. Aliases: `$mute`"),
                ("`$removetimeout [@user]`",          "Remove an active timeout. Aliases: `$unmute`"),
                ("`$warn [@user] [reason]`",          "Issue a warning to a member."),
                ("`$warnings [@user]`",               "View all warnings for a member. Aliases: `$warns`"),
                ("`$clearwarnings [@user]`",          "Clear all warnings for a member."),
                ("`$clear <amount / bots / user @m / contains <kw>>`", "Smart bulk delete with multiple modes."),
                ("`$lock [#channel]`",                "Prevent members from sending messages."),
                ("`$unlock [#channel]`",              "Restore messaging in a channel."),
                ("`$slowmode <seconds> [#channel]`",  "Set slowmode delay. Use 0 to disable."),
                ("`$nick [@user] [nickname]`",        "Change or reset a member's nickname."),
                ("`$userinfo [@user]`",               "Full profile info. Aliases: `$ui` `$whois`"),
                ("`$serverinfo`",                     "Info about this server. Aliases: `$si`"),
                ("`$s` / `$snipe`",                   "Snipe the last deleted message."),
                ("`$es` / `$esnipe`",                 "Snipe the last edited message."),
            ]
        ),

        # 6 — Utility
        page(
            "⚙️ Utility Commands",
            "The boring stuff that makes everything work",
            0x1abc9c,
            [
                ("`$ping`",    "Check bot latency in milliseconds."),
                ("`$help`",    "You're already here. Impressive."),
            ]
        ),

        # 7 — Statistics
        page(
            "📊 Statistics Commands",
            "Track activity, earn ranks, and see who runs the server",
            0x3498db,
            [
                ("`$activity [@user]`",          "Full activity profile with rank, message bar, voice bar, and leaderboard position.\nAliases: `$stats` `$profile`"),
                ("`$messages`",                  "Top 10 users by message count. Your position is highlighted.\nAliases: `$topmessages` `$msgstop`"),
                ("`$globalstats`",               "Server-wide stats: total messages, tracked users, members in voice right now.\nAliases: `$serverstats` `$ss`"),
            ]
        ),
    ]

    # Add consistent footers with page numbers
    for i, embed in enumerate(pages):
        label = "Index" if i == 0 else f"Page {i}/7"
        embed.set_footer(text=f"MoonLight • {label} • ◀️ ▶️ to navigate • ❌ to close")

    return pages


# ---------- NUMBER REACTIONS ----------
NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
NAV_EMOJIS    = ["◀️", "▶️", "❌"]
ALL_EMOJIS    = NAV_EMOJIS + NUMBER_EMOJIS


# ---------- COG ----------

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["h", "commands"])
    async def help(self, ctx: commands.Context, *, query: str = None):
        """
        Paginated help menu.
        Optionally pass a category name: $help fun / economy / gambling / etc.
        """
        pages = build_pages(self.bot)

        # If user typed $help gambling etc, jump straight there
        category_map = {
            "fun":        1,
            "social":     2,
            "economy":    3,
            "gambling":   4,
            "moderation": 5,
            "mod":        5,
            "utility":    6,
            "stats":      7,
            "statistics": 7,
        }

        current = 0
        if query:
            current = category_map.get(query.lower().strip(), 0)

        msg = await ctx.send(embed=pages[current])

        for emoji in ALL_EMOJIS:
            await msg.add_reaction(emoji)

        def check(reaction: discord.Reaction, user: discord.User) -> bool:
            return (
                user.id == ctx.author.id
                and reaction.message.id == msg.id
                and str(reaction.emoji) in ALL_EMOJIS
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=90.0, check=check
                )
                emoji = str(reaction.emoji)

                # Navigation
                if emoji == "▶️":
                    current = (current + 1) % len(pages)
                elif emoji == "◀️":
                    current = (current - 1) % len(pages)
                elif emoji == "❌":
                    await msg.delete()
                    return

                # Number jumps (1️⃣ = page 1, etc.)
                elif emoji in NUMBER_EMOJIS:
                    current = NUMBER_EMOJIS.index(emoji) + 1  # +1 because 0 is index

                await msg.edit(embed=pages[current])

                try:
                    await msg.remove_reaction(reaction, user)
                except discord.Forbidden:
                    pass

            except asyncio.TimeoutError:
                try:
                    await msg.clear_reactions()
                except discord.Forbidden:
                    pass
                break


# ---------- SETUP ----------

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))