"""
X/Twitter data collector using Twitter API v2
Note: Requires Twitter API credentials (Bearer Token)
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List
import json
import os
from ..config import AI_KEYWORDS, LOOKBACK_DAYS

# Twitter API v2 base URL
TWITTER_API_BASE = "https://api.twitter.com/2"

# Twitter API credentials (from environment variables)
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", None)

# Minimum engagement (likes + retweets) for a tweet to be included
MIN_TWITTER_ENGAGEMENT = 10


async def search_tweets(
    query: str,
    days_back: int = LOOKBACK_DAYS,
    max_results: int = 100,
    client: httpx.AsyncClient = None
) -> List[dict]:
    """
    Search for tweets using Twitter API v2.
    
    Args:
        query: Search query
        days_back: How many days back to search
        max_results: Maximum number of results (API limit is 100 per request)
        client: Optional httpx client (for reuse)
    
    Returns:
        List of tweets matching the query
    """
    if not TWITTER_BEARER_TOKEN:
        print("  ⚠️  TWITTER_BEARER_TOKEN not set, skipping Twitter collection")
        return []
    
    cutoff_time = datetime.now() - timedelta(days=days_back)
    cutoff_date = cutoff_time.strftime("%Y-%m-%d")
    
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
        "User-Agent": "AI-News-Agent/1.0"
    }
    
    tweets = []
    next_token = None
    
    try:
        # Build query with date filter
        # Twitter API v2 query syntax
        full_query = f"{query} -is:retweet lang:en"
        
        params = {
            "query": full_query,
            "max_results": min(max_results, 100),  # API limit
            "tweet.fields": "created_at,public_metrics,author_id,text",
            "expansions": "author_id",
            "user.fields": "username",
            "start_time": f"{cutoff_date}T00:00:00Z",
        }
        
        while len(tweets) < max_results:
            if next_token:
                params["next_token"] = next_token
            
            response = await client.get(
                f"{TWITTER_API_BASE}/tweets/search/recent",
                headers=headers,
                params=params,
                timeout=30.0
            )
            
            if response.status_code == 401:
                print("  ⚠️  Twitter API authentication failed. Check your bearer token.")
                break
            elif response.status_code == 429:
                print("  ⚠️  Twitter API rate limit reached. Waiting...")
                await asyncio.sleep(60.0)  # Wait 1 minute
                continue
            elif response.status_code != 200:
                print(f"  ⚠️  Twitter API error: {response.status_code}")
                break
            
            data = response.json()
            
            # Extract tweets
            tweet_data = data.get("data", [])
            users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
            
            for tweet in tweet_data:
                metrics = tweet.get("public_metrics", {})
                engagement = (
                    metrics.get("like_count", 0) +
                    metrics.get("retweet_count", 0) +
                    metrics.get("reply_count", 0)
                )
                
                # Filter by engagement
                if engagement < MIN_TWITTER_ENGAGEMENT:
                    continue
                
                author_id = tweet.get("author_id")
                author = users.get(author_id, {})
                username = author.get("username", "unknown")
                
                tweets.append({
                    "id": f"twitter-{tweet.get('id', '')}",
                    "title": tweet.get("text", "")[:200],  # First 200 chars as "title"
                    "url": f"https://twitter.com/{username}/status/{tweet.get('id', '')}",
                    "twitter_url": f"https://twitter.com/{username}/status/{tweet.get('id', '')}",
                    "points": engagement,  # Use engagement as "points"
                    "num_comments": metrics.get("reply_count", 0),
                    "author": username,
                    "created_at": tweet.get("created_at", ""),
                    "source": "twitter",
                    "text": tweet.get("text", ""),
                    "likes": metrics.get("like_count", 0),
                    "retweets": metrics.get("retweet_count", 0),
                })
            
            # Check for next page
            next_token = data.get("meta", {}).get("next_token")
            if not next_token:
                break
            
            # Rate limiting - Twitter API v2 allows 300 requests per 15 minutes
            await asyncio.sleep(3.0)
    
    except httpx.HTTPStatusError as e:
        print(f"  ⚠️  Twitter API HTTP error: {e.response.status_code}")
    except Exception as e:
        print(f"  ⚠️  Twitter API error: {e}")
    
    return tweets


async def collect_twitter_posts(
    days_back: int = LOOKBACK_DAYS,
    max_results: int = 200
) -> List[dict]:
    """
    Collect AI-related tweets from Twitter/X.
    
    Uses multiple search queries to find AI-related content.
    
    Args:
        days_back: How many days back to search
        max_results: Maximum number of tweets to collect
    
    Returns:
        List of AI-related tweets, sorted by engagement
    """
    if not TWITTER_BEARER_TOKEN:
        print("⚠️  TWITTER_BEARER_TOKEN not set, skipping Twitter collection")
        return []
    
    print(f"📡 Samler data fra X/Twitter (siste {days_back} dager)...")
    
    # Build search queries from AI keywords
    # Twitter API works best with OR queries
    queries = [
        # General AI queries
        "(" + " OR ".join(AI_KEYWORDS[:10]) + ")",
        # Specific tool queries
        "(AI tool OR AI model OR LLM OR GPT OR Claude OR Gemini)",
        # Trending AI topics
        "(artificial intelligence OR machine learning OR deep learning)",
    ]
    
    all_tweets = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for query in queries:
            print(f"   Søker: {query[:50]}...")
            tweets = await search_tweets(
                query,
                days_back=days_back,
                max_results=max_results // len(queries),
                client=client
            )
            all_tweets.extend(tweets)
            
            if len(all_tweets) >= max_results:
                break
    
    # Remove duplicates
    seen_ids = set()
    unique_tweets = []
    for tweet in all_tweets:
        tweet_id = tweet.get("id")
        if tweet_id and tweet_id not in seen_ids:
            seen_ids.add(tweet_id)
            unique_tweets.append(tweet)
    
    # Sort by engagement (points)
    unique_tweets.sort(key=lambda x: x["points"], reverse=True)
    
    print(f"✅ Fant {len(unique_tweets)} AI-relaterte tweets")
    
    return unique_tweets


# CLI for testing
if __name__ == "__main__":
    async def main():
        print("Samler AI-relaterte tweets fra X/Twitter...")
        tweets = await collect_twitter_posts(days_back=7, max_results=100)
        print(f"\nFant {len(tweets)} AI-relaterte tweets")
        
        print("\nTopp 10 etter engagement:")
        for i, tweet in enumerate(tweets[:10], 1):
            print(f"{i}. [{tweet['points']} pts] @{tweet['author']}: {tweet['title'][:60]}...")
        
        # Lagre rådata
        with open("twitter_raw_data.json", "w", encoding="utf-8") as f:
            json.dump(tweets, f, indent=2, ensure_ascii=False)
        print(f"\nLagret til twitter_raw_data.json")
    
    asyncio.run(main())

