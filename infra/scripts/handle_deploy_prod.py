#!/usr/bin/env python3
"""
Handle Prod Deployment
Runs the full pipeline for production environment
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ai_news_agent.main import main
from ai_news_agent.config import OUTPUT_DIR


async def deploy_prod():
    """Run prod deployment"""
    print("🚀 Starting production deployment...")
    
    # Set environment
    os.environ["ENVIRONMENT"] = "prod"
    
    # Run main pipeline
    await main()
    
    # Archive prod data for future dev seeds
    print("\n📦 Archiving production data...")
    output_dir = Path(OUTPUT_DIR)
    
    # Find latest rankings file
    rankings_files = list(output_dir.glob("rankings_*.json"))
    if rankings_files:
        # Exclude dummy files
        rankings_files = [f for f in rankings_files if "dummy" not in f.name]
        
        if rankings_files:
            latest = max(rankings_files, key=lambda f: f.stat().st_mtime)
            
            # Load and save as prod_cache
            with open(latest) as f:
                prod_data = json.load(f)
            
            # Add archive metadata
            prod_data["archived_at"] = datetime.utcnow().isoformat() + "Z"
            
            cache_file = output_dir / "prod_cache.json"
            with open(cache_file, "w") as f:
                json.dump(prod_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Production data archived to {cache_file}")
    
    print("✅ Production deployment complete")


if __name__ == "__main__":
    asyncio.run(deploy_prod())

