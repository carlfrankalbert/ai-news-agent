#!/usr/bin/env python3
"""
Link checker - Entry point
"""
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_news_agent.utils.link_checker import main

if __name__ == "__main__":
    asyncio.run(main())

