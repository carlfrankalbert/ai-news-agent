#!/usr/bin/env python3
"""
Generate HTML - Entry point
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_news_agent.generator.generate_html import main

if __name__ == "__main__":
    main()
