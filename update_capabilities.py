#!/usr/bin/env python3
"""Convenience entry point for AI Capability Monitor."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_news_agent.capability_monitor.main import main

if __name__ == "__main__":
    sys.exit(main())

