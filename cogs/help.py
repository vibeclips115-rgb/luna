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
                "> *Every command starts with* `$`\n"
                "> *Some commands are staff-only*"
            ),
            0x9b59b6,
            [
                (
                    "╔═══════════════════════════════╗",
                    (
                        "**1️⃣  🎭 Fun** — `$luna` `$fortune` `$cosmic` `$luck` `$comfort` `$prophecy` `$8ball` `$rate` `$roast` `$compliment` `$moonfact`\n"
                        "**2️⃣  💞 Social** — `$ship` `$marry` `$divorce` `$spouse` `$confess`\n"
                        "**3️⃣  💰 Economy** — `$balance` `$daily` `$pay` `$leaderboard`\n"
                        "**4️⃣  🎰 Gambling** — `$dice` `$cf` `$bj` `$sw` `$fish` `$slots` `$rob`\n"
                        "**5️⃣  🛡️ Moderation** — `$kick` `$ban` `$softban` `$timeout` `$warn` `$clear` `$lock` `$snipe` `$modinfo` `$disable` `$enable`\n"
                        "**6️⃣  ⚙️ Utility** — `$hug` `$kiss` `$punch` `$slap` `$pat` `$poke` `$bite` `$wave` `$kill` `$afk` `$av`\n"
                        "**7️⃣  🤖 AI** — `$disable ai` `$enable ai`\n"
                        "**8️⃣  📊 Statistics** — `$activity` `$stats` `$messages` `$globalstats`"
                    )
                ),
            ]
        ),

        # 1 — Fun
        page(
            "🎭  Fun Commands",
            "> *Chaotic, personality-driven, and very Luna.*",
            0x9b59b6,
            [
                ("`$luna`",               "Luna's origin story. Read it at least once."),
                ("`$fortune`",            "Luna reads your fortune. Cryptic, as expected."),
                ("`$moonfact`",           "A random fact about the Moon. Actually educational."),
                ("`$roast [@user]`",      "Roast someone. Results will sting."),
                ("`$compliment [@user]`", "Give someone a genuine compliment for once."),
                ("`$cosmic`",             "Luna reads your cosmic energy. Unsettling."),
                ("`$luck`",               "Your luck rating for today. Comes with a visual bar."),
                ("`$comfort`",            "Luna says something kind. She means it."),
                ("`$prophecy`",           "A prophecy delivered. It will happen. Eventually."),
                ("`$8ball <question>`",   "Ask the oracle anything. It answers in riddles."),
                ("`$rate <anything>`",    "Luna rates whatever you throw at her. Out of 10."),
            ]
        ),

        # 2 — Social
        page(
            "💞  Social Commands",
            "> *Relationships, anonymous confessions, and chaos.*",
            0xe84393,
            [
                ("`$ship [@u1] [@u2]`",  "Calculate compatibility. Results may devastate."),
                ("`$marry [@user]`",     "Propose to someone. They have 60s to decide your fate."),
                ("`$divorce`",           "End your marriage. Luna witnesses it in silence."),
                ("`$spouse [@user]`",    "Check who someone is married to."),
                (
                    "`$confess <text>`",
                    (
                        "Send an anonymous confession to the confessions channel.\n"
                        "─ Your identity is **completely hidden** from everyone including staff\n"
                        "─ Your command message is deleted instantly\n"
                        "─ You'll receive a quiet DM confirming it was sent\n"
                        "─ *30 second cooldown*"
                    )
                ),
            ]
        ),

        # 3 — Economy
        page(
            "💰  Economy Commands",
            "> *Build your MoonShards empire. Or lose it.*",
            0xf1c40f,
            [
                ("`$balance [@user]`",   "Check your wallet — or spy on someone else's."),
                ("`$daily`",             "Claim **5,000–15,000 MoonShards** every 24 hours."),
                ("`$pay [@user] <amt>`", "Transfer MoonShards to another user."),
                ("`$leaderboard`",       "Top 10 richest players on the server. Are you on it?"),
            ]
        ),

        # 4 — Gambling
        page(
            "🎰  Gambling Commands",
            "> *High risk. Higher reward. Luna is not responsible for your losses.*",
            0xe67e22,
            [
                ("`$dice <amt> <n1> <n2>`", "Guess both dice rolls.\n> Match 1 → **+1x** · Match 2 → **+2x** · Miss → **−1x**"),
                ("`$cf <amt> <h/t>`",       "Coinflip. Heads or tails. Pure 50/50.\n> Win → **+1x** · Lose → **−1x**"),
                ("`$bj <amt>`",             "Blackjack. Hit 🟢 · Stand 🛑 · Double Down ⚡\n> Natural 21 → **+1.5x**"),
                ("`$sw <amt>`",             "Spin the wheel. Max **100,000**.\n> Multipliers: **−4x → +4x**"),
                ("`$fish <amt>`",           "Cast your line. Max **100,000**.\n> Trash → **−4x** · Legendary → **+4x**"),
                ("`$slots <amt>`",          "Pull the slot machine. Max **100,000**.\n> 🌙🌙🌙 → **+10x** jackpot"),
                ("`$rob [@user]`",          "Rob someone. **40% success rate.**\n> Success → steal up to 25% · Fail → pay a fine"),
            ]
        ),

        # 5 — Moderation
        page(
            "🛡️  Moderation Commands",
            "> *Staff-only tools. Tier-locked by role.*\n> 🔴 **Mod only** · 🟡 **Trial Mod+**",
            0xe74c3c,
            [
                ("🔴  `$kick [@user] [reason]`",           "Kick a member from the server."),
                ("🔴  `$ban [@user] [reason]`",            "Permanently ban a member."),
                ("🔴  `$unban <user_id>`",                 "Unban a user by their ID."),
                ("🔴  `$softban [@user] [reason]`",        "Ban + unban to wipe recent messages. No permanent record."),
                ("🟡  `$timeout [@user] <mins> [reason]`", "Timeout a member. Alias: `$mute`"),
                ("🟡  `$removetimeout [@user]`",           "Remove an active timeout. Alias: `$unmute`"),
                ("🟡  `$warn [@user] [reason]`",           "Issue a formal warning."),
                ("🟡  `$warnings [@user]`",                "View all warnings for a member. Alias: `$warns`"),
                ("🟡  `$clearwarnings [@user]`",           "Clear all warnings for a member."),
                ("🟡  `$clear <amt / bots / user @m / contains <kw>>`", "Smart bulk delete with four modes."),
                ("🟡  `$lock [#channel]`",                 "Prevent members from sending messages."),
                ("🟡  `$unlock [#channel]`",               "Restore messaging in a channel."),
                ("🟡  `$slowmode <seconds> [#channel]`",   "Set slowmode delay. Use `0` to disable."),
                ("🟡  `$nick [@user] [nickname]`",         "Change or reset a member's nickname."),
                ("🟡  `$userinfo [@user]`",                "Full member profile. Aliases: `$ui` `$whois`"),
                ("🟡  `$serverinfo`",                      "Server stats and info. Aliases: `$si` `$server`"),
                ("🟡  `$s` / `$snipe`",                   "Snipe the last deleted message in this channel."),
                ("🟡  `$es` / `$esnipe`",                  "Snipe the last edited message in this channel."),
                ("🟡  `$modinfo`",                         "Display this role-permission breakdown as a live embed."),
                ("🔴🟡 `$disable ai` / `$enable ai`",     "Toggle AI responses server-wide. **Owner & Co-Owner only.**"),
            ]
        ),

        # 6 — Utility
        page(
            "⚙️  Utility Commands",
            "> *Actions, AFK, and general tools. Available to everyone.*",
            0x1abc9c,
            [
                ("`$hug [@user]`",   "Hug someone. Always appreciated."),
                ("`$kiss [@user]`",  "Kiss someone. Bold move."),
                ("`$punch [@user]`", "Punch someone. They probably deserved it."),
                ("`$slap [@user]`",  "Slap someone. Clean and efficient."),
                ("`$pat [@user]`",   "Pat someone on the head."),
                ("`$poke [@user]`",  "Poke someone until they respond."),
                ("`$bite [@user]`",  "Bite someone. Feral behavior."),
                ("`$wave [@user]`",  "Wave at someone. Civilized."),
                ("`$kill [@user]`",  "Dramatically eliminate someone from existence."),
                ("`$afk [reason]`",  "Set your AFK status. Luna notifies anyone who mentions you."),
                ("`$av [@user]`",    "Show a user's avatar. Aliases: `$avatar` `$pfp`"),
                ("`$ping`",          "Check Luna's latency in milliseconds."),
                ("`$help`",          "You're already here. Impressive."),
            ]
        ),

        # 7 — AI
        page(
            "🤖  AI Commands",
            "> *Luna's AI is powered by Groq. She's always listening.*",
            0x5865f2,
            [
                (
                    "How to talk to Luna",
                    (
                        "Just mention her name or reply to her message — no prefix needed.\n"
                        "```\n"
                        "luna what do you think about this?\n"
                        "hey luna, roast me\n"
                        "[reply to Luna's message] wait what did you mean by that\n"
                        "```"
                    )
                ),
                (
                    "Limits",
                    (
                        "─ **Daily limit:** 10 AI responses per user\n"
                        "─ **Cooldown:** 10 seconds between responses\n"
                        "─ **Bypassed for:** Ryuken & Aizen — no limits ever"
                    )
                ),
                (
                    "`$disable ai` / `$enable ai`",
                    "Toggle AI responses server-wide.\n**Owner & Co-Owner only.**"
                ),
            ]
        ),

        # 8 — Statistics
        page(
            "📊  Statistics Commands",
            "> *Track activity, earn ranks, and see who runs the server.*",
            0x3498db,
            [
                ("`$activity [@user]`", "Full activity profile — rank, message bar, voice bar, leaderboard position.\nAliases: `$stats` `$profile`"),
                ("`$messages`",         "Top 10 users by message count. Your position is highlighted.\nAliases: `$topmessages` `$msgstop`"),
                ("`$globalstats`",      "Server-wide stats: total messages, tracked users, members in voice.\nAliases: `$serverstats` `$ss`"),
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