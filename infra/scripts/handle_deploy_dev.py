#!/usr/bin/env python3
"""
Handle Dev Deployment
Runs the full pipeline for development environment
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ai_news_agent.main import main
import asyncio


async def deploy_dev():
    """Run dev deployment"""
    print("🚀 Starting dev deployment...")
    
    # Set environment
    os.environ["ENVIRONMENT"] = "dev"
    
    # Run main pipeline
    await main()
    
    print("✅ Dev deployment complete")


if __name__ == "__main__":
    asyncio.run(deploy_dev())

