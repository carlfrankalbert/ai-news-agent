#!/usr/bin/env python3
"""
AI News Agent MVP
==================
Samler AI-verktøy-mentions fra Hacker News og rangerer dem med Claude.

Bruk:
    python main.py                    # Kjør full pipeline
    python main.py --collect-only     # Bare samle data
    python main.py --analyze-only     # Bare analyser (krever eksisterende data)
    python main.py --days 30          # Override antall dager
"""
import argparse
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from collectors import (
    collect_from_hackernews,
    collect_from_reddit,
    collect_from_producthunt,
)
from analyzer import analyze_with_claude, validate_rankings
from config import OUTPUT_DIR, LOOKBACK_DAYS


def get_period_string() -> str:
    """Returner periode-string i YYYY-MM format."""
    return datetime.now().strftime("%Y-%m")


def save_output(data: dict, filename: str) -> Path:
    """Lagre data til output-mappe."""
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    
    filepath = output_path / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath


def load_cached_posts(period: str):
    """Last inn cached posts hvis de finnes."""
    filepath = Path(OUTPUT_DIR) / f"raw_posts_{period}.json"
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    return None


async def run_collection(days: int = LOOKBACK_DAYS):
    """Kjør datainnsamling fra alle kilder."""
    print(f"📡 Samler data fra alle kilder (siste {days} dager)...")
    print("=" * 60)
    
    all_posts = []
    sources_scanned = []
    
    # 1. Hacker News
    try:
        print("\n🔹 Hacker News...")
        hn_posts = await collect_from_hackernews(days_back=days)
        all_posts.extend(hn_posts)
        sources_scanned.append("hackernews")
        print(f"   ✅ {len(hn_posts)} posts fra Hacker News")
    except Exception as e:
        print(f"   ❌ Feil ved Hacker News: {e}")
    
    # 2. Reddit
    try:
        print("\n🔹 Reddit...")
        reddit_posts = await collect_from_reddit(days_back=days)
        all_posts.extend(reddit_posts)
        sources_scanned.append("reddit")
        print(f"   ✅ {len(reddit_posts)} posts fra Reddit")
    except Exception as e:
        print(f"   ❌ Feil ved Reddit: {e}")
    
    # 3. Product Hunt
    try:
        print("\n🔹 Product Hunt...")
        ph_posts = await collect_from_producthunt(days_back=days)
        all_posts.extend(ph_posts)
        sources_scanned.append("producthunt")
        print(f"   ✅ {len(ph_posts)} posts fra Product Hunt")
    except Exception as e:
        print(f"   ❌ Feil ved Product Hunt: {e}")
    
    # Deduplicate basert på URL eller title
    seen = set()
    unique_posts = []
    for post in all_posts:
        # Bruk URL som primary key, fallback til title
        key = post.get("url", "") or post.get("title", "").lower()
        if key and key not in seen:
            seen.add(key)
            unique_posts.append(post)
    
    # Sorter etter points (kombinert score)
    unique_posts.sort(key=lambda x: x.get("points", 0), reverse=True)
    
    print("\n" + "=" * 60)
    print(f"✅ Totalt {len(unique_posts)} unike AI-relaterte posts")
    print(f"   Kilder: {', '.join(sources_scanned)}")
    if unique_posts:
        top_post = unique_posts[0]
        print(f"   Topp post: [{top_post.get('points', 0)} pts] {top_post.get('title', '')[:50]}...")
        print(f"   Kilde: {top_post.get('source', 'unknown')}")
    
    return unique_posts


def run_analysis(posts, period: str):
    """Kjør Claude-analyse på innsamlet data."""
    print(f"\n🤖 Analyserer {len(posts)} posts med Claude...")
    
    rankings = analyze_with_claude(posts, period)
    
    # Valider output
    is_valid, issues = validate_rankings(rankings)
    if not is_valid:
        print(f"⚠️  Valideringsproblemer:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ Rankings validert OK")
    
    return rankings


def print_summary(rankings):
    """Print en lesbar oppsummering av resultatene."""
    print("\n" + "="*60)
    print("📊 AI VERKTØY-RANKING")
    print("="*60)
    
    if "summary" in rankings:
        print(f"\n📝 Oppsummering: {rankings['summary']}")
    
    for cat in rankings.get("categories", []):
        print(f"\n🏆 {cat['name']}")
        print("-" * 40)
        
        medals = {"gold": "🥇", "silver": "🥈", "bronze": "🥉"}
        
        for item in cat.get("top3", []):
            medal = medals.get(item.get("medal", ""), "  ")
            name = item.get("name", "?")
            provider = item.get("provider", "")
            reason = item.get("short_reason", "")
            print(f"{medal} {name} ({provider})")
            print(f"   {reason}")
    
    if rankings.get("new_and_noteworthy"):
        print(f"\n✨ Nytt & spennende:")
        print("-" * 40)
        for item in rankings["new_and_noteworthy"]:
            print(f"• {item['name']} ({item.get('provider', '')}) - {item.get('short_reason', '')}")


async def main():
    parser = argparse.ArgumentParser(description="AI News Agent MVP")
    parser.add_argument("--collect-only", action="store_true", help="Bare samle data, ikke analyser")
    parser.add_argument("--analyze-only", action="store_true", help="Bare analyser eksisterende data")
    parser.add_argument("--days", type=int, default=LOOKBACK_DAYS, help="Antall dager tilbake")
    parser.add_argument("--no-cache", action="store_true", help="Ignorer cached data")
    args = parser.parse_args()
    
    period = get_period_string()
    print(f"🚀 AI News Agent - Periode: {period}")
    print(f"   Lookback: {args.days} dager")
    
    # Steg 1: Samle data
    if args.analyze_only:
        posts = load_cached_posts(period)
        if not posts:
            print("❌ Ingen cached data funnet. Kjør uten --analyze-only først.")
            return
        print(f"📂 Lastet {len(posts)} cached posts")
    else:
        posts = await run_collection(days=args.days)
        
        # Cache rådata
        raw_file = save_output(posts, f"raw_posts_{period}.json")
        print(f"💾 Rådata lagret: {raw_file}")
        
        if args.collect_only:
            print("\n✅ Ferdig (collect-only mode)")
            return
    
    # Steg 2: Analyser med Claude
    rankings = run_analysis(posts, period)
    
    # Steg 3: Lagre output
    output_file = save_output(rankings, f"rankings_{period}.json")
    print(f"💾 Rankings lagret: {output_file}")
    
    # Steg 4: Print oppsummering
    print_summary(rankings)
    
    print(f"\n✅ Ferdig! Se {output_file} for full JSON.")


if __name__ == "__main__":
    asyncio.run(main())
