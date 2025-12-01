"""
Hacker News data collector using Firebase API
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
from config import HN_API_BASE, AI_KEYWORDS, MIN_HN_POINTS, LOOKBACK_DAYS


async def fetch_story_ids(endpoint: str = "topstories", limit: int = 500) -> List[int]:
    """
    Hent story IDs fra HN Firebase API.
    
    Args:
        endpoint: topstories, newstories, beststories
        limit: Maks antall IDs
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{HN_API_BASE}/{endpoint}.json",
            timeout=30.0
        )
        response.raise_for_status()
        ids = response.json()
        return ids[:limit] if ids else []


async def fetch_story(story_id: int, client: httpx.AsyncClient) -> Optional[Dict]:
    """Hent detaljer for én story."""
    try:
        response = await client.get(
            f"{HN_API_BASE}/item/{story_id}.json",
            timeout=10.0
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


async def collect_ai_mentions(days_back: int = LOOKBACK_DAYS, max_stories: int = 500) -> List[Dict]:
    """
    Samle AI-relaterte posts fra Hacker News via Firebase API.
    
    Henter top/best/new stories og filtrerer på AI-relevans.
    
    Returns:
        Liste med AI-relaterte posts, sortert etter points
    """
    cutoff_time = datetime.now() - timedelta(days=days_back)
    cutoff_timestamp = cutoff_time.timestamp()
    
    # Samle story IDs fra ulike endpoints
    all_ids = set()
    for endpoint in ["topstories", "beststories", "newstories"]:
        try:
            ids = await fetch_story_ids(endpoint, limit=max_stories)
            all_ids.update(ids)
            print(f"   Hentet {len(ids)} fra {endpoint}")
        except Exception as e:
            print(f"   Feil ved {endpoint}: {e}")
    
    print(f"   Totalt {len(all_ids)} unike story IDs")
    
    # Hent detaljer for hver story (med batching)
    ai_posts = []
    batch_size = 50
    ids_list = list(all_ids)
    
    async with httpx.AsyncClient() as client:
        for i in range(0, len(ids_list), batch_size):
            batch = ids_list[i:i+batch_size]
            tasks = [fetch_story(sid, client) for sid in batch]
            results = await asyncio.gather(*tasks)
            
            for story in results:
                if story is None:
                    continue
                
                # Filtrer på tid
                story_time = story.get("time", 0)
                if story_time < cutoff_timestamp:
                    continue
                
                # Filtrer på points
                if story.get("score", 0) < MIN_HN_POINTS:
                    continue
                
                # Filtrer på AI-relevans
                if is_ai_relevant(story):
                    ai_posts.append(normalize_post(story))
            
            # Progress
            if (i + batch_size) % 200 == 0:
                print(f"   Prosessert {i + batch_size}/{len(ids_list)} stories...")
            
            await asyncio.sleep(0.1)  # Rate limit
    
    # Sorter etter points
    ai_posts.sort(key=lambda x: x["points"], reverse=True)
    
    return ai_posts


def normalize_post(raw: Dict) -> Dict:
    """
    Normaliser HN-post til vårt format.
    """
    story_id = raw.get("id", "")
    created_time = raw.get("time", 0)
    
    if created_time:
        created_date = datetime.fromtimestamp(created_time).isoformat()
    else:
        created_date = ""
    
    return {
        "id": str(story_id),
        "title": raw.get("title", ""),
        "url": raw.get("url", ""),
        "hn_url": f"https://news.ycombinator.com/item?id={story_id}",
        "points": raw.get("score", 0),
        "num_comments": raw.get("descendants", 0),
        "author": raw.get("by", ""),
        "created_at": created_date,
        "source": "hackernews",
    }


def is_ai_relevant(story: Dict) -> bool:
    """
    Sjekk om en story er AI-relevant basert på keywords.
    """
    title = (story.get("title") or "").lower()
    url = (story.get("url") or "").lower()
    
    text_to_check = f"{title} {url}"
    
    return any(kw.lower() in text_to_check for kw in AI_KEYWORDS)


# CLI for testing
if __name__ == "__main__":
    async def main():
        print("Samler AI-relaterte posts fra Hacker News...")
        posts = await collect_ai_mentions(days_back=90, max_stories=500)
        print(f"\nFant {len(posts)} AI-relaterte posts")
        
        print("\nTopp 10 etter points:")
        for i, post in enumerate(posts[:10], 1):
            print(f"{i}. [{post['points']} pts] {post['title'][:60]}...")
        
        # Lagre rådata
        with open("hn_raw_data.json", "w") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"\nLagret til hn_raw_data.json")
    
    asyncio.run(main())
