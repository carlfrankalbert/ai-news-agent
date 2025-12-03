#!/usr/bin/env python3
"""
Prepare Development Data
Loads seed data and uploads to Cloudflare KV for dev environment
"""
import json
import os
import subprocess
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from infra.seeds.seed_loader import load_seed_data

KV_NAMESPACE = "dev-data"


def upload_to_kv(data: dict, namespace: str = KV_NAMESPACE):
    """Upload data to Cloudflare KV namespace"""
    print(f"📤 Uploading seed data to KV namespace: {namespace}")
    
    # Create temporary JSON file
    temp_file = Path("/tmp/seed_data.json")
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=2)
    
    try:
        # Upload using wrangler
        result = subprocess.run(
            [
                "wrangler", "kv:key", "put", "seed_data",
                "--path", str(temp_file),
                "--namespace-id", namespace,
            ],
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            print(f"❌ KV upload failed: {result.stderr}")
            return False
        
        print("✅ Seed data uploaded to KV")
        return True
        
    except FileNotFoundError:
        print("⚠️  wrangler CLI not found, skipping KV upload")
        print("   Data will be available in output/ for manual upload")
        return False
    finally:
        # Cleanup
        if temp_file.exists():
            temp_file.unlink()


def main():
    """Main function"""
    print("🔧 Preparing development data...")
    
    # Load seed data
    seed_data = load_seed_data()
    if not seed_data:
        print("❌ No seed data available")
        sys.exit(1)
    
    # Save to output for reference
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "dev_seed_data.json"
    
    with open(output_file, "w") as f:
        json.dump(seed_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Seed data saved to {output_file}")
    
    # Upload to KV if wrangler is available
    if os.getenv("CLOUDFLARE_API_TOKEN"):
        upload_to_kv(seed_data)
    else:
        print("⚠️  CLOUDFLARE_API_TOKEN not set, skipping KV upload")
    
    print("✅ Development data prepared")


if __name__ == "__main__":
    main()

