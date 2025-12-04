#!/usr/bin/env python3
"""
Coding Assistant Scoring Agent
Automatically scores and ranks AI coding assistant tools
"""
import asyncio
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .config import (
    CODING_ASSISTANTS,
    LOOKBACK_DAYS,
    RAW_DATA_DIR,
    SCORES_DATA_DIR,
    OUTPUT_DIR
)
from .fetchers.github import fetch_all_github_stats
from .fetchers.hackernews import fetch_all_hn_mentions
from .fetchers.reddit import fetch_all_reddit_mentions
from .analyzers.sentiment import analyze_sentiment_batch, normalize_sentiment
from .analyzers.scoring import (
    calculate_buzz_score,
    calculate_sentiment_score,
    calculate_utility_score,
    calculate_price_score,
    calculate_final_score
)


async def fetch_all_data(tools: List[Dict], days_back: int = 30) -> Dict[str, Dict]:
    """
    Fetch all data from all sources.
    
    Returns:
        {
            "tool_name": {
                "github": {...},
                "hn": {...},
                "reddit": {...}
            }
        }
    """
    print("=" * 60)
    print("📡 Fetching data from all sources...")
    print("=" * 60)
    
    # Fetch GitHub data
    print("\n1️⃣  GitHub API")
    github_results = await fetch_all_github_stats(tools, cache_dir=RAW_DATA_DIR)
    
    # Fetch HN data
    print("\n2️⃣  Hacker News API")
    hn_results = await fetch_all_hn_mentions(tools, days_back=days_back)
    
    # Fetch Reddit data
    print("\n3️⃣  Reddit API")
    reddit_results = await fetch_all_reddit_mentions(tools, days_back=days_back)
    
    # Combine all data
    all_data = {}
    for tool in tools:
        name = tool["name"]
        all_data[name] = {
            "github": github_results.get(name, {}),
            "hn": hn_results.get(name, {}),
            "reddit": reddit_results.get(name, {})
        }
    
    return all_data


def analyze_sentiments(all_data: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Analyze sentiments for all tools.
    
    Returns:
        {
            "tool_name": {
                "hn_sentiment": float,
                "reddit_sentiment": float
            }
        }
    """
    print("\n" + "=" * 60)
    print("💭 Analyzing sentiments...")
    print("=" * 60)
    
    sentiments = {}
    
    for tool_name, data in all_data.items():
        print(f"\n📊 Analyzing {tool_name}...")
        
        # HN sentiment
        hn_comments = data.get("hn", {}).get("comments", [])
        hn_sentiment_raw = analyze_sentiment_batch(hn_comments)
        hn_sentiment = normalize_sentiment(hn_sentiment_raw)
        
        # Reddit sentiment
        reddit_comments = data.get("reddit", {}).get("comments", [])
        reddit_sentiment_raw = analyze_sentiment_batch(reddit_comments)
        reddit_sentiment = normalize_sentiment(reddit_sentiment_raw)
        
        sentiments[tool_name] = {
            "hn_sentiment": hn_sentiment,
            "reddit_sentiment": reddit_sentiment
        }
        
        print(f"  ✅ HN: {hn_sentiment:.2f}, Reddit: {reddit_sentiment:.2f}")
    
    return sentiments


def calculate_scores(
    all_data: Dict[str, Dict],
    sentiments: Dict[str, Dict]
) -> List[Dict]:
    """
    Calculate all scores for all tools.
    
    Returns:
        List of tool scores with rankings
    """
    print("\n" + "=" * 60)
    print("📊 Calculating scores...")
    print("=" * 60)
    
    # Prepare data for percentile calculations
    all_tools_data = []
    for tool_name, data in all_data.items():
        all_tools_data.append({
            "name": tool_name,
            "github": data.get("github", {}),
            "hn": data.get("hn", {}),
            "reddit": data.get("reddit", {})
        })
    
    # Calculate scores for each tool
    tool_scores = []
    
    for tool in CODING_ASSISTANTS:
        tool_name = tool["name"]
        print(f"\n📈 Calculating scores for {tool_name}...")
        
        data = all_data.get(tool_name, {})
        sentiment_data = sentiments.get(tool_name, {})
        
        # Calculate component scores
        buzz = calculate_buzz_score(
            tool_name,
            data.get("github", {}),
            data.get("hn", {}),
            data.get("reddit", {}),
            all_tools_data
        )
        
        sentiment = calculate_sentiment_score(
            tool_name,
            data.get("github", {}),
            data.get("hn", {}),
            data.get("reddit", {}),
            sentiment_data.get("hn_sentiment", 0.5),
            sentiment_data.get("reddit_sentiment", 0.5)
        )
        
        utility = calculate_utility_score(tool_name)
        price = calculate_price_score(tool_name)
        
        # Calculate final score
        final_score = calculate_final_score(buzz, sentiment, utility, price)
        
        tool_scores.append({
            "name": tool_name,
            "company": tool.get("company", ""),
            "final_score": round(final_score, 1),
            "buzz": round(buzz, 1),
            "sentiment": round(sentiment, 1),
            "utility": round(utility, 1),
            "price": round(price, 1),
            "github_url": tool.get("github_url", ""),
            "website": tool.get("website", "")
        })
        
        print(f"  ✅ Final: {final_score:.1f} (Buzz: {buzz:.1f}, Sentiment: {sentiment:.1f}, Utility: {utility:.1f}, Price: {price:.1f})")
    
    # Sort by final score and add rankings
    tool_scores.sort(key=lambda x: x["final_score"], reverse=True)
    
    for i, tool in enumerate(tool_scores, 1):
        tool["rank"] = i
    
    return tool_scores


def save_raw_data(all_data: Dict[str, Dict], date_str: str):
    """Save raw API responses."""
    raw_file = RAW_DATA_DIR / f"{date_str}_raw.json"
    with open(raw_file, "w") as f:
        json.dump(all_data, f, indent=2, default=str)
    print(f"\n💾 Raw data saved: {raw_file}")


def save_scores(scores: List[Dict], date_str: str):
    """Save calculated scores."""
    scores_file = SCORES_DATA_DIR / f"{date_str}_scores.json"
    with open(scores_file, "w") as f:
        json.dump(scores, f, indent=2)
    print(f"💾 Scores saved: {scores_file}")


def save_rankings(scores: List[Dict]):
    """Save final rankings."""
    rankings = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "tools": scores
    }
    
    rankings_file = OUTPUT_DIR / "coding_assistants_rankings.json"
    with open(rankings_file, "w") as f:
        json.dump(rankings, f, indent=2)
    print(f"💾 Rankings saved: {rankings_file}")


async def main(tool_name: Optional[str] = None, days_back: int = LOOKBACK_DAYS):
    """
    Main entry point.
    
    Args:
        tool_name: Optional tool name to process (if None, process all)
        days_back: Number of days to look back
    """
    print("🚀 Coding Assistant Scoring Agent")
    print("=" * 60)
    
    # Filter tools if specific tool requested
    tools = CODING_ASSISTANTS
    if tool_name:
        tools = [t for t in CODING_ASSISTANTS if t["name"].lower() == tool_name.lower()]
        if not tools:
            print(f"❌ Tool '{tool_name}' not found")
            return
    
    print(f"📋 Processing {len(tools)} tool(s)")
    print(f"📅 Lookback period: {days_back} days")
    
    # Fetch all data
    all_data = await fetch_all_data(tools, days_back=days_back)
    
    # Analyze sentiments
    sentiments = analyze_sentiments(all_data)
    
    # Calculate scores
    scores = calculate_scores(all_data, sentiments)
    
    # Save outputs
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_raw_data(all_data, date_str)
    save_scores(scores, date_str)
    save_rankings(scores)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 FINAL RANKINGS")
    print("=" * 60)
    for tool in scores:
        print(f"{tool['rank']}. {tool['name']} - Score: {tool['final_score']:.1f}")
        print(f"   (Buzz: {tool['buzz']:.1f}, Sentiment: {tool['sentiment']:.1f}, Utility: {tool['utility']:.1f}, Price: {tool['price']:.1f})")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coding Assistant Scoring Agent")
    parser.add_argument("--tool", type=str, help="Process specific tool only")
    parser.add_argument("--days", type=int, default=LOOKBACK_DAYS, help="Lookback period in days")
    
    args = parser.parse_args()
    
    asyncio.run(main(tool_name=args.tool, days_back=args.days))


