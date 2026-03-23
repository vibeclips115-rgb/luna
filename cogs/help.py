import asyncio
import discord
from discord.ext import commands
from datetime import datetime


# ---------- PAGE DEFINITIONS ----------

def build_pages(bot: commands.Bot) -> list[discord.Embed]:

    def page(title: str, description: str, color: int, fields: list[tuple[str, str]]) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow(),
        )
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        return embed

    pages = [

        # 0 — Overview
        page(
            "🌙 Luna — Command Index",
            (
                "```\n"
                "  Navigate  ◀️ ▶️   Jump  1️⃣–8️⃣   Close  ❌\n"
                "```\n"
                "> Every command starts with `$`\n"
                "> Some commands are restricted to staff roles\n"
                "> Luna also responds to her name and message replies — no prefix needed"
            ),
            0x9b59b6,
            [
                (
                    "📋  Pages",
                    (
                        "**1️⃣  🎭 Fun** — `$luna` `$fortune` `$cosmic` `$luck` `$comfort` `$prophecy` `$8ball` `$rate` `$roast` `$compliment` `$moonfact`\n"
                        "**2️⃣  💞 Social** — `$ship` `$marry` `$divorce` `$spouse` `$confess`\n"
                        "**3️⃣  💰 Economy** — `$balance` `$daily` `$pay` `$leaderboard`\n"
                        "**4️⃣  🎰 Gambling** — `$dice` `$cf` `$bj` `$sw` `$fish` `$slots` `$rob`\n"
                        "**5️⃣  🛡️ Moderation** — `$kick` `$ban` `$softban` `$timeout` `$warn` `$clear` `$lock` `$snipe` `$modinfo` `$disable` `$enable`\n"
                        "**6️⃣  ⚙️ Utility** — `$hug` `$kiss` `$punch` `$slap` `$pat` `$poke` `$bite` `$wave` `$kill` `$afk` `$av` `$quote`\n"
                        "**7️⃣  🤖 AI** — `$ai disable ch` `$ai enable ch` `$disable ai` `$enable ai`\n"
                        "**8️⃣  📊 Statistics** — `$activity` `$stats` `$messages` `$globalstats`"
                    )
                ),
                (
                    "⚡  Quick Tips",
                    (
                        "─ Use `$help <category>` to jump straight to a page\n"
                        "─ Example: `$help gambling` · `$help mod` · `$help ai`\n"
                        "─ Reactions time out after **90 seconds** of inactivity"
                    )
                ),
            ]
        ),

        # 1 — Fun
        page(
            "🎭  Fun Commands",
            "> Chaotic, personality-driven, and very Luna.\n> Available to **everyone** — no restrictions.",
            0x9b59b6,
            [
                ("`$luna`",               "Luna's origin story. The lore is real. Read it at least once."),
                ("`$fortune`",            "Luna reads your fortune. Cryptic, unsettling, and somehow always accurate."),
                ("`$moonfact`",           "A random fact about the Moon. Genuinely educational. Luna approves."),
                ("`$cosmic`",             "Luna reads your cosmic energy for today. Results may be disturbing."),
                ("`$luck`",               "Your luck rating for today, complete with a visual progress bar. Don't blame Luna for the outcome."),
                ("`$comfort`",            "Luna says something kind. She means every word."),
                ("`$prophecy`",           "A prophecy is delivered. It will happen. Luna doesn't know when."),
                ("`$8ball <question>`",   "Ask the oracle anything. It speaks in riddles and certainty simultaneously."),
                ("`$rate <anything>`",    "Luna rates whatever you throw at her, out of 10. Brutal honesty included."),
                ("`$roast [@user]`",      "Roast someone. The results will sting. You have been warned."),
                ("`$compliment [@user]`", "Give someone a genuine compliment. A rare act of kindness in this server."),
            ]
        ),

        # 2 — Social
        page(
            "💞  Social Commands",
            "> Relationships, anonymous confessions, and interpersonal chaos.\n> Available to **everyone**.",
            0xe84393,
            [
                ("`$ship [@user1] [@user2]`", "Calculate compatibility between two people. The algorithm is merciless."),
                ("`$marry [@user]`",          "Propose to someone. They have **60 seconds** to accept or reject you. Luna watches."),
                ("`$divorce`",                "End your current marriage. Luna witnesses it in complete silence."),
                ("`$spouse [@user]`",         "Check who someone is married to. Useful for drama."),
                (
                    "`$confess <text>`",
                    (
                        "Send an anonymous confession to the confessions channel.\n"
                        "─ Your identity is **completely hidden** — even from staff\n"
                        "─ Your command message is **deleted instantly**\n"
                        "─ You'll receive a quiet DM confirming it was posted\n"
                        "─ *30 second cooldown between confessions*"
                    )
                ),
            ]
        ),

        # 3 — Economy
        page(
            "💰  Economy Commands",
            "> Build your MoonShards empire — or watch it crumble in the gambling section.\n> Available to **everyone**.",
            0xf1c40f,
            [
                ("`$balance [@user]`",    "Check your MoonShards wallet, or spy on someone else's. No shame in it."),
                ("`$daily`",              "Claim **5,000–15,000 MoonShards** every 24 hours. Don't miss a day."),
                ("`$pay [@user] <amt>`",  "Transfer MoonShards to another user. Charity or bribery — Luna doesn't judge."),
                ("`$leaderboard`",        "The top 10 richest players on the server. Your net worth, exposed publicly."),
            ]
        ),

        # 4 — Gambling
        page(
            "🎰  Gambling Commands",
            "> High risk. Potentially higher reward.\n> Luna is not responsible for your financial decisions.",
            0xe67e22,
            [
                ("`$dice <amt> <n1> <n2>`", "Guess both dice values before they roll.\n> Match 1 → **+1×** · Match both → **+2×** · Miss → **−1×**"),
                ("`$cf <amt> <h/t>`",       "Coinflip. Heads or tails. Pure 50/50 with no house edge.\n> Win → **+1×** · Lose → **−1×**"),
                ("`$bj <amt>`",             "Blackjack. Hit 🟢 · Stand 🛑 · Double Down ⚡ — beat the dealer.\n> Natural 21 → **+1.5×** · Standard win → **+1×**"),
                ("`$sw <amt>`",             "Spin the Wheel of Fate. **Max bet: 100,000**.\n> Multipliers range from **−4× to +4×** — anything can happen"),
                ("`$fish <amt>`",           "Cast your line and see what bites. **Max bet: 100,000**.\n> Trash → **−4×** · Common → small gain · Legendary → **+4×**"),
                ("`$slots <amt>`",          "Pull the slot machine. **Max bet: 100,000**.\n> 🌙🌙🌙 → **+10× jackpot** · other combos → varying multipliers"),
                ("`$rob [@user]`",          "Attempt to rob another user.\n> **40% success rate** — steal up to 25% of their balance\n> Fail → you pay a fine instead. Choose your targets wisely."),
            ]
        ),

        # 5 — Moderation
        page(
            "🛡️  Moderation Commands",
            "> Staff-only tools, tiered by role.\n> 🔴 **Owner / Co-Owner only** · 🟡 **Trial Mod and above**",
            0xe74c3c,
            [
                ("🔴  `$kick [@user] [reason]`",                      "Remove a member from the server. They can rejoin."),
                ("🔴  `$ban [@user] [reason]`",                       "Permanently ban a member. They cannot rejoin."),
                ("🔴  `$unban <user_id>`",                            "Unban a previously banned user by their Discord ID."),
                ("🔴  `$softban [@user] [reason]`",                   "Ban then immediately unban — deletes recent messages without a permanent record."),
                ("🟡  `$timeout [@user] <mins> [reason]`",            "Temporarily mute a member. Alias: `$mute`"),
                ("🟡  `$removetimeout [@user]`",                      "Lift an active timeout early. Alias: `$unmute`"),
                ("🟡  `$warn [@user] [reason]`",                      "Issue a formal warning. It's logged and tracked."),
                ("🟡  `$warnings [@user]`",                           "View the full warning history for a member. Alias: `$warns`"),
                ("🟡  `$clearwarnings [@user]`",                      "Wipe all warnings from a member's record."),
                ("🟡  `$clear <amt / bots / user @m / contains kw>`", "Smart bulk delete with four modes: count, bots only, by user, or by keyword."),
                ("🟡  `$lock [#channel]`",                            "Prevent members from sending messages in a channel."),
                ("🟡  `$unlock [#channel]`",                          "Restore messaging permissions in a locked channel."),
                ("🟡  `$slowmode <seconds> [#channel]`",              "Set a slowmode delay. Use `0` to disable it."),
                ("🟡  `$nick [@user] [nickname]`",                    "Change or reset a member's server nickname."),
                ("🟡  `$userinfo [@user]`",                           "Full member profile — join date, roles, warnings. Aliases: `$ui` `$whois`"),
                ("🟡  `$serverinfo`",                                  "Server-wide stats and info. Aliases: `$si` `$server`"),
                ("🟡  `$snipe` / `$s`",                               "Recover the last deleted message in this channel."),
                ("🟡  `$esnipe` / `$es`",                             "Recover the last edited message in this channel."),
                ("🟡  `$modinfo`",                                     "Display the live role-permission breakdown for staff."),
                ("🔴  `$disable ai` / `$enable ai`",                  "Toggle AI responses **server-wide**. Owner & Co-Owner only."),
            ]
        ),

        # 6 — Utility
        page(
            "⚙️  Utility Commands",
            "> Actions, AFK management, avatars, and quote cards.\n> Available to **everyone** unless noted.",
            0x1abc9c,
            [
                ("`$hug [@user]`",    "Send a hug. Comes with a GIF. Always appreciated."),
                ("`$kiss [@user]`",   "Kiss someone. Bold move. Luna fetches a GIF accordingly."),
                ("`$punch [@user]`",  "Punch someone. They probably deserved it."),
                ("`$slap [@user]`",   "Slap someone. Clean, efficient, no further comment."),
                ("`$pat [@user]`",    "Pat someone on the head. Wholesome."),
                ("`$poke [@user]`",   "Poke someone repeatedly until they acknowledge you exist."),
                ("`$bite [@user]`",   "Bite someone. Feral behavior. Luna does not endorse this."),
                ("`$wave [@user]`",   "Wave at someone. The civilized option."),
                ("`$kill [@user]`",   "Dramatically eliminate someone from the narrative. Luna narrates it."),
                ("`$afk [reason]`",   "Set your AFK status with an optional reason.\nLuna will notify anyone who mentions you while you're away — and announce your return."),
                ("`$av [@user]`",     "Display a user's full-size avatar. Aliases: `$avatar` `$pfp`"),
                (
                    "`$quote`",
                    (
                        "Generate a stylized quote card and post it to the quotes channel.\n"
                        "─ `$quote <text>` — quote yourself\n"
                        "─ `$quote @user <text>` — quote someone else\n"
                        "─ *(reply to any message)* + `$quote` — instantly quotes that message and its author\n"
                        "─ *15 second cooldown · max 220 characters*"
                    )
                ),
            ]
        ),

        # 7 — AI
        page(
            "🤖  AI — Luna's Intelligence",
            "> Luna is powered by **Groq** (`llama-3.3-70b-versatile`).\n> She listens, she remembers context, and she has opinions.",
            0x5865f2,
            [
                (
                    "💬  How to Talk to Luna",
                    (
                        "No prefix needed — just say her name or reply to her:\n"
                        "```\n"
                        "luna what do you think about this?\n"
                        "hey luna, roast me\n"
                        "[reply to Luna's message] wait what did you mean\n"
                        "```"
                    )
                ),
                (
                    "⏱️  Limits",
                    (
                        "─ **Daily limit:** 10 AI responses per user per day\n"
                        "─ **Cooldown:** 10 seconds between responses\n"
                        "─ **No limits for:** Ryuken & Aizen — always bypassed"
                    )
                ),
                (
                    "🔧  AI Controls",
                    (
                        "`$ai disable ch` — silence Luna in the **current channel** only\n"
                        "`$ai enable ch` — restore Luna's replies in the **current channel**\n"
                        "`$disable ai` — disable AI responses **server-wide**\n"
                        "`$enable ai` — re-enable AI responses **server-wide**\n"
                        "*All controls require Owner or Co-Owner.*"
                    )
                ),
                (
                    "🌙  QOTD — Question of the Day",
                    (
                        "Luna posts an AI-generated question every day to the QOTD channel.\n"
                        "─ Themes rotate: philosophy, hypotheticals, morality, creativity, and more\n"
                        "─ Pings the QOTD role automatically\n"
                        "─ `$testqotd` — manually trigger a QOTD *(Owner & Co-Owner only)*"
                    )
                ),
            ]
        ),

        # 8 — Statistics
        page(
            "📊  Statistics Commands",
            "> Track your activity, earn ranks, and see who actually runs this server.\n> Available to **everyone**.",
            0x3498db,
            [
                (
                    "`$activity [@user]`",
                    (
                        "Full activity profile for a user — rank, message count with a visual bar, voice time with a visual bar, and leaderboard position.\n"
                        "Aliases: `$stats` `$profile`"
                    )
                ),
                (
                    "`$messages`",
                    (
                        "Top 10 users ranked by total message count.\n"
                        "Your position is highlighted even if you're not in the top 10.\n"
                        "Aliases: `$topmessages` `$msgstop`"
                    )
                ),
                (
                    "`$globalstats`",
                    (
                        "Server-wide aggregate stats: total messages logged, number of tracked users, and current members in voice channels.\n"
                        "Aliases: `$serverstats` `$ss`"
                    )
                ),
            ]
        ),
    ]

    # Consistent footers
    labels = ["Index"] + [f"Page {i}/8" for i in range(1, 9)]
    for i, embed in enumerate(pages):
        embed.set_footer(text=f"MoonLight  ✦  {labels[i]}  ·  ◀️ ▶️ navigate  ·  1️⃣–8️⃣ jump  ·  ❌ close")

    return pages


# ---------- REACTIONS ----------
NUMBER_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
NAV_EMOJIS    = ["◀️", "▶️", "❌"]
ALL_EMOJIS    = NAV_EMOJIS + NUMBER_EMOJIS


# ---------- COG ----------

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["h", "commands"])
    async def help(self, ctx: commands.Context, *, query: str = None):
        """Paginated help menu. Optionally: $help fun / social / economy / gambling / mod / utility / ai / stats"""
        pages = build_pages(self.bot)

        category_map = {
            "fun":        1,
            "social":     2,
            "economy":    3,
            "gambling":   4,
            "moderation": 5,
            "mod":        5,
            "utility":    6,
            "ai":         7,
            "stats":      8,
            "statistics": 8,
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

                if emoji == "▶️":
                    current = (current + 1) % len(pages)
                elif emoji == "◀️":
                    current = (current - 1) % len(pages)
                elif emoji == "❌":
                    await msg.delete()
                    return
                elif emoji in NUMBER_EMOJIS:
                    current = NUMBER_EMOJIS.index(emoji) + 1

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