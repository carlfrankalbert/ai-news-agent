"""Main entry point for AI Capability Monitor."""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict

from .fetcher import CapabilityFetcher
from .analyzer import CapabilityAnalyzer
from .table_generator import TableGenerator


def load_previous_capabilities(filepath: str) -> Dict:
    """Load previous capability data from JSON file."""
    if not os.path.exists(filepath):
        return {}
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load previous capabilities: {e}")
        return {}


def save_capabilities_json(capabilities: Dict, filepath: str):
    """Save capabilities as JSON for future comparison."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(capabilities, f, indent=2, ensure_ascii=False)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="AI Capability Monitor - Update capability comparison table"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/capability_monitor",
        help="Directory for data files"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory for output files"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Anthropic API key (defaults to ANTHROPIC_API_KEY env var)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch data but don't save files"
    )
    
    args = parser.parse_args()
    
    # Setup directories
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    history_dir = data_dir / "history"
    
    data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)
    
    # File paths
    current_table_path = data_dir / "current_table.md"
    current_json_path = data_dir / "current_capabilities.json"
    previous_json_path = data_dir / "previous_capabilities.json"
    report_path = output_dir / "capability_report.md"
    history_path = history_dir / f"capabilities_{datetime.now().strftime('%Y-%m')}.json"
    
    print("🤖 AI Capability Monitor")
    print("=" * 50)
    
    # Load previous data
    print("\n📖 Loading previous capability data...")
    previous_capabilities = load_previous_capabilities(str(previous_json_path))
    
    # Initialize components
    print("\n🔍 Fetching latest capabilities...")
    fetcher = CapabilityFetcher(api_key=args.api_key)
    analyzer = CapabilityAnalyzer()
    generator = TableGenerator()
    
    # Fetch capabilities for all models
    print("\n📡 Fetching model capabilities...")
    capabilities = fetcher.fetch_all_capabilities()
    
    if not capabilities:
        print("❌ Error: Failed to fetch any capabilities")
        return 1
    
    print(f"✅ Fetched capabilities for {len(capabilities)} models")
    
    # Fetch benchmark results
    print("\n🏆 Fetching benchmark results...")
    benchmarks = fetcher.fetch_benchmark_results()
    
    # Merge with benchmarks
    print("\n🔗 Merging with benchmark data...")
    merged_capabilities = analyzer.merge_with_benchmarks(capabilities, benchmarks)
    
    # Validate data
    print("\n✔️ Validating data...")
    warnings = analyzer.validate_data(merged_capabilities)
    if warnings:
        print("⚠️ Validation warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    # Compare with previous
    print("\n📊 Comparing with previous version...")
    changes = analyzer.compare_with_previous(merged_capabilities, previous_capabilities)
    
    if changes:
        print(f"📝 Found {len(changes)} changes:")
        for change in changes[:5]:  # Show first 5
            print(f"  - {change}")
        if len(changes) > 5:
            print(f"  ... and {len(changes) - 5} more")
    
    # Generate outputs
    print("\n📄 Generating reports...")
    
    if not args.dry_run:
        # Save current as previous for next run
        if current_json_path.exists():
            import shutil
            shutil.copy(str(current_json_path), str(previous_json_path))
        
        # Save current capabilities as JSON
        save_capabilities_json(merged_capabilities, str(current_json_path))
        
        # Save to history
        save_capabilities_json(merged_capabilities, str(history_path))
        
        # Generate and save table
        generator.save_table(merged_capabilities, str(current_table_path))
        
        # Generate and save full report
        generator.save_report(merged_capabilities, str(report_path), changes)
        
        print(f"✅ Saved files:")
        print(f"  - {current_table_path}")
        print(f"  - {current_json_path}")
        print(f"  - {report_path}")
        print(f"  - {history_path}")
    else:
        print("🔍 Dry run - not saving files")
        print("\n" + generator.generate_table(merged_capabilities))
    
    print("\n✨ Done!")
    return 0


if __name__ == "__main__":
    exit(main())

