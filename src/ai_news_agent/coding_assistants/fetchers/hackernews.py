"""
Hacker News API Fetcher for Coding Assistants
Uses Algolia API for search
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

HN_ALGOLIA_API = "https://hn.algolia.com/api/v1"


async def search_hn_mentions(
    tool_name: str,
    days_back: int = 30,
    client: httpx.AsyncClient = None
) -> Dict:
    """
    Search Hacker News for mentions of a tool.
    
    Returns:
        {
            "mentions_count": int,
            "comments": List[str],  # Comment text for sentiment analysis
            "stories": List[Dict]   # Story metadata
        }
    """
    if client is None:
        async with httpx.AsyncClient(timeout=30.0) as client:
            return await _search_hn(tool_name, days_back, client)
    else:
        return await _search_hn(tool_name, days_back, client)


async def _search_hn(
    tool_name: str,
    days_back: int,
    client: httpx.AsyncClient
) -> Dict:
    """Internal search function."""
    try:
        # Calculate timestamp for 30 days ago
        cutoff_date = datetime.now() - timedelta(days=days_back)
        timestamp = int(cutoff_date.timestamp())
        
        # Search for tool name in stories
        query = tool_name.lower()
        url = f"{HN_ALGOLIA_API}/search"
        params = {
            "query": query,
            "tags": "story",
            "numericFilters": f"created_at_i>{timestamp}",
            "hitsPerPage": 100
        }
        
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        hits = data.get("hits", [])
        mentions_count = len(hits)
        
        # Extract comment text from story comments
        comments = []
        stories = []
        
        for hit in hits:
            story = {
                "title": hit.get("title", ""),
                "url": hit.get("url", ""),
                "points": hit.get("points", 0),
                "created_at": hit.get("created_at", ""),
                "objectID": hit.get("objectID")
            }
            stories.append(story)
            
            # Get comment text if available
            comment_text = hit.get("comment_text", "")
            if comment_text:
                comments.append(comment_text)
        
        # Also search in comments
        comment_params = {
            "query": query,
            "tags": "comment",
            "numericFilters": f"created_at_i>{timestamp}",
            "hitsPerPage": 100
        }
        
        comment_response = await client.get(url, params=comment_params)
        if comment_response.status_code == 200:
            comment_data = comment_response.json()
            comment_hits = comment_data.get("hits", [])
            mentions_count += len(comment_hits)
            
            for hit in comment_hits:
                comment_text = hit.get("comment_text", "")
                if comment_text:
                    comments.append(comment_text)
        
        # Rate limiting
        await asyncio.sleep(0.5)
        
        return {
            "mentions_count": mentions_count,
            "comments": comments,
            "stories": stories
        }
        
    except httpx.HTTPStatusError as e:
        print(f"  ❌ Error fetching HN data for {tool_name}: {e}")
        return {
            "mentions_count": 0,
            "comments": [],
            "stories": []
        }
    except Exception as e:
        print(f"  ❌ Unexpected error fetching HN data: {e}")
        return {
            "mentions_count": 0,
            "comments": [],
            "stories": []
        }


async def fetch_all_hn_mentions(
    tools: list,
    days_back: int = 30
) -> Dict[str, Dict]:
    """
    Fetch HN mentions for all tools.
    
    Returns:
        {
            "tool_name": {
                "mentions_count": int,
                "comments": List[str],
                "stories": List[Dict]
            }
        }
    """
    results = {}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for tool in tools:
            name = tool["name"]
            print(f"📡 Searching Hacker News for {name}...")
            
            data = await search_hn_mentions(name, days_back, client)
            results[name] = data
            
            print(f"  ✅ Found {data['mentions_count']} mentions")
    
    return results

