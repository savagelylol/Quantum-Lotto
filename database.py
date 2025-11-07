"""
Database module for Quantum Lotto Discord Bot
Handles all SQLite operations for users, loot, and universe state
"""

import aiosqlite
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import random

DATABASE_PATH = "quantum_lotto.db"


async def initialize_database():
    """Create all necessary tables for the bot"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Users table - stores credits and stats
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                credits INTEGER DEFAULT 10,
                total_pulls INTEGER DEFAULT 0,
                total_stabilizations INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Loot items table - stores user inventories
        await db.execute("""
            CREATE TABLE IF NOT EXISTS loot_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                rarity TEXT NOT NULL,
                acquired_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Universe state table - stores global instability and collapse info
        await db.execute("""
            CREATE TABLE IF NOT EXISTS universe_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                instability REAL DEFAULT 0.0,
                last_collapse TEXT,
                collapse_count INTEGER DEFAULT 0,
                total_messages INTEGER DEFAULT 0
            )
        """)
        
        # Initialize universe state if not exists
        await db.execute("""
            INSERT OR IGNORE INTO universe_state (id, instability, last_collapse, collapse_count)
            VALUES (1, 0.0, NULL, 0)
        """)
        
        await db.commit()
        print("✅ Database initialized successfully")


async def get_or_create_user(user_id: int, username: str) -> Dict:
    """Get user data or create new user with starting credits"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # Try to get existing user
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
        
        # Create new user with 10 starting credits
        await db.execute(
            """INSERT INTO users (user_id, username, credits) 
               VALUES (?, ?, 10)""",
            (user_id, username)
        )
        await db.commit()
        
        # Return new user data
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else {}


async def update_user_credits(user_id: int, credits_change: int) -> int:
    """Update user credits and return new balance"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET credits = credits + ? WHERE user_id = ?",
            (credits_change, user_id)
        )
        await db.commit()
        
        async with db.execute(
            "SELECT credits FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def increment_user_stat(user_id: int, stat_name: str):
    """Increment a user statistic (total_pulls, total_stabilizations)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            f"UPDATE users SET {stat_name} = {stat_name} + 1 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()


async def add_loot_item(user_id: int, item_name: str, rarity: str):
    """Add a loot item to user's inventory"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """INSERT INTO loot_items (user_id, item_name, rarity)
               VALUES (?, ?, ?)""",
            (user_id, item_name, rarity)
        )
        await db.commit()


async def get_user_inventory(user_id: int) -> List[Dict]:
    """Get all loot items for a user, grouped by rarity"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT item_name, rarity, acquired_at 
               FROM loot_items 
               WHERE user_id = ? 
               ORDER BY 
                   CASE rarity
                       WHEN 'Reality Breaker' THEN 1
                       WHEN 'Mythic' THEN 2
                       WHEN 'Legendary' THEN 3
                       WHEN 'Epic' THEN 4
                       WHEN 'Rare' THEN 5
                       WHEN 'Common' THEN 6
                   END,
                   acquired_at DESC""",
            (user_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_inventory_count(user_id: int) -> int:
    """Get total count of items in user's inventory"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM loot_items WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def get_instability() -> float:
    """Get current universe instability percentage"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT instability FROM universe_state WHERE id = 1"
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0.0


async def update_instability(change: float) -> float:
    """Update instability by a change amount, clamped to 0-100"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Get current instability
        async with db.execute(
            "SELECT instability FROM universe_state WHERE id = 1"
        ) as cursor:
            row = await cursor.fetchone()
            current = row[0] if row else 0.0
        
        # Calculate new instability (clamped to 0-100)
        new_instability = max(0.0, min(100.0, current + change))
        
        # Update in database
        await db.execute(
            "UPDATE universe_state SET instability = ? WHERE id = 1",
            (new_instability,)
        )
        await db.commit()
        
        return new_instability


async def increment_message_count():
    """Increment total message counter"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE universe_state SET total_messages = total_messages + 1 WHERE id = 1"
        )
        await db.commit()


async def get_universe_state() -> Dict:
    """Get complete universe state"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM universe_state WHERE id = 1"
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else {}


async def trigger_collapse() -> Tuple[int, int]:
    """
    Trigger a universe collapse event
    Randomly removes 50-80% of all loot items
    Returns (items_removed, total_items_before)
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Get total item count before collapse
        async with db.execute("SELECT COUNT(*) FROM loot_items") as cursor:
            row = await cursor.fetchone()
            total_items = row[0] if row else 0
        
        if total_items == 0:
            # No items to remove, just reset instability
            await db.execute(
                """UPDATE universe_state 
                   SET instability = 0.0, 
                       last_collapse = ?, 
                       collapse_count = collapse_count + 1
                   WHERE id = 1""",
                (datetime.utcnow().isoformat(),)
            )
            await db.commit()
            return 0, 0
        
        # Get all loot item IDs
        async with db.execute("SELECT id FROM loot_items") as cursor:
            rows = await cursor.fetchall()
            all_ids = [row[0] for row in rows]
        
        # Randomly select 50-80% to remove
        removal_percentage = random.uniform(0.5, 0.8)
        items_to_remove = int(total_items * removal_percentage)
        ids_to_remove = random.sample(all_ids, items_to_remove)
        
        # Delete selected items
        if ids_to_remove:
            placeholders = ','.join('?' * len(ids_to_remove))
            await db.execute(
                f"DELETE FROM loot_items WHERE id IN ({placeholders})",
                ids_to_remove
            )
        
        # Update universe state
        await db.execute(
            """UPDATE universe_state 
               SET instability = 0.0, 
                   last_collapse = ?, 
                   collapse_count = collapse_count + 1
               WHERE id = 1""",
            (datetime.utcnow().isoformat(),)
        )
        
        await db.commit()
        return items_to_remove, total_items


async def get_top_looters(limit: int = 10) -> List[Dict]:
    """Get top users by total loot count"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT u.username, u.user_id, COUNT(l.id) as loot_count
               FROM users u
               LEFT JOIN loot_items l ON u.user_id = l.user_id
               GROUP BY u.user_id
               HAVING loot_count > 0
               ORDER BY loot_count DESC
               LIMIT ?""",
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_rarity_counts(user_id: int) -> Dict[str, int]:
    """Get count of items by rarity for a user"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT rarity, COUNT(*) as count
               FROM loot_items
               WHERE user_id = ?
               GROUP BY rarity""",
            (user_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return {row['rarity']: row['count'] for row in rows}
