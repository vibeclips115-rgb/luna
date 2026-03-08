import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import random
import asyncio
import time
from typing import Final

from moonlight.database import (
    get_balance,
    set_balance,
    get_last_daily,
    set_daily as db_set_daily,
    get_top_balances,
)

MAX_BET = 250_000

blackjack_games = {}

CARD_VALUES: Final = {
    "A": 11,
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10
}

CARDS = list(CARD_VALUES.keys())

COIN_EMOJI = "<a:coinflip:1464991352147410944>"
CURRENCY = "MoonShards"

def hand_value(hand):
    value = sum(CARD_VALUES[c] for c in hand)
    aces = hand.count("A")

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

WHEEL_SPIN_GIF = "https://media.tenor.com/6K7Ew6N6cEAAAAAC/spinning-wheel.gif"


class Gambling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("🏓 Pong! I'm alive.")

    @commands.command(name="pay", aliases=["transfer", "give"])
    async def pay(self, ctx, member: discord.Member, amount: int):
     sender = ctx.author

     # ❌ Invalid cases
     if member.bot:
        return await ctx.send("🤖 You can’t send MoonShards to bots.")

     if member.id == sender.id:
        return await ctx.send("❌ You can’t pay yourself.")

     if amount <= 0:
         return await ctx.send("❌ Amount must be greater than 0.")

     sender_balance = get_balance(sender.id)

     if sender_balance < amount:
        return await ctx.send(
            f"❌ You don’t have enough MoonShards.\n"
            f"💰 Your balance: **{sender_balance}** 🌙"
        )

      # ✅ Transfer
     receiver_balance = get_balance(member.id)

     set_balance(sender.id, sender_balance - amount)
     set_balance(member.id, receiver_balance + amount)

     # ✅ Embed
     embed = discord.Embed(
        title="🌙 MoonShards Transfer",
        color=discord.Color.blurple()
     )

     embed.add_field(
        name="📤 Sender",
        value=sender.mention,
        inline=True
     )

     embed.add_field(
        name="📥 Receiver",
        value=member.mention,
        inline=True
     )

     embed.add_field(
        name="💸 Amount",
        value=f"**{amount}** MoonShards 🌙",
        inline=False
     )

     embed.set_thumbnail(url=sender.display_avatar.url)
     embed.set_footer(text="MoonLight Economy • Secure Transfer")

     await ctx.send(embed=embed)

    @commands.command(aliases=["spin"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sw(self, ctx, amount: int):
     user_id = ctx.author.id
     balance = get_balance(user_id)

     MAX_BET = 100_000

    # ---------- VALIDATION ----------
     if amount <= 0:
        return await ctx.send("❌ Enter a positive amount.")
     if amount > MAX_BET:
        return await ctx.send("❌ Max bet is **100,000**.")
     if amount > balance:
        return await ctx.send("❌ You don’t have enough balance.")

    # ---------- SPINNING EMBED ----------
     spinning_embed = discord.Embed(
        title="🎡 Spinning the Wheel...",
        description="The wheel spins under the Moonlight 🌙",
        color=discord.Color.blurple()
     )
     spinning_embed.set_image(
        url="https://media1.tenor.com/m/7T24taTZIWQAAAAd/spinning.gif"
    )

     msg = await ctx.send(embed=spinning_embed)
     await asyncio.sleep(2)

    # ---------- OUTCOMES ----------
     outcomes = [
        ("💀 Total disaster!", -4),
        ("😬 Bad spin", -2),
        ("😐 Weak spin", -1),
        ("🍀 Lucky spin!", 1),
        ("🔥 Great spin!", 2),
        ("💎 JACKPOT!", 4),
    ]

     text, multiplier = random.choice(outcomes)

     if multiplier > 0:
        change = amount * multiplier
        new_balance = balance + change
        result_text = f"🎉 **+{change} {CURRENCY}**"
        color = discord.Color.green()
     else:
        change = amount * abs(multiplier)
        new_balance = balance - change
        result_text = f"💸 **-{change} {CURRENCY}**"
        color = discord.Color.red()

     set_balance(user_id, new_balance)

    # ---------- RESULT EMBED ----------
     result_embed = discord.Embed(
        title="🎡 Spin Result",
        description=text,
        color=color
    )

     result_embed.add_field(
        name="🎯 Bet",
        value=f"`{amount} {CURRENCY}`",
        inline=True
    )

     result_embed.add_field(
        name="📊 Outcome",
        value=result_text,
        inline=True
    )

     result_embed.add_field(
        name="💰 New Balance",
        value=f"`{new_balance} {CURRENCY}`",
        inline=False
     )

     result_embed.set_footer(text="Moonlight Casino 🌙 Spin responsibly")

     await msg.edit(embed=result_embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def fish(self, ctx, amount: int):
     user_id = ctx.author.id
     balance = get_balance(user_id)

     MAX_BET = 100_000

     # ---------- VALIDATION ----------
     if amount <= 0:
        return await ctx.send("❌ Enter a positive amount.")
     if amount > MAX_BET:
        return await ctx.send("❌ Max bet for fishing is **100,000 MoonShards**.")
     if amount > balance:
        return await ctx.send(f"❌ You don’t have enough {CURRENCY}.")
 
     # ---------- SUSPENSE ----------
     start_embed = discord.Embed(
        title="🎣 Fishing...",
        description="Casting your line into the Moonlight waters 🌊",
        color=discord.Color.blurple()
     )
     start_embed.set_footer(text="Will you catch treasure or trash?")
     msg = await ctx.send(embed=start_embed)

     await asyncio.sleep(2)

     # ---------- OUTCOMES ----------
     outcomes = [
        ("💀 You caught trash! x4 loss", -4),
        ("😬 A weak catch... x2 loss", -2),
        ("🐟 Small fish! x1 profit", 1),
        ("🐠 Nice catch! x2 profit", 2),
        ("🦈 BIG FISH! x3 profit", 3),
        ("🐋 LEGENDARY CATCH! x4 profit", 4),
     ]

     result_text, multiplier = random.choice(outcomes)

     if multiplier > 0:
        profit = amount * multiplier
        new_balance = balance + profit
        color = discord.Color.green()
        result_line = f"🎉 **+{profit} {CURRENCY}**"
     else:
        loss = amount * abs(multiplier)
        new_balance = balance - loss
        color = discord.Color.red()
        result_line = f"💸 **-{loss} {CURRENCY}**"

     set_balance(user_id, new_balance)

    # ---------- RESULT EMBED ----------
     result_embed = discord.Embed(
        title="🎣 Fishing Result",
        description=result_text,
        color=color
     )

     result_embed.add_field(
        name="🎯 Bet",
        value=f"`{amount} {CURRENCY}`",
        inline=True
     )

     result_embed.add_field(
        name="📊 Outcome",
        value=result_line,
        inline=True
     )

     result_embed.add_field(
        name="💰 New Balance",
        value=f"`{new_balance} {CURRENCY}`",
        inline=False
     )

     result_embed.set_footer(text="Moonlight Economy • Fish responsibly 🌙")

     await msg.edit(embed=result_embed)

    @commands.command(aliases=["bal", "networth"])
    async def balance(self, ctx, member: discord.Member = None):
        user = member or ctx.author
        user_id = user.id

        balance = get_balance(user_id)

        embed = discord.Embed(
            title="💰 Moonlight Wallet",
            color=discord.Color.purple()
        )

        # Profile picture
        embed.set_thumbnail(url=user.display_avatar.url)

        embed.add_field(
            name="👤 User",
            value=user.mention,
            inline=False
        )

        embed.add_field(
            name="📍 Server",
            value=ctx.guild.name,
            inline=False
        )

        embed.add_field(
            name="💎 Net Worth",
            value=f"**{balance:,} {CURRENCY}**",
            inline=True
        )

        embed.add_field(
            name="💰 Current Balance",
            value=f"**{balance:,} {CURRENCY}**",
            inline=True
        )

        embed.set_footer(
            text="Moonlight Economy • Your financial status 🌙",
            icon_url=ctx.guild.icon.url if ctx.guild.icon else None
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def addmoney(self, ctx: commands.Context, amount: int):
        user_id: int = ctx.author.id

        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return

        new_balance: int = get_balance(user_id) + amount
        set_balance(user_id, new_balance)

        await ctx.send(
            f"💸 **Admin Grant**\n"
            f"+{amount:,} {CURRENCY}\n"
            f"💰 New Balance: **{new_balance:,}**"
        )

    @commands.command()
    async def daily(self, ctx: commands.Context):
        user_id: int = ctx.author.id
        now: int = int(time.time())
        cooldown: int = 86400  # 24 hours

        # ensure user row exists
        get_balance(user_id)

        last_claim: int = get_last_daily(user_id)

        if now - last_claim < cooldown:
            remaining = cooldown - (now - last_claim)
            hours, remainder = divmod(remaining, 3600)
            minutes, _ = divmod(remainder, 60)
            await ctx.send(
                f"⏳ Too soon! Come back in **{hours}h {minutes}m** 🌙"
            )
            return

        reward: int = random.randint(5000, 15000)
        new_balance: int = get_balance(user_id) + reward

        set_balance(user_id, new_balance)
        db_set_daily(user_id, timestamp=now)

        await ctx.send(
            f"🎁 **Daily Reward!**\n"
            f"+{reward:,} {CURRENCY}\n"
            f"💰 Balance: **{new_balance:,}**"
        )


    @commands.command(aliases=["lb", "top"])
    async def leaderboard(self, ctx):
        top_users = get_top_balances(10)

        if not top_users:
            return await ctx.send("❌ No data yet.")

        embed = discord.Embed(
            title="🏆 MoonShards Leaderboard",
            description="Top 10 richest players 🌙",
            color=discord.Color.purple()
        )

        medals = ["🥇", "🥈", "🥉"]

        for i, (user_id, balance) in enumerate(top_users):
            medal = medals[i] if i < 3 else f"#{i+1}"

            user = self.bot.get_user(user_id)
            if user is None:
                try:
                    user = await self.bot.fetch_user(user_id)
                except discord.NotFound:
                    user = None
                except discord.Forbidden:
                    user = None
                except discord.HTTPException as e:
                    print(f"Failed to fetch user {user_id}: {e}")
                    user = None

            name = user.name if user else f"User {user_id}"

            embed.add_field(
                name=f"{medal} {name}",
                value=f"💰 `{balance} {CURRENCY}`",
                inline=False
            )

        embed.set_footer(text="Moonlight Economy • Play responsibly 🌌")

        await ctx.send(embed=embed)


    @commands.command(aliases=["d"])
    @commands.cooldown(1, 10, BucketType.user)
    async def dice(self, ctx, amount: int, n1: int, n2: int):
        user_id = ctx.author.id
        balance = get_balance(user_id)

        # ---------- VALIDATION ----------
        if amount <= 0:
            return await ctx.send("❌ Enter a positive amount.")

        if amount > balance:
            return await ctx.send(f"❌ You don’t have enough {CURRENCY}.")

        if amount > MAX_BET:
            return await ctx.send(f"❌ Max bet is **{MAX_BET} {CURRENCY}**.")

        if n1 == n2:
            return await ctx.send("❌ The two numbers must be different.")

        if not (1 <= n1 <= 6 and 1 <= n2 <= 6):
            return await ctx.send("❌ Dice numbers must be between **1 and 6**.")

        # ---------- ROLL PREP ----------
        guessed = {n1, n2}
        rolled = random.sample(range(1, 7), 2)
        matches = len(guessed.intersection(rolled))

        # ---------- SUSPENSE EMBED ----------
        rolling_embed = discord.Embed(
            title="🎲 Rolling the dice...",
            description="The dice are in the air 🌙",
            color=discord.Color.blurple()
        )
        rolling_embed.set_footer(text="Moonlight Economy • Feeling lucky?")

        msg = await ctx.send(embed=rolling_embed)

        # ⏳ THE THRILL
        await asyncio.sleep(1.8)

        # ---------- RESULT ----------
        if matches == 2:
            winnings = amount * 2
            new_balance = balance + winnings
            title = "🔥 JACKPOT!"
            color = discord.Color.gold()
            result_text = f"You matched **both numbers**!\n🎉 **+{winnings} {CURRENCY}**"
        elif matches == 1:
            winnings = amount
            new_balance = balance + winnings
            title = "✅ You Won!"
            color = discord.Color.green()
            result_text = f"You matched **1 number**!\n🎉 **+{winnings} {CURRENCY}**"
        else:
            new_balance = balance - amount
            title = "💀 You Lost"
            color = discord.Color.red()
            result_text = f"No matches.\n❌ **-{amount} {CURRENCY}**"

        set_balance(user_id, new_balance)

        # ---------- FINAL EMBED ----------
        result_embed = discord.Embed(
            title=title,
            color=color
        )

        result_embed.add_field(
            name="🎲 Dice Rolled",
            value=f"**{rolled[0]} & {rolled[1]}**",
            inline=True
        )

        result_embed.add_field(
            name="🎯 Your Guess",
            value=f"**{n1} & {n2}**",
            inline=True
        )

        result_embed.add_field(
            name="📊 Result",
            value=result_text,
            inline=False
        )

        result_embed.add_field(
            name="💰 New Balance",
            value=f"`{new_balance} {CURRENCY}`",
            inline=False
        )

        result_embed.set_footer(text="Moonlight Economy • Dice Roll 🎲")

        # 🔁 EDIT — not send
        await msg.edit(embed=result_embed)

    @commands.command(aliases=["cf"])
    @commands.cooldown(1, 8, BucketType.user)
    async def coinflip(self, ctx, amount: int, choice: str = "h"):
        user_id = ctx.author.id
        balance = get_balance(user_id)
        choice = choice.lower()

        if choice not in ["h", "t"]:
            return await ctx.send("❌ Use `$cf <amount> h/t`")
        if amount <= 0:
            return await ctx.send("❌ Enter a positive amount.")
        if amount > balance:
            return await ctx.send(f"❌ You don’t have enough {CURRENCY}.")
        if amount > MAX_BET:
            return await ctx.send(f"❌ Max bet is **{MAX_BET} {CURRENCY}**.")

        bet_on = "Heads" if choice == "h" else "Tails"

        msg = await ctx.send(
            f"{COIN_EMOJI} **Flipping...**\n"
            f"🎯 You bet on **{bet_on}**"
        )
        await asyncio.sleep(1.8)

        result = random.choice(["h", "t"])
        landed = "Heads" if result == "h" else "Tails"

        if choice == result:
            new_balance = balance + amount
            result_text = f"🎉 You **WON {amount}**!"
        else:
            new_balance = balance - amount
            result_text = f"💀 You **LOST {amount}**..."

        set_balance(user_id, new_balance)

        await msg.edit(
            content=f"🪙 **{landed}!**\n"
                    f"🎯 You bet on **{bet_on}**\n"
                    f"{result_text}\n"
                    f"💰 Balance: **{new_balance}**"
        )
    @commands.command()
    async def bj(self, ctx, amount: int):
        user_id = ctx.author.id
        balance = get_balance(user_id)

        if amount <= 0:
            return await ctx.send("❌ Enter a positive amount.")


        if amount > MAX_BET:
            return await ctx.send(
                f"❌ Max blackjack bet is **{MAX_BET:,} {CURRENCY}**."
            )
        if amount > balance:
            return await ctx.send("❌ Not enough balance.")
        if user_id in blackjack_games:
            return await ctx.send("❌ Finish your current blackjack game first.")

        player = random.sample(CARDS, 2)
        dealer = random.sample(CARDS, 2)

        embed = discord.Embed(
            title="🃏 Blackjack",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🧍 Your Hand",
            value=f"{' '.join(player)} (`{hand_value(player)}`)",
            inline=False
        )

        embed.add_field(
            name="🤵 Dealer",
            value=f"{dealer[0]} ❓",
            inline=False
        )

        embed.set_footer(text="🟢 = Hit | 🛑 = Stand")

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🟢")
        await msg.add_reaction("🛑")

        blackjack_games[user_id] = {
            "amount": amount,
            "player": player,
            "dealer": dealer,
            "message_id": msg.id
        }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        game = blackjack_games.get(user.id)
        if not game:
            return

        if reaction.message.id != game["message_id"]:
            return

        try:
            await reaction.remove(user)
        except:
            pass

        player = game["player"]
        dealer = game["dealer"]
        bet = game["amount"]

        # 🟢 HIT
        if str(reaction.emoji) == "🟢":
            player.append(random.choice(CARDS))
            value = hand_value(player)

            if value > 21:
                set_balance(user.id, get_balance(user.id) - bet)
                del blackjack_games[user.id]

                embed = discord.Embed(
                    title="💀 BUST!",
                    description=f"{' '.join(player)} (`{value}`)\n❌ -{bet} {CURRENCY}",
                    color=discord.Color.red()
                )
                return await reaction.message.edit(embed=embed)

            embed = reaction.message.embeds[0]
            embed.set_field_at(
                0,
                name="🧍 Your Hand",
                value=f"{' '.join(player)} (`{value}`)",
                inline=False
            )
            return await reaction.message.edit(embed=embed)

        # 🛑 STAND
        if str(reaction.emoji) == "🛑":
            while hand_value(dealer) < 17:
                dealer.append(random.choice(CARDS))

            p = hand_value(player)
            d = hand_value(dealer)
            balance = get_balance(user.id)

            if d > 21 or p > d:
                set_balance(user.id, balance + bet)
                result = f"🎉 YOU WIN +{bet} {CURRENCY}"
                color = discord.Color.green()
            elif d == p:
                result = "😐 PUSH (tie)"
                color = discord.Color.gold()
            else:
                set_balance(user.id, balance - bet)
                result = f"💀 YOU LOSE -{bet} {CURRENCY}"
                color = discord.Color.red()

            del blackjack_games[user.id]

            embed = discord.Embed(
                title="🃏 Blackjack Result",
                color=color
            )
            embed.add_field(
                name="🧍 Your Hand",
                value=f"{' '.join(player)} (`{p}`)",
                inline=False
            )
            embed.add_field(
                name="🤵 Dealer Hand",
                value=f"{' '.join(dealer)} (`{d}`)",
                inline=False
            )
            embed.add_field(name="📊 Result", value=result, inline=False)

            await reaction.message.edit(embed=embed)

async def setup(bot):
    await bot.add_cog(Gambling(bot))
