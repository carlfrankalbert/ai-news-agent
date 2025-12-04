"""
GitHub API Fetcher for Coding Assistants
"""
import httpx
import os
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from pathlib import Path
import json

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def fetch_github_stats(
    owner: str,
    repo: str,
    client: httpx.AsyncClient,
    cache_dir: Optional[Path] = None
) -> Dict:
    """
    Fetch GitHub repository statistics.
    
    Returns:
        {
            "stars": int,
            "forks": int,
            "open_issues": int,
            "closed_issues": int,
            "last_commit_date": str,
            "stars_30d_ago": Optional[int]  # If previous snapshot exists
        }
    """
    if not owner or not repo:
        return {
            "stars": 0,
            "forks": 0,
            "open_issues": 0,
            "closed_issues": 0,
            "last_commit_date": None,
            "stars_30d_ago": None
        }
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-News-Agent/1.0"
    }
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        # Fetch repo info
        repo_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
        response = await client.get(repo_url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        
        # Get issue counts from repo data (approximate)
        # Note: GitHub API doesn't provide exact counts easily, so we use the repo's open_issues_count
        # and estimate closed issues
        open_issues_count = repo_data.get("open_issues_count", 0)
        
        # For closed issues, we can't get exact count without pagination
        # Use a simple heuristic: if repo has many open issues, likely has many closed too
        # This is an approximation - for better accuracy, would need to paginate
        closed_issues_count = open_issues_count * 2  # Rough estimate
        
        # Get last commit date
        commits_url = f"{repo_url}/commits?per_page=1"
        commits_response = await client.get(commits_url, headers=headers)
        last_commit_date = None
        if commits_response.status_code == 200:
            commits = commits_response.json()
            if commits and isinstance(commits, list) and len(commits) > 0:
                last_commit_date = commits[0].get("commit", {}).get("author", {}).get("date")
        
        # Try to get previous snapshot for stars growth
        stars_30d_ago = None
        if cache_dir:
            snapshot_file = cache_dir / f"{owner}_{repo}_snapshot.json"
            if snapshot_file.exists():
                try:
                    with open(snapshot_file, "r") as f:
                        snapshot = json.load(f)
                        if "stars" in snapshot and "date" in snapshot:
                            snapshot_date = datetime.fromisoformat(snapshot["date"].replace("Z", "+00:00"))
                            days_ago = (datetime.now(snapshot_date.tzinfo) - snapshot_date).days
                            if 25 <= days_ago <= 35:  # Approximately 30 days
                                stars_30d_ago = snapshot["stars"]
                except Exception:
                    pass
        
        result = {
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "open_issues": open_issues_count,
            "closed_issues": closed_issues_count,
            "last_commit_date": last_commit_date,
            "stars_30d_ago": stars_30d_ago
        }
        
        # Save current snapshot
        if cache_dir:
            snapshot_file = cache_dir / f"{owner}_{repo}_snapshot.json"
            snapshot_data = {
                "stars": result["stars"],
                "date": datetime.utcnow().isoformat() + "Z"
            }
            with open(snapshot_file, "w") as f:
                json.dump(snapshot_data, f)
        
        # Rate limit: 30 requests per minute for unauthenticated, 5000 for authenticated
        await asyncio.sleep(0.5 if GITHUB_TOKEN else 2.0)
        
        return result
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"  ⚠️  Repository {owner}/{repo} not found")
            return {
                "stars": 0,
                "forks": 0,
                "open_issues": 0,
                "closed_issues": 0,
                "last_commit_date": None,
                "stars_30d_ago": None
            }
        print(f"  ❌ Error fetching GitHub stats for {owner}/{repo}: {e}")
        return {
            "stars": 0,
            "forks": 0,
            "open_issues": 0,
            "closed_issues": 0,
            "last_commit_date": None,
            "stars_30d_ago": None
        }
    except Exception as e:
        print(f"  ❌ Unexpected error fetching GitHub stats: {e}")
        return {
            "stars": 0,
            "forks": 0,
            "open_issues": 0,
            "closed_issues": 0,
            "last_commit_date": None,
            "stars_30d_ago": None
        }


async def fetch_all_github_stats(
    tools: list,
    cache_dir: Optional[Path] = None
) -> Dict[str, Dict]:
    """
    Fetch GitHub stats for all tools.
    
    Returns:
        {
            "tool_name": {
                "stars": int,
                "forks": int,
                ...
            }
        }
    """
    results = {}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for tool in tools:
            name = tool["name"]
            owner = tool.get("github_owner")
            repo = tool.get("github_repo")
            
            print(f"📡 Fetching GitHub stats for {name}...")
            stats = await fetch_github_stats(owner, repo, client, cache_dir)
            results[name] = stats
            
            if stats["stars"] > 0:
                print(f"  ✅ {stats['stars']} stars, {stats['forks']} forks")
            else:
                print(f"  ⚠️  No GitHub data available")
    
    return results

