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

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip (will use system env vars)
    pass

from typing import List, Dict
from pathlib import Path
import json
from datetime import datetime, timedelta

from .collectors.hackernews import collect_ai_mentions
from .collectors.github import collect_github_trending
from .analyzer import analyze_with_claude, validate_rankings, add_trends_to_rankings
from .config import LOOKBACK_DAYS, OUTPUT_DIR
from .utils import get_period_string, save_output, load_cached_posts




async def run_collection(days: int = LOOKBACK_DAYS) -> List[Dict]:
    """Kjør datainnsamling fra alle kilder."""
    print(f"📡 Samler data fra Hacker News (siste {days} dager)...")
    hn_posts = await collect_ai_mentions(days_back=days)
    print(f"✅ Fant {len(hn_posts)} AI-relaterte HN posts")
    
    print(f"📡 Samler data fra GitHub Trending (siste {days} dager)...")
    github_repos = await collect_github_trending(days_back=days, max_results=100)
    print(f"✅ Fant {len(github_repos)} AI-relaterte GitHub repos")
    
    # Kombiner og sorter
    all_posts = hn_posts + github_repos
    all_posts.sort(key=lambda x: x["points"], reverse=True)
    
    print(f"📊 Totalt {len(all_posts)} AI-relaterte items fra alle kilder")
    if all_posts:
        print(f"   Topp item: [{all_posts[0]['points']} pts] {all_posts[0]['title'][:50]}...")
    
    return all_posts


def run_analysis(posts: list[dict], period: str) -> dict:
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


def print_summary(rankings: dict):
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
            
            # Vis trend hvis tilgjengelig
            trend = item.get("trend", {})
            trend_str = ""
            if trend.get("status"):
                status = trend["status"]
                status_emoji = {
                    "new": "✨",
                    "rising": "📈",
                    "falling": "📉",
                    "stable": "➡️"
                }.get(status, "")
                
                change = trend.get("rank_change")
                if change is not None and change != 0:
                    trend_str = f" {status_emoji} {'+' if change > 0 else ''}{change}"
                elif status == "new":
                    trend_str = f" {status_emoji} Nytt"
                elif status == "stable" and trend.get("previous_rank"):
                    trend_str = f" {status_emoji} Uendret (var #{trend['previous_rank']})"
            
            print(f"{medal} {name} ({provider}){trend_str}")
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
    
    # Check if analysis failed
    if rankings.get("error"):
        print(f"\n❌ Analyse feilet: {rankings.get('error')}")
        print("💡 Prøver å bruke forrige måneds data hvis tilgjengelig...")
        
        # Try to use previous month's data as fallback
        from datetime import datetime, timedelta
        try:
            year, month = map(int, period.split("-"))
            prev_date = datetime(year, month, 1) - timedelta(days=1)
            prev_period = prev_date.strftime("%Y-%m")
            prev_file = Path(OUTPUT_DIR) / f"rankings_{prev_period}.json"
            
            if prev_file.exists():
                with open(prev_file) as f:
                    prev_rankings = json.load(f)
                print(f"✅ Bruker data fra {prev_period} som fallback")
                rankings = prev_rankings
                rankings["period"] = period  # Update period
                rankings["generated_at"] = datetime.now().isoformat()
            else:
                print("⚠️  Ingen forrige måneds data tilgjengelig")
        except Exception as e:
            print(f"⚠️  Kunne ikke laste forrige måneds data: {e}")
    
    # Steg 2.5: Legg til trend-analyse (sammenlign med forrige måned)
    print("\n📊 Analyserer trender (sammenligner med forrige måned)...")
    rankings = add_trends_to_rankings(rankings)
    if rankings.get("trend_analysis", {}).get("has_previous_data"):
        prev_period = rankings["trend_analysis"]["previous_period"]
        print(f"✅ Sammenlignet med {prev_period}")
    else:
        print("ℹ️  Ingen forrige måneds data funnet (første kjøring?)")
    
    # Steg 3: Lagre output
    output_file = save_output(rankings, f"rankings_{period}.json")
    print(f"💾 Rankings lagret: {output_file}")
    
    # Steg 4: Print oppsummering
    print_summary(rankings)
    
    print(f"\n✅ Ferdig! Se {output_file} for full JSON.")


if __name__ == "__main__":
    asyncio.run(main())
