"""
Configuration for Coding Assistant Scoring
"""
from typing import Dict, List
from pathlib import Path

# Tools to track
CODING_ASSISTANTS = [
    {
        "name": "Cursor",
        "company": "Anysphere",
        "github_owner": "getcursor",
        "github_repo": "cursor",
        "website": "https://cursor.sh",
        "github_url": "https://github.com/getcursor/cursor"
    },
    {
        "name": "GitHub Copilot",
        "company": "GitHub",
        "github_owner": None,  # No public repo
        "github_repo": None,
        "website": "https://github.com/features/copilot",
        "github_url": None
    },
    {
        "name": "Continue",
        "company": "Continue",
        "github_owner": "continuedev",
        "github_repo": "continue",
        "website": "https://continue.dev",
        "github_url": "https://github.com/continuedev/continue"
    },
    {
        "name": "Cody",
        "company": "Sourcegraph",
        "github_owner": "sourcegraph",
        "github_repo": "cody",
        "website": "https://sourcegraph.com/cody",
        "github_url": "https://github.com/sourcegraph/cody"
    },
    {
        "name": "Aider",
        "company": "Aider",
        "github_owner": "paul-gauthier",
        "github_repo": "aider",
        "website": "https://aider.chat",
        "github_url": "https://github.com/paul-gauthier/aider"
    },
    {
        "name": "Supermaven",
        "company": "Supermaven",
        "github_owner": "supermaven-inc",
        "github_repo": "supermaven-vscode",
        "website": "https://supermaven.com",
        "github_url": "https://github.com/supermaven-inc/supermaven-vscode"
    }
]

# Scoring weights
SCORING_WEIGHTS = {
    "buzz": 0.30,
    "sentiment": 0.25,
    "utility": 0.25,
    "price": 0.20
}

# Buzz score sub-weights
BUZZ_WEIGHTS = {
    "github_stars": 0.4,
    "github_stars_growth": 0.3,
    "hn_mentions": 0.15,
    "reddit_mentions": 0.15
}

# Sentiment score sub-weights
SENTIMENT_WEIGHTS = {
    "github_issue_health": 0.3,
    "hn_sentiment": 0.35,
    "reddit_sentiment": 0.35
}

# API settings
GITHUB_API_BASE = "https://api.github.com"
HN_ALGOLIA_API = "https://hn.algolia.com/api/v1"
REDDIT_API_BASE = "https://www.reddit.com"

# Reddit subreddits to search
REDDIT_SUBREDDITS = ["programming", "vscode", "neovim", "coding"]

# Data directories
BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "coding_assistants"
RAW_DATA_DIR = DATA_DIR / "raw"
SCORES_DATA_DIR = DATA_DIR / "scores"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
SCORES_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Data files
FEATURES_FILE = DATA_DIR / "features.json"
PRICING_FILE = DATA_DIR / "pricing.json"

# Lookback period (days)
LOOKBACK_DAYS = 30

