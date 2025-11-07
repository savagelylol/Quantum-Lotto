# 🎰 Quantum Lotto Discord Bot

A chaotic gambling simulator Discord bot where server activity increases "instability" and random loot drops become more likely as reality threatens to collapse!

## 🌀 Features

### Core Mechanics
- **Instability System**: Every message and pull increases universe instability (0-100%)
- **Collapse Events**: When instability exceeds 95%, a random collapse wipes 50-80% of all loot
- **Dynamic Drop Rates**: Higher instability = better chance for rare loot
- **Credit Economy**: Start with 10 credits, spend them to pull or stabilize

### Loot Rarities
1. ⚪ **Common** (60% base) - Basic items
2. 🔵 **Rare** (25% base) - Uncommon finds
3. 🟣 **Epic** (10% base) - Powerful artifacts
4. 🟡 **Legendary** (4% base) - Exceptional treasures
5. 🔴 **Mythic** (0.8% base) - Near-impossible finds
6. 💠 **Reality Breaker** (0.2% base) - The impossible made real

*Drop rates shift dramatically based on instability!*

### Slash Commands
- `/pull` - Pull from the Quantum Lotto (costs 1 credit)
- `/status` - View universe instability, leaderboard, and current drop rates
- `/stabilize` - Spend 10 credits to reduce instability by 5-15%
- `/inventory` - View your collected loot

### Interactive Buttons
Every pull result includes persistent buttons:
- 🎰 **Pull Again** - Quick re-pull
- 🔧 **Stabilize** - Quick stabilization
- 🎒 **Show Inventory** - Quick inventory check

## 🚀 Setup

### Prerequisites
- Python 3.11+
- Discord Bot Token
- Replit account (recommended for easy deployment)

### Using Replit (Recommended)
1. This bot uses Replit's Discord integration for secure token management
2. The Discord connection is already set up in this Repl
3. Just click "Run" and the bot will start!

### Manual Setup
1. Install dependencies:
   ```bash
   pip install discord.py python-dotenv aiosqlite
   ```

2. Create a `.env` file:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

## 🔧 Bot Configuration

### Getting a Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the token
5. Enable these **Privileged Gateway Intents**:
   - Message Content Intent
   - Server Members Intent (optional)
   - Presence Intent (optional)

### Bot Permissions
Your bot needs these permissions:
- Read Messages/View Channels
- Send Messages
- Embed Links
- Read Message History
- Use Slash Commands

### Invite Link
Use this URL template to invite your bot:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274877959168&scope=bot%20applications.commands
```

Replace `YOUR_CLIENT_ID` with your bot's client ID from the Developer Portal.

## 📊 How It Works

### Instability Mechanics
- **Per Message**: +0.3% instability
- **Per Pull**: +1.5-3.5% instability  
- **Passive Growth**: +0.5-2.0% every 5 minutes
- **Stabilization**: -5% to -15% (costs 10 credits)

### Collapse System
- Background task checks instability every 30 seconds
- Collapse triggers when instability exceeds random threshold (95-99%)
- Removes 50-80% of ALL loot items from ALL users
- Resets instability to 0%
- Announces collapse in all servers

### Credit System
- Start with 10 credits
- Pulling costs 1 credit
- Stabilizing costs 10 credits
- *Future: Credits regenerate over time or through events*

## 🗄️ Database

The bot uses SQLite with three tables:
- `users` - User credits, stats, and info
- `loot_items` - User inventories
- `universe_state` - Global instability and collapse data

Database file: `quantum_lotto.db` (auto-created on first run)

## 📁 Project Structure

```
quantum-lotto-bot/
├── bot.py              # Main bot file with commands and events
├── database.py         # SQLite operations and helpers
├── loot_system.py      # Loot generation and probability logic
├── .env                # Environment variables (not committed)
├── .env.example        # Environment template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🎨 Customization

### Adjust Instability Rates
Edit these constants in `bot.py`:
```python
INSTABILITY_INCREASE_PER_MESSAGE = 0.3
COLLAPSE_THRESHOLD_MIN = 95
COLLAPSE_THRESHOLD_MAX = 99
```

### Modify Loot Tables
Edit item pools in `loot_system.py`:
```python
ITEM_POOLS = {
    "Common": [...],
    "Rare": [...],
    # etc
}
```

### Change Drop Rates
Modify base probabilities in `loot_system.py`:
```python
RARITY_TIERS = {
    "Common": {"base_probability": 0.60, ...},
    # etc
}
```

## 🐛 Troubleshooting

### Bot won't start
- Check your Discord token is correct
- Ensure all dependencies are installed
- Check console for error messages

### Commands not showing
- Wait a few minutes for Discord to sync commands
- Try kicking and re-inviting the bot
- Ensure bot has `applications.commands` scope

### Database errors
- Delete `quantum_lotto.db` to reset (WARNING: loses all data)
- Check file permissions

## 📝 License

This project is open source and available for personal and educational use.

## 🎮 Have Fun!

May the quantum odds ever be in your favor... until they collapse! 💠⚛️🌀

---

*Quantum Lotto - Where chaos meets gambling, and reality is just a suggestion.*
