"""
Reddit data collector for AI tools mentions
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
from config import AI_KEYWORDS, LOOKBACK_DAYS

# Reddit subreddits å skanne
REDDIT_SUBREDDITS = [
    "MachineLearning",
    "LocalLLaMA",
    "artificial",
    "ChatGPT",
    "OpenAI",
    "singularity",
    "agi",
    "learnmachinelearning",
]

# Reddit API (gratis, ingen auth nødvendig for public data)
REDDIT_API_BASE = "https://www.reddit.com/r"

# Minimum upvotes for å inkludere en post
MIN_REDDIT_UPVOTES = 10


async def fetch_subreddit_posts(
    subreddit: str,
    sort: str = "top",
    time_period: str = "month",
    limit: int = 100,
    client: Optional[httpx.AsyncClient] = None
) -> List[Dict]:
    """
    Hent posts fra en subreddit.
    
    Args:
        subreddit: Subreddit navn (uten r/)
        sort: top, hot, new, rising
        time_period: all, year, month, week, day (kun for top)
        limit: Maks antall posts (max 100)
    """
    if client is None:
        async with httpx.AsyncClient() as client:
            return await fetch_subreddit_posts(subreddit, sort, time_period, limit, client)
    
    url = f"{REDDIT_API_BASE}/{subreddit}/{sort}.json"
    params = {
        "limit": min(limit, 100),
        "t": time_period if sort == "top" else None,
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    # Reddit krever User-Agent header
    headers = {
        "User-Agent": "AI-News-Agent/1.0 (by /u/fyrk-agent)"
    }
    
    try:
        response = await client.get(url, params=params, headers=headers, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        
        posts = []
        for child in data.get("data", {}).get("children", []):
            post_data = child.get("data", {})
            posts.append(post_data)
        
        return posts
    except Exception as e:
        print(f"   Feil ved henting fra r/{subreddit}: {e}")
        return []


async def collect_ai_mentions(days_back: int = LOOKBACK_DAYS) -> List[Dict]:
    """
    Samle AI-relaterte posts fra Reddit.
    
    Returns:
        Liste med AI-relaterte posts, sortert etter upvotes
    """
    cutoff_time = datetime.now() - timedelta(days=days_back)
    cutoff_timestamp = cutoff_time.timestamp()
    
    print(f"📡 Samler data fra Reddit (siste {days_back} dager)...")
    print(f"   Subreddits: {', '.join([f'r/{s}' for s in REDDIT_SUBREDDITS])}")
    
    all_posts = []
    
    async with httpx.AsyncClient() as client:
        for subreddit in REDDIT_SUBREDDITS:
            try:
                # Hent både top og hot posts
                top_posts = await fetch_subreddit_posts(
                    subreddit, sort="top", time_period="month", limit=100, client=client
                )
                hot_posts = await fetch_subreddit_posts(
                    subreddit, sort="hot", limit=50, client=client
                )
                
                # Kombiner og deduplicate
                seen_ids = set()
                for post in top_posts + hot_posts:
                    post_id = post.get("id")
                    if post_id and post_id not in seen_ids:
                        seen_ids.add(post_id)
                        all_posts.append(post)
                
                print(f"   r/{subreddit}: {len(top_posts)} top + {len(hot_posts)} hot")
                
                # Rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"   Feil ved r/{subreddit}: {e}")
                continue
    
    print(f"   Totalt {len(all_posts)} unike posts hentet")
    
    # Filtrer på relevans og kvalitet
    ai_posts = []
    for post in all_posts:
        # Filtrer på tid
        created_time = post.get("created_utc", 0)
        if created_time < cutoff_timestamp:
            continue
        
        # Filtrer på upvotes
        upvotes = post.get("ups", 0)
        if upvotes < MIN_REDDIT_UPVOTES:
            continue
        
        # Filtrer på AI-relevans
        if is_ai_relevant(post):
            ai_posts.append(normalize_post(post))
    
    # Sorter etter upvotes
    ai_posts.sort(key=lambda x: x["points"], reverse=True)
    
    print(f"✅ Fant {len(ai_posts)} AI-relaterte posts fra Reddit")
    
    return ai_posts


def normalize_post(raw: Dict) -> Dict:
    """
    Normaliser Reddit-post til vårt format.
    """
    post_id = raw.get("id", "")
    created_time = raw.get("created_utc", 0)
    
    if created_time:
        created_date = datetime.fromtimestamp(created_time).isoformat()
    else:
        created_date = ""
    
    # Reddit URL
    subreddit = raw.get("subreddit", "")
    reddit_url = f"https://www.reddit.com{raw.get('permalink', '')}"
    
    return {
        "id": f"reddit_{post_id}",
        "title": raw.get("title", ""),
        "url": raw.get("url", "") or reddit_url,
        "reddit_url": reddit_url,
        "points": raw.get("ups", 0),
        "num_comments": raw.get("num_comments", 0),
        "author": raw.get("author", ""),
        "subreddit": subreddit,
        "created_at": created_date,
        "source": "reddit",
    }


def is_ai_relevant(post: Dict) -> bool:
    """
    Sjekk om en Reddit-post er AI-relevant.
    """
    title = (post.get("title") or "").lower()
    selftext = (post.get("selftext") or "").lower()
    url = (post.get("url") or "").lower()
    
    text_to_check = f"{title} {selftext} {url}"
    
    return any(kw.lower() in text_to_check for kw in AI_KEYWORDS)


# CLI for testing
if __name__ == "__main__":
    async def main():
        print("Samler AI-relaterte posts fra Reddit...")
        posts = await collect_ai_mentions(days_back=30)
        print(f"\nFant {len(posts)} AI-relaterte posts")
        
        print("\nTopp 10 etter upvotes:")
        for i, post in enumerate(posts[:10], 1):
            print(f"{i}. [{post['points']} pts] r/{post.get('subreddit', '?')} - {post['title'][:60]}...")
        
        # Lagre rådata
        with open("reddit_raw_data.json", "w") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"\nLagret til reddit_raw_data.json")
    
    asyncio.run(main())

