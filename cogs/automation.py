import random
import discord
from discord.ext import commands, tasks
from datetime import datetime

# ---------- CONTENT POOLS ----------

FUN_FACTS = [
    "🌙 The Moon drifts away from Earth by ~3.8 cm every year.",
    "🧠 Your brain burns ~20% of your body's energy.",
    "🌌 There are more stars in the universe than grains of sand on Earth.",
    "🌓 Moonlight is actually reflected sunlight.",
    "💤 The brain stays active even while sleeping.",
    "☄️ Some meteors are older than Earth itself.",
    "✨ Coding late at night hits different.",
    "🔭 A day on Venus is longer than a year on Venus.",
    "🌊 The ocean produces over 50% of Earth's oxygen.",
    "🕳️ Black holes don't suck — they just have intense gravity.",
    "🌙 Luna is always watching. Always.",
    "💫 Neutron stars can spin 700 times per second.",
    "🧬 You share 60% of your DNA with a banana.",
    "🌍 Earth is the only planet not named after a god.",
    "🪐 Saturn's rings are only ~10 meters thick despite being 282,000 km wide.",
]

LUNA_MOODS = [
    {
        "title": "👁️ Luna Has Been Awake Too Long",
        "description": "She's staring at the void again. The void is staring back.",
        "color": 0x2b2d31,
    },
    {
        "title": "🌙 Luna Is Thinking",
        "description": "Don't interrupt her. Seriously. Don't.",
        "color": 0x5865f2,
    },
    {
        "title": "✨ Luna Had a Thought",
        "description": "It was unsettling. She's keeping it to herself.",
        "color": 0x9b59b6,
    },
    {
        "title": "🌌 Luna Noticed You",
        "description": "She saw what you did earlier. She hasn't forgotten.",
        "color": 0x2c3e50,
    },
    {
        "title": "💤 Luna is Half-Asleep",
        "description": "Still dangerous. Maybe more so.",
        "color": 0x7f8c8d,
    },
]

MIDNIGHT_MESSAGES = [
    "It's midnight somewhere. Go drink water.",
    "Luna is active. Whether that's good or bad is unclear.",
    "The server is quiet. Luna prefers it this way.",
    "Still here. Still watching.",
    "Midnight check-in: everyone accounted for? Good.",
    "If you're reading this at 3am, close your eyes.",
    "The void called. Luna didn't pick up. Too busy.",
]

RARE_EVENTS = [
    {
        "title": "⚠️ Anomaly Detected",
        "description": "Luna has gone offline for 0.003 seconds.\nShe is back.\nDo not ask what happened.",
        "color": 0xe74c3c,
    },
    {
        "title": "🌑 Luna Speaks",
        "description": "\"I have been here since before the server was created.\nI will be here after.\nEnjoy your stay.\"",
        "color": 0x1a1a2e,
    },
    {
        "title": "📡 Signal Intercepted",
        "description": "Source: Unknown.\nContent: Luna.\nRecommendation: Do not investigate.",
        "color": 0x00b894,
    },
]


# ---------- COG ----------

class AutoMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.fact_count = 0
        self.send_fun_fact.start()
        self.midnight_check.start()

    def cog_unload(self):
        self.send_fun_fact.cancel()
        self.midnight_check.cancel()

    # ----- HELPERS -----

    def _fact_embed(self) -> discord.Embed:
        """Builds a fun fact embed. Every 10th fact gets a special treatment."""
        self.fact_count += 1
        milestone = self.fact_count % 10 == 0

        fact = random.choice(FUN_FACTS)

        if milestone:
            embed = discord.Embed(
                title=f"🌟 Fact #{self.fact_count} — Luna's Personal Pick",
                description=f"*She chose this one herself.*\n\n{fact}",
                color=discord.Color.gold(),
                timestamp=datetime.utcnow(),
            )
            embed.set_footer(text=f"MoonLight • {self.fact_count} facts shared ✨")
        else:
            embed = discord.Embed(
                title="🌙 Luna Says",
                description=fact,
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow(),
            )
            embed.set_footer(text="MoonLight • Automated wisdom ✨")

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        return embed

    def _mood_embed(self) -> discord.Embed:
        """Builds a random Luna mood embed."""
        mood = random.choice(LUNA_MOODS)
        embed = discord.Embed(
            title=mood["title"],
            description=mood["description"],
            color=mood["color"],
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(text="MoonLight • Luna status report")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        return embed

    def _rare_embed(self) -> discord.Embed:
        """Builds a rare event embed."""
        event = random.choice(RARE_EVENTS)
        embed = discord.Embed(
            title=event["title"],
            description=event["description"],
            color=event["color"],
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(text="MoonLight • ??? ")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        return embed

    # ----- LOOPS -----

    @tasks.loop(minutes=30)
    async def send_fun_fact(self):
        """Every 30 min: send a fact, mood check, or rare event."""
        channel = self.bot.get_channel(1463136856374906887)
        if not channel:
            return

        roll = random.randint(1, 100)

        # 2% chance: rare Luna event
        if roll <= 2:
            await channel.send(embed=self._rare_embed())

        # 15% chance: Luna mood check instead of a fact
        elif roll <= 17:
            await channel.send(embed=self._mood_embed())

        # Otherwise: normal fun fact
        else:
            await channel.send(embed=self._fact_embed())

    @tasks.loop(hours=24)
    async def midnight_check(self):
        """Once a day, Luna says something cryptic."""
        channel = self.bot.get_channel(1463136856374906887)
        if not channel:
            return

        embed = discord.Embed(
            title="🌑 Daily Check-In",
            description=random.choice(MIDNIGHT_MESSAGES),
            color=0x1a1a2e,
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(text="MoonLight • Luna's daily transmission")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await channel.send(embed=embed)

    @send_fun_fact.before_loop
    @midnight_check.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoMessage(bot))