#!/usr/bin/env python3
"""
Entry point for Coding Assistant Scoring Agent
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_news_agent.coding_assistants.main import main
import asyncio
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coding Assistant Scoring Agent")
    parser.add_argument("--tool", type=str, help="Process specific tool only")
    parser.add_argument("--days", type=int, default=30, help="Lookback period in days")
    
    args = parser.parse_args()
    
    asyncio.run(main(tool_name=args.tool, days_back=args.days))


