"""
Loot system for Quantum Lotto Discord Bot
Handles loot generation, rarities, and instability-based probabilities
"""

import random
from typing import Tuple


# Rarity tiers with base probabilities (at 0% instability)
RARITY_TIERS = {
    "Common": {
        "emoji": "⚪",
        "base_probability": 0.60,
        "color": 0x95a5a6
    },
    "Rare": {
        "emoji": "🔵",
        "base_probability": 0.25,
        "color": 0x3498db
    },
    "Epic": {
        "emoji": "🟣",
        "base_probability": 0.10,
        "color": 0x9b59b6
    },
    "Legendary": {
        "emoji": "🟡",
        "base_probability": 0.04,
        "color": 0xf1c40f
    },
    "Mythic": {
        "emoji": "🔴",
        "base_probability": 0.008,
        "color": 0xe74c3c
    },
    "Reality Breaker": {
        "emoji": "💠",
        "base_probability": 0.002,
        "color": 0x00ffff
    }
}


# Item pools for each rarity
ITEM_POOLS = {
    "Common": [
        "Quantum Dust",
        "Broken Clock",
        "Rusty Coin",
        "Faded Photograph",
        "Mundane Stone",
        "Worn Button",
        "Ordinary Paperclip",
        "Plain Marble",
        "Standard Penny",
        "Simple Thread"
    ],
    "Rare": [
        "Glowing Crystal",
        "Mysterious Key",
        "Ancient Scroll",
        "Enchanted Ring",
        "Silver Dagger",
        "Ethereal Feather",
        "Mystic Orb",
        "Rune Stone",
        "Arcane Symbol",
        "Blessed Charm"
    ],
    "Epic": [
        "Void Fragment",
        "Temporal Shard",
        "Dimensional Gate Key",
        "Chaos Essence",
        "Stellar Crown",
        "Infinity Loop",
        "Quantum Entangler",
        "Nebula Core",
        "Warp Catalyst",
        "Astral Compass"
    ],
    "Legendary": [
        "Singularity Heart",
        "Time Fracture",
        "Reality Anchor",
        "Cosmic Thread",
        "Eternal Flame",
        "Universe Seed",
        "Dimensional Rift",
        "Probability Manipulator",
        "Fate Weaver",
        "Spacetime Fabric"
    ],
    "Mythic": [
        "Primordial Spark",
        "Omega Point",
        "Genesis Code",
        "Entropy Reversal",
        "Absolute Zero",
        "Infinite Horizon",
        "Quantum Godhood",
        "Big Bang Remnant",
        "Existential Key",
        "Multiverse Core"
    ],
    "Reality Breaker": [
        "The Impossible Thing",
        "Paradox Incarnate",
        "Laws of Physics (Broken)",
        "End of Everything",
        "Beginning After End",
        "Schrödinger's Answer",
        "Divide by Zero",
        "Fourth Wall Fragment",
        "Meta Singularity",
        "Conceptual Nullifier"
    ]
}


def calculate_adjusted_probabilities(instability: float) -> dict:
    """
    Calculate rarity probabilities based on current instability
    Higher instability = higher chance for rare items
    
    Args:
        instability: Current instability percentage (0-100)
    
    Returns:
        Dictionary of rarity -> adjusted probability
    """
    # Normalize instability to 0-1
    chaos_factor = instability / 100.0
    
    adjusted = {}
    
    # Higher instability boosts rare items, reduces common items
    # Using exponential scaling for dramatic effects at high instability
    for rarity, data in RARITY_TIERS.items():
        base = data["base_probability"]
        
        if rarity == "Common":
            # Common items become less likely as chaos increases
            adjusted[rarity] = base * (1 - 0.7 * chaos_factor)
        elif rarity == "Rare":
            # Rare items get slight boost
            adjusted[rarity] = base * (1 + 0.5 * chaos_factor)
        elif rarity == "Epic":
            # Epic gets moderate boost
            adjusted[rarity] = base * (1 + 1.5 * chaos_factor)
        elif rarity == "Legendary":
            # Legendary gets significant boost
            adjusted[rarity] = base * (1 + 3.0 * chaos_factor)
        elif rarity == "Mythic":
            # Mythic gets huge boost
            adjusted[rarity] = base * (1 + 6.0 * chaos_factor)
        elif rarity == "Reality Breaker":
            # Reality Breaker becomes much more likely at high chaos
            adjusted[rarity] = base * (1 + 15.0 * chaos_factor)
    
    # Normalize to ensure probabilities sum to 1.0
    total = sum(adjusted.values())
    for rarity in adjusted:
        adjusted[rarity] /= total
    
    return adjusted


def generate_loot(instability: float) -> Tuple[str, str]:
    """
    Generate a random loot item based on current instability
    
    Args:
        instability: Current instability percentage (0-100)
    
    Returns:
        Tuple of (item_name, rarity)
    """
    # Get adjusted probabilities
    probabilities = calculate_adjusted_probabilities(instability)
    
    # Select rarity based on weighted random
    rarities = list(probabilities.keys())
    weights = [probabilities[r] for r in rarities]
    selected_rarity = random.choices(rarities, weights=weights, k=1)[0]
    
    # Select random item from that rarity's pool
    item_name = random.choice(ITEM_POOLS[selected_rarity])
    
    return item_name, selected_rarity


def get_rarity_info(rarity: str) -> dict:
    """Get emoji and color for a rarity tier"""
    return RARITY_TIERS.get(rarity, {
        "emoji": "❓",
        "color": 0x95a5a6
    })


def format_probability_display(instability: float) -> str:
    """
    Format probability display for current instability
    Shows percentage chance for each rarity tier
    """
    probabilities = calculate_adjusted_probabilities(instability)
    
    lines = []
    for rarity in ["Common", "Rare", "Epic", "Legendary", "Mythic", "Reality Breaker"]:
        emoji = RARITY_TIERS[rarity]["emoji"]
        prob = probabilities[rarity] * 100
        lines.append(f"{emoji} **{rarity}**: {prob:.2f}%")
    
    return "\n".join(lines)


def get_instability_level_description(instability: float) -> Tuple[str, str]:
    """
    Get flavor text description for current instability level
    Returns (title, description)
    """
    if instability < 20:
        return "Stable Universe", "Reality is holding together... for now. ⚛️"
    elif instability < 40:
        return "Minor Fluctuations", "Space-time is getting wobbly. 🌀"
    elif instability < 60:
        return "Quantum Turbulence", "The fabric of reality is trembling! 💫"
    elif instability < 80:
        return "Critical Instability", "Reality is fracturing at the seams! ⚡"
    elif instability < 95:
        return "IMMINENT COLLAPSE", "The universe hangs by a thread! 🔥"
    else:
        return "🚨 REALITY FAILURE 🚨", "TOTAL COLLAPSE APPROACHING! ☠️"
