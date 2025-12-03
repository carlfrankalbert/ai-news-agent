"""
Trend Analyzer - sammenligner nåværende rankings med forrige måned
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from config import OUTPUT_DIR


def normalize_tool_name(name: str) -> str:
    """
    Normaliser verktøynavn for sammenligning.
    Fjerner versjonsnumre og normaliserer whitespace.
    """
    # Fjern versjonsnumre (f.eks. "Claude 3.5" -> "Claude")
    import re
    # Fjern versjonsnumre som "3.5", "4.0", "v2", etc.
    name = re.sub(r'\s+v?\d+\.?\d*', '', name, flags=re.IGNORECASE)
    # Normaliser whitespace
    name = ' '.join(name.split())
    return name.lower().strip()


def find_tool_in_category(tool_name: str, category: dict) -> Optional[dict]:
    """
    Finn et verktøy i en kategori basert på normalisert navn.
    Returnerer verktøyet hvis funnet, None ellers.
    """
    normalized_search = normalize_tool_name(tool_name)
    
    for item in category.get("top3", []):
        normalized_item = normalize_tool_name(item.get("name", ""))
        # Sjekk både eksakt match og delvis match (f.eks. "Claude" matcher "Claude 3.5")
        if normalized_search == normalized_item or \
           normalized_search in normalized_item or \
           normalized_item in normalized_search:
            return item
    
    return None


def load_previous_rankings(period: str) -> Optional[dict]:
    """
    Last inn forrige måneds rankings.
    """
    # Beregn forrige måned
    try:
        year, month = map(int, period.split("-"))
        prev_date = datetime(year, month, 1) - timedelta(days=1)
        prev_period = prev_date.strftime("%Y-%m")
    except:
        return None
    
    # Prøv først eksakt match
    filepath = Path(OUTPUT_DIR) / f"rankings_{prev_period}.json"
    
    # Hvis ikke funnet, prøv også med _example suffix (for testing)
    if not filepath.exists():
        example_path = Path(OUTPUT_DIR) / f"rankings_{prev_period}_example.json"
        if example_path.exists():
            filepath = example_path
        else:
            return None
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def calculate_trends(current_rankings: dict, previous_rankings: Optional[dict]) -> dict:
    """
    Beregn trender ved å sammenligne nåværende med forrige måned.
    Returnerer en dict med trend-data som kan legges til i rankings.
    """
    if not previous_rankings:
        return {
            "has_previous_data": False,
            "previous_period": None,
            "trends": {}
        }
    
    trends = {}
    previous_period = previous_rankings.get("period", "unknown")
    
    # Gå gjennom hver kategori i nåværende rankings
    for current_cat in current_rankings.get("categories", []):
        cat_slug = current_cat.get("slug", "")
        trends[cat_slug] = {}
        
        # Finn tilsvarende kategori i forrige måned
        prev_cat = None
        for pc in previous_rankings.get("categories", []):
            if pc.get("slug") == cat_slug:
                prev_cat = pc
                break
        
        if not prev_cat:
            # Ny kategori - marker alle som "new"
            for item in current_cat.get("top3", []):
                tool_name = item.get("name", "")
                trends[cat_slug][tool_name] = {
                    "status": "new",
                    "previous_rank": None,
                    "rank_change": None
                }
            continue
        
        # Sammenlign verktøy i kategorien
        for current_item in current_cat.get("top3", []):
            current_name = current_item.get("name", "")
            current_rank = current_item.get("rank", 0)
            
            # Finn samme verktøy i forrige måned
            prev_item = find_tool_in_category(current_name, prev_cat)
            
            if not prev_item:
                # Nytt verktøy
                trends[cat_slug][current_name] = {
                    "status": "new",
                    "previous_rank": None,
                    "rank_change": None
                }
            else:
                # Eksisterende verktøy - sammenlign ranking
                prev_rank = prev_item.get("rank", 0)
                rank_change = prev_rank - current_rank  # Positiv = steg opp, negativ = falt ned
                
                if rank_change > 0:
                    status = "rising"
                elif rank_change < 0:
                    status = "falling"
                else:
                    status = "stable"
                
                trends[cat_slug][current_name] = {
                    "status": status,
                    "previous_rank": prev_rank,
                    "rank_change": rank_change
                }
        
        # Sjekk om noen verktøy forsvant (var i forrige måned, ikke i nåværende)
        for prev_item in prev_cat.get("top3", []):
            prev_name = prev_item.get("name", "")
            found = False
            
            for current_item in current_cat.get("top3", []):
                if find_tool_in_category(prev_name, {"top3": [current_item]}):
                    found = True
                    break
            
            if not found:
                # Verktøy forsvant fra topp 3
                trends[cat_slug][prev_name] = {
                    "status": "disappeared",
                    "previous_rank": prev_item.get("rank", 0),
                    "rank_change": None
                }
    
    return {
        "has_previous_data": True,
        "previous_period": previous_period,
        "trends": trends
    }


def add_trends_to_rankings(rankings: dict) -> dict:
    """
    Legg til trend-data i rankings-strukturen.
    Modifiserer rankings in-place og returnerer den.
    """
    previous_rankings = load_previous_rankings(rankings.get("period", ""))
    trend_data = calculate_trends(rankings, previous_rankings)
    
    # Legg til trend_data på toppnivå
    rankings["trend_analysis"] = trend_data
    
    # Legg til trend-info i hver verktøy-item
    for cat in rankings.get("categories", []):
        cat_slug = cat.get("slug", "")
        cat_trends = trend_data.get("trends", {}).get(cat_slug, {})
        
        for item in cat.get("top3", []):
            tool_name = item.get("name", "")
            tool_trend = cat_trends.get(tool_name, {})
            
            # Legg til trend-info i item
            item["trend"] = {
                "status": tool_trend.get("status", "unknown"),
                "previous_rank": tool_trend.get("previous_rank"),
                "rank_change": tool_trend.get("rank_change")
            }
    
    return rankings


# CLI for testing
if __name__ == "__main__":
    # Test med eksempel-data
    output_dir = Path(OUTPUT_DIR)
    rankings_files = list(output_dir.glob("rankings_*.json"))
    
    if len(rankings_files) < 2:
        print("Trenger minst 2 rankings-filer for testing")
        exit(1)
    
    # Last nyeste
    latest_file = max(rankings_files, key=lambda f: f.stat().st_mtime)
    print(f"Tester med {latest_file}")
    
    with open(latest_file) as f:
        current = json.load(f)
    
    # Legg til trender
    current_with_trends = add_trends_to_rankings(current)
    
    # Print oppsummering
    print(f"\n📊 Trend-analyse for {current.get('period')}")
    print(f"   Forrige periode: {current_with_trends['trend_analysis'].get('previous_period', 'N/A')}")
    print(f"   Har forrige data: {current_with_trends['trend_analysis'].get('has_previous_data', False)}")
    
    for cat in current_with_trends.get("categories", []):
        print(f"\n🏆 {cat.get('name')}:")
        for item in cat.get("top3", []):
            trend = item.get("trend", {})
            status = trend.get("status", "unknown")
            prev_rank = trend.get("previous_rank")
            change = trend.get("rank_change")
            
            status_emoji = {
                "new": "✨",
                "rising": "📈",
                "falling": "📉",
                "stable": "➡️",
                "disappeared": "👻"
            }.get(status, "❓")
            
            change_str = ""
            if change is not None:
                if change > 0:
                    change_str = f" (+{change})"
                elif change < 0:
                    change_str = f" ({change})"
                else:
                    change_str = " (=)"
            
            prev_str = f" (var #{prev_rank})" if prev_rank else ""
            
            print(f"   {status_emoji} {item.get('name')}: {status}{prev_str}{change_str}")

