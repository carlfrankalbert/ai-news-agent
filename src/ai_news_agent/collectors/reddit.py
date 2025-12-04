"""
Reddit data collector using Reddit JSON API (no auth required)
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List
import json
from ..config import AI_KEYWORDS, LOOKBACK_DAYS

# Reddit API base URL (public JSON endpoint, no auth required)
REDDIT_API_BASE = "https://www.reddit.com"

# Subreddits to search for AI-related content
AI_SUBREDDITS = [
    "MachineLearning",
    "artificial",
    "LocalLLaMA",
    "OpenAI",
    "singularity",
    "ChatGPT",
    "StableDiffusion",
    "comfyui",
    "programming",
    "technology",
    "Futurology",
    "gamedev",
    "webdev",
    "learnmachinelearning",
    "deeplearning",
    "computervision",
    "nlp",
    "robotics"
]

# Minimum score for a post to be included
MIN_REDDIT_SCORE = 5


async def fetch_subreddit_posts(
    subreddit: str,
    days_back: int = LOOKBACK_DAYS,
    limit: int = 100,
    client: httpx.AsyncClient = None
) -> List[dict]:
    """
    Fetch recent posts from a subreddit.
    
    Args:
        subreddit: Subreddit name (without r/)
        days_back: How many days back to look
        limit: Maximum number of posts to fetch
        client: Optional httpx client (for reuse)
    
    Returns:
        List of posts from the subreddit
    """
    cutoff_time = datetime.now() - timedelta(days=days_back)
    cutoff_timestamp = cutoff_time.timestamp()
    
    headers = {
        "User-Agent": "AI-News-Agent/1.0 (by /u/ai-news-agent)"
    }
    
    posts = []
    
    try:
        # Fetch hot posts from subreddit
        url = f"{REDDIT_API_BASE}/r/{subreddit}/hot.json"
        params = {
            "limit": min(limit, 100)  # Reddit API max is 100 per request
        }
        
        response = await client.get(url, params=params, headers=headers, timeout=30.0)
        
        if response.status_code == 200:
            data = response.json()
            children = data.get("data", {}).get("children", [])
            
            for child in children:
                post_data = child.get("data", {})
                
                # Filter by time
                created_utc = post_data.get("created_utc", 0)
                if created_utc < cutoff_timestamp:
                    continue
                
                # Filter by score
                score = post_data.get("score", 0)
                if score < MIN_REDDIT_SCORE:
                    continue
                
                # Filter by AI relevance
                title = post_data.get("title", "").lower()
                selftext = post_data.get("selftext", "").lower()
                text_to_check = f"{title} {selftext}"
                
                if any(kw.lower() in text_to_check for kw in AI_KEYWORDS):
                    posts.append({
                        "id": f"reddit-{post_data.get('id', '')}",
                        "title": post_data.get("title", ""),
                        "url": post_data.get("url", ""),
                        "reddit_url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "points": score,
                        "num_comments": post_data.get("num_comments", 0),
                        "author": post_data.get("author", ""),
                        "created_at": datetime.fromtimestamp(created_utc).isoformat(),
                        "source": "reddit",
                        "subreddit": subreddit,
                        "text": selftext[:500] if selftext else "",  # First 500 chars
                    })
        
        # Rate limiting - Reddit allows 60 requests per minute
        await asyncio.sleep(1.0)
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print(f"  ⚠️  Rate limited on r/{subreddit}, waiting...")
            await asyncio.sleep(5.0)
        elif e.response.status_code == 404:
            print(f"  ⚠️  Subreddit r/{subreddit} not found or private")
        else:
            print(f"  ⚠️  Error fetching r/{subreddit}: {e.response.status_code}")
    except Exception as e:
        print(f"  ⚠️  Error fetching r/{subreddit}: {e}")
    
    return posts


async def collect_reddit_posts(
    days_back: int = LOOKBACK_DAYS,
    max_posts_per_subreddit: int = 50
) -> List[dict]:
    """
    Collect AI-related posts from multiple Reddit subreddits.
    
    Args:
        days_back: How many days back to look
        max_posts_per_subreddit: Maximum posts to fetch per subreddit
    
    Returns:
        List of AI-related Reddit posts, sorted by score
    """
    print(f"📡 Samler data fra Reddit (siste {days_back} dager)...")
    print(f"   Søker i {len(AI_SUBREDDITS)} subreddits...")
    
    all_posts = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Fetch from all subreddits in parallel (with rate limiting)
        tasks = []
        for subreddit in AI_SUBREDDITS:
            tasks.append(
                fetch_subreddit_posts(
                    subreddit,
                    days_back=days_back,
                    limit=max_posts_per_subreddit,
                    client=client
                )
            )
        
        # Execute with some delay between batches to respect rate limits
        batch_size = 5
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i+batch_size]
            results = await asyncio.gather(*batch, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    print(f"  ⚠️  Error in batch: {result}")
                    continue
                all_posts.extend(result)
            
            # Rate limiting between batches
            if i + batch_size < len(tasks):
                await asyncio.sleep(2.0)
    
    # Remove duplicates (same post ID)
    seen_ids = set()
    unique_posts = []
    for post in all_posts:
        post_id = post.get("id")
        if post_id and post_id not in seen_ids:
            seen_ids.add(post_id)
            unique_posts.append(post)
    
    # Sort by score
    unique_posts.sort(key=lambda x: x["points"], reverse=True)
    
    print(f"✅ Fant {len(unique_posts)} AI-relaterte Reddit posts")
    
    return unique_posts


# CLI for testing
if __name__ == "__main__":
    async def main():
        print("Samler AI-relaterte posts fra Reddit...")
        posts = await collect_reddit_posts(days_back=30, max_posts_per_subreddit=50)
        print(f"\nFant {len(posts)} AI-relaterte posts")
        
        print("\nTopp 10 etter score:")
        for i, post in enumerate(posts[:10], 1):
            print(f"{i}. [{post['points']} pts] r/{post['subreddit']}: {post['title'][:60]}...")
        
        # Lagre rådata
        with open("reddit_raw_data.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"\nLagret til reddit_raw_data.json")
    
    asyncio.run(main())

