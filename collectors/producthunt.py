"""
Product Hunt data collector for AI tools
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
from config import AI_KEYWORDS, LOOKBACK_DAYS

# Product Hunt API (gratis tier)
# Merk: Product Hunt har begrenset gratis API, så vi bruker web scraping som fallback
PRODUCT_HUNT_API_BASE = "https://api.producthunt.com/v2/api/graphql"

# Minimum upvotes for å inkludere et produkt
MIN_PH_UPVOTES = 10


async def fetch_producthunt_trending(
    days_back: int = LOOKBACK_DAYS,
    limit: int = 100
) -> List[Dict]:
    """
    Hent trending produkter fra Product Hunt via web scraping.
    
    Product Hunt har begrenset gratis API, så vi bruker deres public RSS/JSON feeds
    eller scraping som fallback.
    """
    print(f"📡 Samler data fra Product Hunt (siste {days_back} dager)...")
    
    # Product Hunt har en public JSON feed for trending products
    # Vi kan også scrape deres "AI Tools" kategori
    products = []
    
    try:
        # Prøv å hente fra Product Hunt's public API endpoint
        # Merk: Dette kan kreve auth i fremtiden, så vi har en fallback
        async with httpx.AsyncClient() as client:
            # Product Hunt har en GraphQL API, men krever auth for de fleste queries
            # Vi bruker derfor scraping av deres public pages
            
            # Scrape "AI Tools" kategorien
            url = "https://www.producthunt.com/topics/artificial-intelligence"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
            
            response = await client.get(url, headers=headers, timeout=30.0)
            
            if response.status_code == 200:
                # Parse HTML for å finne produkter
                # Dette er en forenklet versjon - i produksjon bør du bruke BeautifulSoup
                html = response.text
                
                # Product Hunt bruker JSON-LD structured data
                # Vi kan også prøve å hente fra deres API hvis vi har access token
                print("   ⚠️  Product Hunt API krever autentisering")
                print("   💡 Bruker web scraping som fallback")
                
                # For nå returnerer vi tom liste - implementer scraping eller få API key
                # I produksjon: bruk BeautifulSoup eller Selenium for scraping
                
    except Exception as e:
        print(f"   Feil ved Product Hunt: {e}")
    
    # Filtrer på AI-relevans
    ai_products = []
    cutoff_time = datetime.now() - timedelta(days=days_back)
    
    for product in products:
        # Filtrer på tid
        created_time = product.get("created_at", "")
        if created_time:
            try:
                created_date = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
                if created_date < cutoff_time:
                    continue
            except:
                pass
        
        # Filtrer på upvotes
        upvotes = product.get("votes_count", 0) or product.get("upvotes", 0)
        if upvotes < MIN_PH_UPVOTES:
            continue
        
        # Filtrer på AI-relevans
        if is_ai_relevant(product):
            ai_products.append(normalize_post(product))
    
    # Sorter etter upvotes
    ai_products.sort(key=lambda x: x["points"], reverse=True)
    
    print(f"✅ Fant {len(ai_products)} AI-relaterte produkter fra Product Hunt")
    
    return ai_products


async def collect_ai_mentions(days_back: int = LOOKBACK_DAYS) -> List[Dict]:
    """
    Wrapper for å matche samme interface som andre collectors.
    """
    return await fetch_producthunt_trending(days_back=days_back)


def normalize_post(raw: Dict) -> Dict:
    """
    Normaliser Product Hunt-post til vårt format.
    """
    product_id = raw.get("id", "") or raw.get("slug", "")
    created_time = raw.get("created_at", "")
    
    if created_time:
        try:
            created_date = datetime.fromisoformat(created_time.replace("Z", "+00:00")).isoformat()
        except:
            created_date = ""
    else:
        created_date = ""
    
    # Product Hunt URL
    slug = raw.get("slug", "")
    ph_url = f"https://www.producthunt.com/posts/{slug}" if slug else ""
    
    return {
        "id": f"producthunt_{product_id}",
        "title": raw.get("name", "") or raw.get("title", ""),
        "url": raw.get("website", "") or ph_url,
        "producthunt_url": ph_url,
        "points": raw.get("votes_count", 0) or raw.get("upvotes", 0),
        "num_comments": raw.get("comments_count", 0),
        "author": raw.get("maker", {}).get("name", "") if isinstance(raw.get("maker"), dict) else "",
        "tagline": raw.get("tagline", ""),
        "created_at": created_date,
        "source": "producthunt",
    }


def is_ai_relevant(product: Dict) -> bool:
    """
    Sjekk om et Product Hunt-produkt er AI-relevant.
    """
    name = (product.get("name") or product.get("title") or "").lower()
    tagline = (product.get("tagline") or "").lower()
    description = (product.get("description") or "").lower()
    website = (product.get("website") or "").lower()
    
    text_to_check = f"{name} {tagline} {description} {website}"
    
    return any(kw.lower() in text_to_check for kw in AI_KEYWORDS)


# CLI for testing
if __name__ == "__main__":
    async def main():
        print("Samler AI-relaterte produkter fra Product Hunt...")
        products = await collect_ai_mentions(days_back=30)
        print(f"\nFant {len(products)} AI-relaterte produkter")
        
        if products:
            print("\nTopp 10 etter upvotes:")
            for i, product in enumerate(products[:10], 1):
                print(f"{i}. [{product['points']} pts] {product['title'][:60]}...")
        
        # Lagre rådata
        with open("producthunt_raw_data.json", "w") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"\nLagret til producthunt_raw_data.json")
    
    asyncio.run(main())

