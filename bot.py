"""
Quantum Lotto Discord Bot
A chaotic gambling simulator where server activity increases instability
"""

import discord
from discord import app_commands
from discord.ext import tasks
import asyncio
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import our custom modules
import database
import loot_system

# Load environment variables
load_dotenv()

# Bot configuration
INSTABILITY_INCREASE_PER_MESSAGE = 0.3
INSTABILITY_CHECK_INTERVAL = 30  # seconds
COLLAPSE_THRESHOLD_MIN = 95  # minimum instability for possible collapse
COLLAPSE_THRESHOLD_MAX = 99  # maximum instability threshold


class QuantumLottoBot(discord.Client):
    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.collapse_threshold = random.uniform(COLLAPSE_THRESHOLD_MIN, COLLAPSE_THRESHOLD_MAX)
    
    async def setup_hook(self):
        """Called when bot is setting up"""
        # Initialize database
        await database.initialize_database()
        
        # Start background tasks
        self.instability_checker.start()
        self.passive_instability_increase.start()
        
        # Sync commands
        await self.tree.sync()
        print("🎰 Quantum Lotto Bot is ready!")
    
    async def on_ready(self):
        """Called when bot is fully ready"""
        print(f"💠 Logged in as {self.user}")
        print(f"⚛️ Connected to {len(self.guilds)} guild(s)")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="reality collapse | /pull"
        )
        await self.change_presence(activity=activity)
    
    async def on_message(self, message):
        """Increase instability with each message"""
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Increment message count in database
        await database.increment_message_count()
        
        # Icrease instability slightly
        new_instability = await database.update_instability(INSTABILITY_INCREASE_PER_MESSAGE)
        
        # Small chance to send chaos message at high instability
        if new_instability > 80 and random.random() < 0.02:
            warnings = [
                "⚠️ *Reality trembles...*",
                "🌀 *The void stirs...*",
                "⚡ *Quantum fluctuations detected!*",
                "💫 *Something feels... wrong...*",
                "🔥 *Entropy increases...*"
            ]
            await message.channel.send(random.choice(warnings))
    
    @tasks.loop(seconds=INSTABILITY_CHECK_INTERVAL)
    async def instability_checker(self):
        """Periodically check if universe should collapse"""
        current = await database.get_instability()
        
        # Check if we have exceeded the collapse threshold
        if current >= self.collapse_threshold:
            await self.trigger_universe_collapse()
            # Set new random threshold
            self.collapse_threshold = random.uniform(COLLAPSE_THRESHOLD_MIN, COLLAPSE_THRESHOLD_MAX)
    @tasks.loop(minutes=5)
    async def passive_instability_increase(self):
        """Slowly increase instability over time"""
        increase = random.uniform(0.5, 2.0)
        await database.update_instability(increase)
    
    async def trigger_universe_collapse(self):
        """Execute a universe collapse event"""
        print("🚨 UNIVERSE COLLAPSE TRIGGERED!")
        
        # Trigger the collapse in database
        items_removed, total_items = await database.trigger_collapse()
        
        # Get universe state
        state = await database.get_universe_state()
        collapse_count = state.get('collapse_count', 0)
        
        # Create dramatic announcement embed
        embed = discord.Embed(
            title="🚨 REALITY HAS COLLAPSED 🚨",
            description=(
                "**THE QUANTUM LOTTERY HAS BROKEN!**\n\n"
                f"The universe could not withstand the chaos.\n"
                f"**{items_removed:,}** items have been erased from existence.\n\n"
                f"💀 **Collapse #{collapse_count}**\n"
                f"⚛️ Instability has been reset to 0%\n\n"
                "*The lottery continues... for now.*"
            ),
            color=0xff0000,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Quantum Lotto • Reality is temporary")
        
        # Send to all guilds
        for guild in self.guilds:
            # Try to find a suitable channel
            channel = None
            
            # Try to find general/main channel
            for ch in guild.text_channels:
                if ch.name in ['general', 'main', 'chat']:
                    channel = ch
                    break
            
            # Fall back to first available text channel
            if not channel:
                channel = guild.text_channels[0] if guild.text_channels else None
            
            if channel:
                try:
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    print(f"Cannot send collapse message to {guild.name}")


# Create bot instance
bot = QuantumLottoBot()


# ============================================
# SLASH COMMANDS
# ============================================

@bot.tree.command(name="pull", description="💠 Pull from the Quantum Lotto (costs 1 credit)")
async def pull_command(interaction: discord.Interaction):
    """Perform a loot pull"""
    await interaction.response.defer()
    
    # Get or create user
    user = await database.get_or_create_user(
        interaction.user.id, 
        interaction.user.display_name
    )
    
    # Check if user has enough credits
    if user['credits'] < 1:
        embed = discord.Embed(
            title="❌ Insufficient Credits",
            description=(
                f"You need **1 credit** to pull, but you only have **{user['credits']}**.\n\n"
                "*Credits regenerate slowly over time, or you can earn them through events!*"
            ),
            color=0xe74c3c
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    # Deduct credit
    await database.update_user_credits(interaction.user.id, -1)
    await database.increment_user_stat(interaction.user.id, 'total_pulls')
    
    # Get current instability
    instability = await database.get_instability()
    
    # Generate loot
    item_name, rarity = loot_system.generate_loot(instability)
    
    # Add to user's inventory
    await database.add_loot_item(interaction.user.id, item_name, rarity)
    
    # Get rarity info
    rarity_info = loot_system.get_rarity_info(rarity)
    
    # Increase instability from the pull
    pull_instability_increase = random.uniform(1.5, 3.5)
    new_instability = await database.update_instability(pull_instability_increase)
    
    # Create result embed
    embed = discord.Embed(
        title=f"{rarity_info['emoji']} QUANTUM PULL RESULT",
        description=(
            f"**{item_name}**\n"
            f"Rarity: **{rarity}** {rarity_info['emoji']}\n\n"
            f"⚛️ Universe Instability: **{new_instability:.1f}%**\n"
            f"💳 Credits Remaining: **{user['credits'] - 1}**"
        ),
        color=rarity_info['color'],
        timestamp=datetime.utcnow()
    )
    
    # Add instability warning if high
    if new_instability > 85:
        embed.add_field(
            name="⚠️ WARNING",
            value="*Reality is becoming unstable! A collapse may be imminent!*",
            inline=False
        )
    
    embed.set_footer(text="Quantum Lotto v1.1")
    
    # Create persistent buttons
    view = LootButtons()
    
    await interaction.followup.send(embed=embed, view=view)


@bot.tree.command(name="status", description="⚛️ View universe instability and leaderboard")
async def status_command(interaction: discord.Interaction):
    """Show universe status and leaderboard"""
    await interaction.response.defer()
    
    # Get universe state
    state = await database.get_universe_state()
    instability = state.get('instability', 0)
    last_collapse = state.get('last_collapse')
    collapse_count = state.get('collapse_count', 0)
    
    # Get instability description
    level_title, level_desc = loot_system.get_instability_level_description(instability)
    
    # Format last collapse time
    if last_collapse:
        try:
            collapse_dt = datetime.fromisoformat(last_collapse)
            time_ago = datetime.utcnow() - collapse_dt
            if time_ago.days > 0:
                collapse_str = f"{time_ago.days}d ago"
            elif time_ago.seconds > 3600:
                collapse_str = f"{time_ago.seconds // 3600}h ago"
            else:
                collapse_str = f"{time_ago.seconds // 60}m ago"
        except:
            collapse_str = "Unknown"
    else:
        collapse_str = "Never"
    
    # Get top looters
    top_looters = await database.get_top_looters(10)
    
    # Build leaderboard text
    if top_looters:
        leaderboard_lines = []
        for i, looter in enumerate(top_looters, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            leaderboard_lines.append(
                f"{medal} **{looter['username']}** - {looter['loot_count']} items"
            )
        leaderboard_text = "\n".join(leaderboard_lines)
    else:
        leaderboard_text = "*No loot collected yet!*"
    
    # Create status embed
    embed = discord.Embed(
        title="🌀 QUANTUM UNIVERSE STATUS",
        description=f"**{level_title}**\n*{level_desc}*",
        color=0x00ffff if instability < 50 else 0xffa500 if instability < 80 else 0xff0000,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="⚛️ Current Instability",
        value=f"**{instability:.1f}%**",
        inline=True
    )
    
    embed.add_field(
        name="💀 Total Collapses",
        value=f"**{collapse_count}**",
        inline=True
    )
    
    embed.add_field(
        name="⏰ Last Collapse",
        value=collapse_str,
        inline=True
    )
    
    embed.add_field(
        name="🏆 Top Looters",
        value=leaderboard_text,
        inline=False
    )
    
    # Add current drop rates
    prob_display = loot_system.format_probability_display(instability)
    embed.add_field(
        name="🎲 Current Drop Rates",
        value=prob_display,
        inline=False
    )
    
    embed.set_footer(text="Quantum Lotto • The universe remembers")
    
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="stabilize", description="🔧 Reduce instability (costs 10 credits)")
async def stabilize_command(interaction: discord.Interaction):
    """Spend credits to reduce universe instability"""
    await interaction.response.defer()
    
    # Get user
    user = await database.get_or_create_user(
        interaction.user.id,
        interaction.user.display_name
    )
    
    # Check if user has enough credits
    if user['credits'] < 10:
        embed = discord.Embed(
            title="❌ Insufficient Credits",
            description=(
                f"Stabilization requires **10 credits**, but you only have **{user['credits']}**.\n\n"
                "*Keep pulling to earn more credits!*"
            ),
            color=0xe74c3c
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    # Deduct credits
    new_balance = await database.update_user_credits(interaction.user.id, -10)
    await database.increment_user_stat(interaction.user.id, 'total_stabilizations')
    
    # Get current instability
    current = await database.get_instability()
    
    # Calculate reduction (random between 5-15%)
    reduction = random.uniform(5.0, 15.0)
    new_instability = await database.update_instability(-reduction)
    
    # Create result embed
    embed = discord.Embed(
        title="🔧 STABILIZATION SUCCESSFUL",
        description=(
            f"You've channeled quantum energy to stabilize reality!\n\n"
            f"⚛️ Instability: **{current:.1f}%** → **{new_instability:.1f}%**\n"
            f"📉 Reduced by: **{reduction:.1f}%**\n\n"
            f"💳 Credits Remaining: **{new_balance}**"
        ),
        color=0x2ecc71,
        timestamp=datetime.utcnow()
    )
    
    embed.set_footer(text="Quantum Lotto • Preserving reality, one credit at a time")
    
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="inventory", description="🎒 View your collected loot")
async def inventory_command(interaction: discord.Interaction):
    """Show user's inventory"""
    await interaction.response.defer()
    
    # Get user inventory
    items = await database.get_user_inventory(interaction.user.id)
    user = await database.get_or_create_user(
        interaction.user.id,
        interaction.user.display_name
    )
    
    if not items:
        embed = discord.Embed(
            title="🎒 Empty Inventory",
            description=(
                "You haven't collected any loot yet!\n\n"
                "Use `/pull` to start your quantum collection!"
            ),
            color=0x95a5a6
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    # Group items by rarity
    rarity_counts = await database.get_rarity_counts(interaction.user.id)
    
    # Build inventory display
    embed = discord.Embed(
        title=f"🎒 {interaction.user.display_name}'s Quantum Vault",
        description=f"**Total Items:** {len(items)}\n**Credits:** {user['credits']}",
        color=0x9b59b6,
        timestamp=datetime.utcnow()
    )
    
    # Add rarity summary
    rarity_lines = []
    for rarity in ["Reality Breaker", "Mythic", "Legendary", "Epic", "Rare", "Common"]:
        count = rarity_counts.get(rarity, 0)
        if count > 0:
            emoji = loot_system.get_rarity_info(rarity)['emoji']
            rarity_lines.append(f"{emoji} **{rarity}**: {count}")
    
    if rarity_lines:
        embed.add_field(
            name="📊 Collection Summary",
            value="\n".join(rarity_lines),
            inline=False
        )
    
    # Show recent items (up to 15)
    recent_items = items[:15]
    recent_lines = []
    for item in recent_items:
        emoji = loot_system.get_rarity_info(item['rarity'])['emoji']
        recent_lines.append(f"{emoji} {item['item_name']}")
    
    embed.add_field(
        name="🆕 Recent Acquisitions",
        value="\n".join(recent_lines) if recent_lines else "*None*",
        inline=False
    )
    
    if len(items) > 15:
        embed.set_footer(text=f"Showing 15 of {len(items)} items • Quantum Lotto")
    else:
        embed.set_footer(text="Quantum Lotto • Your reality-defying collection")
    
    await interaction.followup.send(embed=embed)


# ============================================
# BUTTON VIEWS
# ============================================

class LootButtons(discord.ui.View):
    """Persistent buttons for loot interactions"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Pull Again", style=discord.ButtonStyle.primary, emoji="🎰")
    async def pull_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Pull again button"""
        # Invoke pull command callback
        await pull_command.callback(interaction)
    
    @discord.ui.button(label="Stabilize", style=discord.ButtonStyle.success, emoji="🔧")
    async def stabilize(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Stabilize button"""
        await stabilize_command.callback(interaction)
    
    @discord.ui.button(label="Show Inventory", style=discord.ButtonStyle.secondary, emoji="🎒")
    async def show_inventory(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show inventory button"""
        await inventory_command.callback(interaction)


# ============================================
# MAIN ENTRY POINT
# ============================================

async def get_discord_token():
    """Get Discord bot token from environment"""
    token = os.getenv('DISCORD_TOKEN')
    if token:
        print("✅ Using Discord bot token from environment")
        return token
    
    raise ValueError(
        "❌ No Discord bot token found dumbass!\n"

    )


async def main():
    """Main entry point"""
    try:
        token = await get_discord_token()
        await bot.start(token)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
