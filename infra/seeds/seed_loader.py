#!/usr/bin/env python3
"""
Seed Data Loader
Loads seed data from fixed_seeds.json or prod_cache.json
"""
import json
from pathlib import Path
from typing import Optional, Dict

SEEDS_DIR = Path(__file__).parent
FIXED_SEEDS = SEEDS_DIR / "fixed_seeds.json"
PROD_CACHE = Path("output") / "prod_cache.json"


def load_seed_data() -> Optional[Dict]:
    """
    Load seed data with priority:
    1. prod_cache.json (if exists)
    2. fixed_seeds.json (fallback)
    """
    # Try prod cache first
    if PROD_CACHE.exists():
        print(f"📦 Loading seed data from {PROD_CACHE}")
        with open(PROD_CACHE) as f:
            return json.load(f)
    
    # Fallback to fixed seeds
    if FIXED_SEEDS.exists():
        print(f"📦 Loading seed data from {FIXED_SEEDS}")
        with open(FIXED_SEEDS) as f:
            return json.load(f)
    
    print("⚠️  No seed data found")
    return None


if __name__ == "__main__":
    data = load_seed_data()
    if data:
        print(f"✅ Loaded seed data: {data.get('period', 'unknown')} period")
        print(f"   Categories: {len(data.get('categories', []))}")

