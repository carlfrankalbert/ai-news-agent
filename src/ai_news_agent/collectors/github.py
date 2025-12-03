"""
GitHub Trending data collector using GitHub Search API
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import json
import os
from ..config import AI_KEYWORDS, LOOKBACK_DAYS


# GitHub API base URL
GITHUB_API_BASE = "https://api.github.com/search/repositories"

# Minimum stars for a repo to be included
MIN_GITHUB_STARS = 10

# Optional: GitHub token for higher rate limit (60 req/hour without, 5000 with)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)


async def search_github_repos(
    days_back: int = LOOKBACK_DAYS,
    min_stars: int = MIN_GITHUB_STARS,
    max_results: int = 100
) -> list[dict]:
    """
    Søk etter AI-relaterte GitHub repositories som har blitt opprettet eller oppdatert nylig.
    
    Args:
        days_back: Antall dager tilbake å søke
        min_stars: Minimum antall stars for å inkludere repo
        max_results: Maks antall resultater (GitHub API limit er 1000, men vi tar 100 per default)
    
    Returns:
        Liste med AI-relaterte repositories, sortert etter stars
    """
    cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    
    # Bygg søkequery for GitHub API
    # Søker etter repos som er opprettet eller oppdatert nylig, sortert etter stars
    # Vi bruker "pushed" i stedet for "created" for å fange repos som er aktive
    query_parts = [
        f"pushed:>{cutoff_date}",   # Oppdatert i løpet av lookback-perioden (mer fleksibelt)
        f"stars:>={min_stars}",      # Minimum stars
    ]
    # Note: Vi fjerner "topic:ai" fordi det er for restriktivt.
    # Vi filtrerer på AI-relevans i is_ai_relevant() i stedet.
    
    query = " ".join(query_parts)
    
    # Debug: print query for troubleshooting
    print(f"   GitHub query: {query}")
    
    # Headers for GitHub API
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-News-Agent/1.0"
    }
    
    # Legg til token hvis tilgjengelig (for høyere rate limit)
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    ai_repos = []
    page = 1
    per_page = min(100, max_results)  # GitHub API max er 100 per page
    
    print(f"📡 Søker GitHub etter AI-repos (siste {days_back} dager, min {min_stars} stars)...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        while len(ai_repos) < max_results:
            try:
                params = {
                    "q": query,
                    "sort": "stars",      # Sorter etter stars (separat parameter)
                    "order": "desc",      # Høyest først (separat parameter)
                    "per_page": per_page,
                    "page": page
                }
                
                response = await client.get(
                    GITHUB_API_BASE,
                    headers=headers,
                    params=params
                )
                
                # Håndter rate limiting
                if response.status_code == 403:
                    rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", "0")
                    if rate_limit_remaining == "0":
                        reset_time = response.headers.get("X-RateLimit-Reset", "0")
                        print(f"⚠️  GitHub API rate limit nådd. Prøv igjen senere.")
                        break
                
                response.raise_for_status()
                data = response.json()
                
                total_count = data.get("total_count", 0)
                repos = data.get("items", [])
                
                if page == 1:
                    print(f"   GitHub API fant {total_count} totale repos som matcher query")
                
                if not repos:
                    break  # Ingen flere resultater
                
                print(f"   Hentet {len(repos)} repos fra side {page}...")
                
                # Filtrer og normaliser repos
                ai_count_before = len(ai_repos)
                for repo in repos:
                    if is_ai_relevant(repo):
                        normalized = normalize_repo(repo)
                        ai_repos.append(normalized)
                    
                    if len(ai_repos) >= max_results:
                        break
                
                # Debug: vis hvor mange som ble filtrert bort
                if len(repos) > 0:
                    filtered_out = len(repos) - (len(ai_repos) - ai_count_before)
                    if filtered_out > 0:
                        print(f"      Filtrerte bort {filtered_out} repos (ikke AI-relevante)")
                
                # Rate limiting: GitHub tillater 60 req/hour uten token, 5000 med token
                await asyncio.sleep(0.5)  # Vær snill med API
                
                page += 1
                
                # GitHub API har maks 1000 resultater totalt
                if page > 10:  # 10 pages * 100 = 1000 max
                    break
                    
            except httpx.HTTPStatusError as e:
                print(f"⚠️  HTTP feil ved GitHub API: {e.response.status_code}")
                if e.response.status_code == 403:
                    print("   Rate limit nådd eller manglende tilgang")
                break
            except Exception as e:
                print(f"⚠️  Feil ved GitHub API: {e}")
                break
    
    # Sorter etter stars (points)
    ai_repos.sort(key=lambda x: x["points"], reverse=True)
    
    print(f"✅ Fant {len(ai_repos)} AI-relaterte GitHub repos")
    
    return ai_repos


def normalize_repo(raw: dict) -> dict:
    """
    Normaliser GitHub repo til vårt format (samme som HN-posts).
    """
    repo_id = raw.get("id", "")
    created_at = raw.get("created_at", "")
    updated_at = raw.get("updated_at", "")
    
    # Bruk created_at hvis tilgjengelig, ellers updated_at
    date_str = created_at or updated_at or ""
    
    # Parse ISO format til vårt format
    if date_str:
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            date_str = dt.isoformat()
        except:
            date_str = ""
    
    # Bygg full URL
    html_url = raw.get("html_url", "")
    owner = raw.get("owner", {})
    owner_login = owner.get("login", "")
    repo_name = raw.get("name", "")
    
    if not html_url and owner_login and repo_name:
        html_url = f"https://github.com/{owner_login}/{repo_name}"
    
    return {
        "id": f"github-{repo_id}",
        "title": raw.get("name", ""),
        "url": html_url,
        "github_url": html_url,  # Samme som url, men eksplisitt
        "points": raw.get("stargazers_count", 0),  # Stars = "points" i vårt system
        "num_comments": 0,  # GitHub har ikke "comments" som HN
        "author": owner_login,
        "created_at": date_str,
        "source": "github",
        "description": raw.get("description", ""),
        "language": raw.get("language", ""),
        "topics": raw.get("topics", []),  # GitHub topics/tags
    }


def is_ai_relevant(repo: dict) -> bool:
    """
    Sjekk om en repo er AI-relevant basert på keywords.
    Sjekker navn, beskrivelse, topics og language.
    """
    name = (repo.get("name") or "").lower()
    description = (repo.get("description") or "").lower()
    language = (repo.get("language") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    
    # Kombiner all tekst for søk
    text_to_check = f"{name} {description} {language} {' '.join(topics)}"
    
    # Sjekk mot AI keywords
    return any(kw.lower() in text_to_check for kw in AI_KEYWORDS)


async def collect_github_trending(
    days_back: int = LOOKBACK_DAYS,
    max_results: int = 100
) -> list[dict]:
    """
    Hovedfunksjon for å samle GitHub trending repos.
    Samme interface som collect_ai_mentions() for konsistens.
    
    Args:
        days_back: Antall dager tilbake å søke
        max_results: Maks antall resultater
    
    Returns:
        Liste med AI-relaterte repos, sortert etter stars
    """
    return await search_github_repos(
        days_back=days_back,
        min_stars=MIN_GITHUB_STARS,
        max_results=max_results
    )


# CLI for testing
if __name__ == "__main__":
    async def main():
        print("Samler AI-relaterte GitHub repos...")
        repos = await collect_github_trending(days_back=30, max_results=50)
        print(f"\nFant {len(repos)} AI-relaterte repos")
        
        print("\nTopp 10 etter stars:")
        for i, repo in enumerate(repos[:10], 1):
            stars = repo['points']
            name = repo['title']
            desc = repo.get('description', '')[:50]
            print(f"{i}. [{stars} ⭐] {name}")
            if desc:
                print(f"   {desc}...")
        
        # Lagre rådata
        with open("github_raw_data.json", "w", encoding="utf-8") as f:
            json.dump(repos, f, indent=2, ensure_ascii=False)
        print(f"\nLagret til github_raw_data.json")
    
    asyncio.run(main())

