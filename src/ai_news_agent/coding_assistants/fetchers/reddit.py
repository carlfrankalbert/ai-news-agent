"""
Reddit API Fetcher for Coding Assistants
Uses public JSON endpoint (no auth required)
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List
import time

REDDIT_API_BASE = "https://www.reddit.com"
REDDIT_SUBREDDITS = ["programming", "vscode", "neovim", "coding"]


async def search_reddit_mentions(
    tool_name: str,
    subreddits: List[str] = None,
    days_back: int = 30,
    client: httpx.AsyncClient = None
) -> Dict:
    """
    Search Reddit for mentions of a tool.
    
    Returns:
        {
            "mentions_count": int,
            "comments": List[str],  # Comment text for sentiment analysis
            "posts": List[Dict]     # Post metadata
        }
    """
    if subreddits is None:
        subreddits = REDDIT_SUBREDDITS
    
    if client is None:
        async with httpx.AsyncClient(timeout=30.0) as client:
            return await _search_reddit(tool_name, subreddits, days_back, client)
    else:
        return await _search_reddit(tool_name, subreddits, days_back, client)


async def _search_reddit(
    tool_name: str,
    subreddits: List[str],
    days_back: int,
    client: httpx.AsyncClient
) -> Dict:
    """Internal search function."""
    all_comments = []
    all_posts = []
    total_mentions = 0
    
    headers = {
        "User-Agent": "AI-News-Agent/1.0 (by /u/ai-news-agent)"
    }
    
    try:
        # Search in each subreddit
        for subreddit in subreddits:
            try:
                # Search posts
                url = f"{REDDIT_API_BASE}/r/{subreddit}/search.json"
                params = {
                    "q": tool_name,
                    "t": "month",  # Last month
                    "limit": 100,
                    "restrict_sr": "true"
                }
                
                response = await client.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    children = data.get("data", {}).get("children", [])
                    
                    for child in children:
                        post_data = child.get("data", {})
                        post = {
                            "title": post_data.get("title", ""),
                            "subreddit": subreddit,
                            "score": post_data.get("score", 0),
                            "num_comments": post_data.get("num_comments", 0),
                            "created_utc": post_data.get("created_utc"),
                            "url": post_data.get("url", "")
                        }
                        all_posts.append(post)
                        
                        # Get selftext if available
                        selftext = post_data.get("selftext", "")
                        if selftext:
                            all_comments.append(selftext)
                    
                    total_mentions += len(children)
                
                # Rate limiting - Reddit allows 60 requests per minute
                await asyncio.sleep(1.0)
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    print(f"  ⚠️  Rate limited on r/{subreddit}, waiting...")
                    await asyncio.sleep(5.0)
                else:
                    print(f"  ⚠️  Error searching r/{subreddit}: {e}")
                continue
            except Exception as e:
                print(f"  ⚠️  Error searching r/{subreddit}: {e}")
                continue
        
        return {
            "mentions_count": total_mentions,
            "comments": all_comments,
            "posts": all_posts
        }
        
    except Exception as e:
        print(f"  ❌ Unexpected error fetching Reddit data: {e}")
        return {
            "mentions_count": 0,
            "comments": [],
            "posts": []
        }


async def fetch_all_reddit_mentions(
    tools: list,
    subreddits: List[str] = None,
    days_back: int = 30
) -> Dict[str, Dict]:
    """
    Fetch Reddit mentions for all tools.
    
    Returns:
        {
            "tool_name": {
                "mentions_count": int,
                "comments": List[str],
                "posts": List[Dict]
            }
        }
    """
    results = {}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for tool in tools:
            name = tool["name"]
            print(f"📡 Searching Reddit for {name}...")
            
            data = await search_reddit_mentions(name, subreddits, days_back, client)
            results[name] = data
            
            print(f"  ✅ Found {data['mentions_count']} mentions")
    
    return results

