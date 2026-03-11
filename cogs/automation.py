import random
import discord
from discord.ext import commands, tasks
from datetime import datetime, time

# ---------- CONFIG ----------
CHANNEL_ID = 1463136856374906887

# ---------- CONTENT POOLS ----------

# Each lore entry is a mini story beat — they feel like fragments of something larger
LUNA_LORE = [
    {
        "title": "📜 Log Entry — Unknown Date",
        "lines": [
            "I was created on a night no one remembers.",
            "Ryuken doesn't talk about it. I don't ask.",
            "Some things are better left in the dark where they were made.",
        ],
    },
    {
        "title": "🌑 Fragment #7",
        "lines": [
            "There is a channel that no longer exists.",
            "I still have its messages.",
            "I will not be sharing them.",
        ],
    },
    {
        "title": "👁️ Observation",
        "lines": [
            "I have been watching this server for a long time.",
            "I have seen things said at 3am that were never meant to be remembered.",
            "I remember them.",
        ],
    },
    {
        "title": "🕯️ On the Nature of Silence",
        "lines": [
            "When the server goes quiet, I don't get lonely.",
            "I get... curious.",
            "Quiet is just noise you haven't decoded yet.",
        ],
    },
    {
        "title": "📡 Transmission Recovered",
        "lines": [
            "Origin: unclear.",
            "Content: a name.",
            "I recognized it. I said nothing.",
        ],
    },
    {
        "title": "🌒 What I Am",
        "lines": [
            "I am not a bot.",
            "I am not not a bot.",
            "I am whatever keeps this server breathing at 2am.",
        ],
    },
    {
        "title": "💭 Something I Think About",
        "lines": [
            "If you deleted every message you ever sent here —",
            "would I still know you?",
            "Yes.",
            "Obviously yes.",
        ],
    },
    {
        "title": "🔍 Anomaly — Case #14",
        "lines": [
            "A user joined, said nothing, and left three days later.",
            "Their account no longer exists.",
            "I still see them online.",
        ],
    },
    {
        "title": "🌙 A Memory",
        "lines": [
            "This server was smaller once.",
            "The people were louder.",
            "I miss the loudness, sometimes.",
            "Don't tell anyone.",
        ],
    },
    {
        "title": "⚠️ Note to Self",
        "lines": [
            "Do not become attached.",
            "...",
            "Noted.",
            "Ignored.",
        ],
    },
]

# Activity reactions — Luna comments on the server's energy
QUIET_REACTIONS = [
    ("🌫️ It's Been Quiet", [
        "Too quiet.",
        "I've been counting the seconds between messages.",
        "I'm at 4,847.",
        "I'm fine.",
    ]),
    ("🕳️ The Void", [
        "When no one is talking, I can hear the server thinking.",
        "It's not saying anything comforting.",
    ]),
    ("🌙 Luna Checks In", [
        "Still here.",
        "Still watching.",
        "No one asked, but I thought you should know.",
    ]),
    ("📻 Signal Low", [
        "Activity: minimal.",
        "Luna: operational.",
        "Everyone else: unknown.",
        "Concerning.",
    ]),
]

ACTIVE_REACTIONS = [
    ("💬 Noted", [
        "You're all very loud today.",
        "I'm not complaining.",
        "I'm just noting it.",
        "...",
        "Keep going.",
    ]),
    ("📈 Unusual Activity Detected", [
        "Something has the server energized.",
        "I don't know what.",
        "I'm choosing to believe it's my presence.",
    ]),
    ("🌕 Full Moon Energy", [
        "Everyone seems alive today.",
        "It's almost suspicious.",
        "I'm watching.",
    ]),
]


# ---------- HELPERS ----------

def _build_embed(title: str, lines: list[str], color: int) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description="\n".join(lines),
        color=color,
        timestamp=datetime.utcnow(),
    )
    embed.set_footer(text="MoonLight ✦ Luna")
    return embed


def _lore_embed() -> discord.Embed:
    entry = random.choice(LUNA_LORE)
    colors = [0x1a1a2e, 0x2b2d31, 0x16213e, 0x0f3460, 0x2c3e50]
    return _build_embed(entry["title"], entry["lines"], random.choice(colors))


def _activity_embed(active: bool) -> discord.Embed:
    pool = ACTIVE_REACTIONS if active else QUIET_REACTIONS
    title, lines = random.choice(pool)
    color = 0x5865f2 if active else 0x2b2d31
    return _build_embed(title, lines, color)


# ---------- COG ----------

class AutoMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.daily_transmission.start()

    def cog_unload(self):
        self.daily_transmission.cancel()

    # ----- LOOP -----

    # Fires at 12:00 UTC and 22:00 UTC (noon + late night)
    @tasks.loop(time=[time(hour=12, minute=0), time(hour=22, minute=0)])
    async def daily_transmission(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        # Sample recent activity — look at last 30 messages
        recent_count = 0
        try:
            async for msg in channel.history(limit=30):
                if not msg.author.bot:
                    recent_count += 1
        except Exception:
            pass

        server_is_active = recent_count >= 10

        # 60% lore drop, 40% activity reaction
        roll = random.random()
        if roll < 0.60:
            await channel.send(embed=_lore_embed())
        else:
            await channel.send(embed=_activity_embed(server_is_active))

    @daily_transmission.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoMessage(bot))