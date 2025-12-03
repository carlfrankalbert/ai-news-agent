#!/usr/bin/env python3
"""
AI News Agent - Entry point
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_news_agent.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
