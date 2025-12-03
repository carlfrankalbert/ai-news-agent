#!/usr/bin/env python3
"""
Health Check Endpoint
Returns health status for the application
"""
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


def get_git_sha() -> str:
    """Get current git commit SHA"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        if result.returncode == 0:
            return result.stdout.strip()[:7]  # Short SHA
    except:
        pass
    return "unknown"


def health_check() -> dict:
    """Perform health check"""
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
        "version": get_git_sha(),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
    }


if __name__ == "__main__":
    # For local testing
    health = health_check()
    print(json.dumps(health, indent=2))

