# Overview

Quantum Lotto is a Discord bot that gamifies server activity through a chaotic gambling simulator. The bot tracks "universe instability" that increases with server activity and loot pulls, creating dynamic risk/reward mechanics. When instability reaches critical levels (95%+), random "collapse events" can wipe 50-80% of all user loot. The core loop involves users spending credits to pull for rare loot, with drop rates that improve as instability rises, balanced against the risk of losing everything in a collapse.

## Current Status
**Completed**: All core features implemented and reviewed. Bot is functional and waiting for user to enable Message Content Intent in Discord Developer Portal.

**Last Updated**: November 7, 2025

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Application Structure

**Monolithic Discord Bot Architecture**: The bot uses a single-process design with discord.py as the main framework. The architecture is split into three primary modules:

- `bot.py` - Main bot client, command handlers, and event listeners
- `database.py` - SQLite persistence layer for users, loot, and universe state
- `loot_system.py` - Probability calculations and item generation logic

**Rationale**: This modular separation keeps concerns isolated while maintaining simplicity. For a Discord bot with relatively low traffic, a monolithic approach avoids unnecessary complexity of microservices while still providing clear code organization.

## Discord Integration

**Discord.py with Slash Commands**: Uses discord.py v2.6+ with the app_commands framework for modern slash command interactions. Privileged intents (specifically Message Content Intent) are required to track server activity for the instability mechanic.

**Interactive Components**: Implements Discord's button components for persistent UI elements (Pull Again, Stabilize, Show Inventory buttons) attached to pull result messages.

**Rationale**: Slash commands provide better discoverability and type safety compared to prefix commands. Buttons reduce friction for repeated actions and improve user engagement with the gambling loop.

## Data Persistence

**SQLite with aiosqlite**: Uses aiosqlite for async database operations with three main tables:

1. `users` - Stores user credits, statistics, and pull/stabilization counts
2. `loot_items` - Inventory system linking users to acquired loot with timestamps
3. `universe_state` - Singleton table tracking global instability, collapse history, and message counts

**Rationale**: SQLite is appropriate for a bot's scale (single server deployment, moderate data volume). The async wrapper (aiosqlite) prevents blocking the Discord event loop during database operations. The schema uses simple foreign keys rather than complex normalization to prioritize query simplicity.

## Game Mechanics System

**Dynamic Probability Engine**: The loot system calculates drop rates based on current instability percentage. Higher instability shifts probabilities toward rarer items, creating a risk/reward tension with collapse events.

**Background Task System**: Uses discord.ext.tasks for two periodic jobs:
- Instability checker (30s intervals) - Monitors for collapse threshold breaches
- Passive instability increase (5min intervals) - Simulates universe decay even without activity

**State Management**: Global universe state (instability level, collapse threshold) is stored in the database and cached in bot memory for performance. Each message event increments instability by a fixed amount (0.3%).

**Rationale**: The probability engine is the core differentiator of this bot. Storing it in a separate module allows for easy tuning of the risk curve without touching bot or database logic. Background tasks ensure the universe feels "alive" even during quiet periods.

## Economy System

**Credit-Based Currency**: Users start with 10 credits. Pulls cost 1 credit, stabilization costs 10 credits. No credit purchase mechanism exists - credits are earned through future features (not yet implemented).

**Rationale**: Simple integer-based economy avoids floating-point issues. The 1:10 cost ratio for pull vs stabilize creates meaningful economic decisions.

# Recent Changes

## November 7, 2025 - Initial Implementation
- Created complete bot implementation with all requested features
- Implemented database module with SQLite schema and helper functions
- Built loot system with 6 rarity tiers (Common, Rare, Epic, Legendary, Mythic, Reality Breaker)
- Added instability-based probability scaling for dynamic drop rates
- Created slash commands: `/pull`, `/status`, `/stabilize`, `/inventory`
- Implemented background tasks for instability checks and passive growth
- Added persistent buttons for quick actions (Pull Again, Stabilize, Show Inventory)
- Created sci-fi themed embeds with emojis (💠⚛️🌀💫)
- Set up workflow to run bot automatically
- Created comprehensive documentation (README.md and SETUP_INSTRUCTIONS.md)
- Configured .gitignore for Python projects

# External Dependencies

## Core Dependencies

**discord.py** (v2.6.4): Primary Discord API wrapper providing bot client, slash commands, interactions, and event handling. Version 2.0+ required for modern slash command support.

**python-dotenv** (v1.2.1): Environment variable management for secure token storage. Integrates with Replit's secrets management system.

**aiosqlite** (v0.21.0): Async SQLite driver preventing database operations from blocking Discord's event loop.

## Discord Developer Portal

**Bot Token**: Requires a Discord application with bot token stored in `DISCORD_TOKEN` environment variable (configured in Replit Secrets).

**Privileged Intents**: Message Content Intent must be enabled in the Discord Developer Portal for the bot to track message events for instability increases. This is the only blocker preventing the bot from running.

**OAuth2 Permissions**: Bot requires the following permissions:
- Send Messages
- Read Messages/View Channels
- Read Message History
- Embed Links
- Use Slash Commands

## Deployment Environment

**Replit**: Designed for Replit deployment with integrated secrets management through Replit Secrets. The repository includes Replit-specific configuration for automatic bot startup via workflows.

**Python 3.11**: Uses Python 3.11.13 for async/await syntax and discord.py v2 compatibility.

# File Organization

```
/
├── bot.py                      # Main bot file with commands and events
├── database.py                 # SQLite operations and helper functions
├── loot_system.py              # Loot generation and probability calculations
├── README.md                   # Complete project documentation
├── SETUP_INSTRUCTIONS.md       # Quick setup guide for users
├── replit.md                   # This file - project memory and architecture
├── .env.example                # Template for environment variables
├── .gitignore                  # Python gitignore rules
├── pyproject.toml              # Python project configuration (auto-generated)
└── quantum_lotto.db            # SQLite database (auto-created on first run)
```

# Setup Requirements

To run this bot, users must:
1. Create a Discord bot in the Developer Portal
2. Enable Message Content Intent (REQUIRED)
3. Copy bot token to Replit Secrets as `DISCORD_TOKEN`
4. Invite bot to their server with proper permissions
5. Run the bot (workflow starts automatically)

Detailed instructions are provided in `SETUP_INSTRUCTIONS.md`.
