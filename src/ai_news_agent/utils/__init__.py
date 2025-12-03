"""
Utility functions for AI News Agent.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import json

def get_period_string() -> str:
    """Return period string in YYYY-MM format."""
    return datetime.now().strftime("%Y-%m")


def save_output(data: dict, filename: str, output_dir: str = "output") -> Path:
    """Save data to output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    filepath = output_path / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath


def load_cached_posts(period: str, output_dir: str = "output") -> Optional[list]:
    """Load cached posts if they exist."""
    filepath = Path(output_dir) / f"raw_posts_{period}.json"
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None

__all__ = ["get_period_string", "save_output", "load_cached_posts"]


