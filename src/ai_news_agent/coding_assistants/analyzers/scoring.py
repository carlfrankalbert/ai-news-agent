"""
Scoring Calculator for Coding Assistants
"""
from typing import Dict, List
import json
from pathlib import Path
from ..config import (
    SCORING_WEIGHTS,
    BUZZ_WEIGHTS,
    SENTIMENT_WEIGHTS,
    FEATURES_FILE,
    PRICING_FILE
)


def calculate_percentile(value: float, all_values: List[float]) -> float:
    """
    Calculate percentile rank (0-100) for a value.
    
    Args:
        value: The value to rank
        all_values: All values to compare against
    
    Returns:
        Percentile score (0-100)
    """
    if not all_values:
        return 0.0
    
    # Filter out None and invalid values
    valid_values = [v for v in all_values if v is not None and isinstance(v, (int, float))]
    
    if not valid_values:
        return 0.0
    
    if value is None:
        return 0.0
    
    # Count how many values are less than or equal to this value
    count_below = sum(1 for v in valid_values if v <= value)
    total = len(valid_values)
    
    # Calculate percentile
    percentile = (count_below / total) * 100
    
    return percentile


def load_features() -> Dict:
    """Load manual utility scores from features.json."""
    if not FEATURES_FILE.exists():
        print(f"⚠️  Features file not found: {FEATURES_FILE}")
        return {}
    
    try:
        with open(FEATURES_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading features file: {e}")
        return {}


def load_pricing() -> Dict:
    """Load manual pricing scores from pricing.json."""
    if not PRICING_FILE.exists():
        print(f"⚠️  Pricing file not found: {PRICING_FILE}")
        return {}
    
    try:
        with open(PRICING_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading pricing file: {e}")
        return {}


def calculate_buzz_score(
    tool_name: str,
    github_data: Dict,
    hn_data: Dict,
    reddit_data: Dict,
    all_tools_data: List[Dict]
) -> float:
    """
    Calculate buzz score (0-100).
    
    Uses percentile ranking for each metric.
    """
    # Get values for this tool
    github_stars = github_data.get("stars", 0)
    github_stars_growth = 0
    if github_data.get("stars_30d_ago") is not None:
        stars_30d_ago = github_data["stars_30d_ago"]
        current_stars = github_data["stars"]
        if stars_30d_ago > 0:
            github_stars_growth = ((current_stars - stars_30d_ago) / stars_30d_ago) * 100
    
    hn_mentions = hn_data.get("mentions_count", 0)
    reddit_mentions = reddit_data.get("mentions_count", 0)
    
    # Get all values for percentile calculation
    all_github_stars = [d.get("github", {}).get("stars", 0) for d in all_tools_data]
    all_github_growth = []
    for d in all_tools_data:
        gh = d.get("github", {})
        if gh.get("stars_30d_ago") is not None:
            stars_30d_ago = gh["stars_30d_ago"]
            current_stars = gh["stars"]
            if stars_30d_ago > 0:
                growth = ((current_stars - stars_30d_ago) / stars_30d_ago) * 100
                all_github_growth.append(growth)
    
    all_hn_mentions = [d.get("hn", {}).get("mentions_count", 0) for d in all_tools_data]
    all_reddit_mentions = [d.get("reddit", {}).get("mentions_count", 0) for d in all_tools_data]
    
    # Calculate percentiles
    stars_percentile = calculate_percentile(github_stars, all_github_stars)
    growth_percentile = calculate_percentile(github_stars_growth, all_github_growth) if all_github_growth else 0
    hn_percentile = calculate_percentile(hn_mentions, all_hn_mentions)
    reddit_percentile = calculate_percentile(reddit_mentions, all_reddit_mentions)
    
    # Weighted sum
    buzz_score = (
        stars_percentile * BUZZ_WEIGHTS["github_stars"] +
        growth_percentile * BUZZ_WEIGHTS["github_stars_growth"] +
        hn_percentile * BUZZ_WEIGHTS["hn_mentions"] +
        reddit_percentile * BUZZ_WEIGHTS["reddit_mentions"]
    )
    
    return min(100, max(0, buzz_score))


def calculate_sentiment_score(
    tool_name: str,
    github_data: Dict,
    hn_data: Dict,
    reddit_data: Dict,
    hn_sentiment: float,
    reddit_sentiment: float
) -> float:
    """
    Calculate sentiment score (0-100).
    """
    # GitHub issue health (closed/total ratio)
    open_issues = github_data.get("open_issues", 0)
    closed_issues = github_data.get("closed_issues", 0)
    total_issues = open_issues + closed_issues
    
    if total_issues > 0:
        issue_health = closed_issues / total_issues
    else:
        issue_health = 0.5  # Neutral if no issues
    
    # Normalize sentiment scores (already 0-1 from analyzer)
    hn_sentiment_norm = hn_sentiment
    reddit_sentiment_norm = reddit_sentiment
    
    # Weighted sum (convert to 0-100 scale)
    sentiment_score = (
        issue_health * SENTIMENT_WEIGHTS["github_issue_health"] +
        hn_sentiment_norm * SENTIMENT_WEIGHTS["hn_sentiment"] +
        reddit_sentiment_norm * SENTIMENT_WEIGHTS["reddit_sentiment"]
    ) * 100
    
    return min(100, max(0, sentiment_score))


def calculate_utility_score(tool_name: str) -> float:
    """
    Calculate utility score (0-100) from manual features.json.
    """
    features = load_features()
    
    if tool_name not in features:
        print(f"  ⚠️  No utility data for {tool_name}, using default 50")
        return 50.0
    
    tool_features = features[tool_name]
    
    # If there's a total score, use it
    if "total" in tool_features:
        return min(100, max(0, tool_features["total"]))
    
    # Otherwise calculate average of all feature scores
    feature_scores = [v for k, v in tool_features.items() if isinstance(v, (int, float))]
    
    if not feature_scores:
        return 50.0
    
    avg_score = sum(feature_scores) / len(feature_scores)
    return min(100, max(0, avg_score))


def calculate_price_score(tool_name: str) -> float:
    """
    Calculate price score (0-100) from manual pricing.json.
    """
    pricing = load_pricing()
    
    if tool_name not in pricing:
        print(f"  ⚠️  No pricing data for {tool_name}, using default 50")
        return 50.0
    
    tool_pricing = pricing[tool_name]
    
    # If there's a score, use it
    if "score" in tool_pricing:
        return min(100, max(0, tool_pricing["score"]))
    
    # Otherwise infer from tier
    tier = tool_pricing.get("tier", "paid").lower()
    
    tier_scores = {
        "free": 100,
        "freemium": 70,
        "paid": 40,
        "expensive": 20
    }
    
    return tier_scores.get(tier, 50)


def calculate_final_score(
    buzz: float,
    sentiment: float,
    utility: float,
    price: float
) -> float:
    """
    Calculate final weighted score (0-100).
    """
    final_score = (
        buzz * SCORING_WEIGHTS["buzz"] +
        sentiment * SCORING_WEIGHTS["sentiment"] +
        utility * SCORING_WEIGHTS["utility"] +
        price * SCORING_WEIGHTS["price"]
    )
    
    return min(100, max(0, final_score))


