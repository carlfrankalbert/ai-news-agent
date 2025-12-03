#!/usr/bin/env python3
"""
Link checker agent - Validates provider logos and website URLs.
Runs daily to ensure all links in PROVIDER_INFO are still valid.
"""
import asyncio
import httpx
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import sys

# Import PROVIDER_INFO from generator module
# Since check_links.py adds src/ to path, we can import directly
try:
    from ai_news_agent.generator.generate_html import PROVIDER_INFO
except ImportError:
    # Fallback: add src to path if not already there
    src_path = Path(__file__).parent.parent.parent.parent / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path.parent))
    from ai_news_agent.generator.generate_html import PROVIDER_INFO

OUTPUT_DIR = Path("output")
REPORT_FILE = OUTPUT_DIR / "link_check_report.json"

# Timeout for HTTP requests (seconds)
REQUEST_TIMEOUT = 10.0

# User agent to avoid being blocked
USER_AGENT = "Mozilla/5.0 (compatible; FYRK-AI-Radar-LinkChecker/1.0)"


async def check_url(client: httpx.AsyncClient, url: str, url_type: str) -> Tuple[bool, int, str]:
    """
    Check if a URL is accessible.
    Returns: (is_valid, status_code, error_message)
    """
    try:
        response = await client.get(
            url,
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT}
        )
        
        # Consider 2xx and 3xx as valid
        is_valid = 200 <= response.status_code < 400
        
        if is_valid:
            return (True, response.status_code, "")
        else:
            return (False, response.status_code, f"HTTP {response.status_code}")
            
    except httpx.TimeoutException:
        return (False, 0, "Timeout")
    except httpx.ConnectError:
        return (False, 0, "Connection error")
    except httpx.HTTPStatusError as e:
        return (False, e.response.status_code, f"HTTP {e.response.status_code}")
    except Exception as e:
        return (False, 0, str(e))


async def check_provider_links(provider: str, info: Dict[str, str]) -> Dict:
    """Check both logo and website URLs for a provider."""
    results = {
        "provider": provider,
        "logo": {"url": info.get("logo", ""), "valid": False, "status": 0, "error": ""},
        "website": {"url": info.get("website", ""), "valid": False, "status": 0, "error": ""}
    }
    
    async with httpx.AsyncClient() as client:
        # Check logo
        if info.get("logo"):
            logo_valid, logo_status, logo_error = await check_url(client, info["logo"], "logo")
            results["logo"] = {
                "url": info["logo"],
                "valid": logo_valid,
                "status": logo_status,
                "error": logo_error
            }
        
        # Check website
        if info.get("website"):
            website_valid, website_status, website_error = await check_url(client, info["website"], "website")
            results["website"] = {
                "url": info["website"],
                "valid": website_valid,
                "status": website_status,
                "error": website_error
            }
    
    return results


async def check_all_links() -> Dict:
    """Check all provider links and return a report."""
    print("🔍 Starting link validation check...")
    print(f"📋 Checking {len(PROVIDER_INFO)} providers...")
    
    results = []
    all_valid = True
    
    # Check all providers concurrently (with some rate limiting)
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests
    
    async def check_with_semaphore(provider: str, info: Dict[str, str]):
        async with semaphore:
            return await check_provider_links(provider, info)
    
    tasks = [
        check_with_semaphore(provider, info)
        for provider, info in PROVIDER_INFO.items()
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Analyze results
    total_links = 0
    valid_links = 0
    invalid_links = []
    
    for result in results:
        for link_type in ["logo", "website"]:
            link_data = result[link_type]
            if link_data["url"]:
                total_links += 1
                if link_data["valid"]:
                    valid_links += 1
                else:
                    invalid_links.append({
                        "provider": result["provider"],
                        "type": link_type,
                        "url": link_data["url"],
                        "status": link_data["status"],
                        "error": link_data["error"]
                    })
                    all_valid = False
    
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "total_providers": len(PROVIDER_INFO),
            "total_links": total_links,
            "valid_links": valid_links,
            "invalid_links": len(invalid_links),
            "all_valid": all_valid
        },
        "invalid_links": invalid_links,
        "detailed_results": results
    }
    
    return report


def print_report(report: Dict):
    """Print a human-readable report."""
    summary = report["summary"]
    
    print("\n" + "="*60)
    print("📊 LINK CHECK REPORT")
    print("="*60)
    print(f"⏰ Timestamp: {report['timestamp']}")
    print(f"📦 Total providers: {summary['total_providers']}")
    print(f"🔗 Total links checked: {summary['total_links']}")
    print(f"✅ Valid links: {summary['valid_links']}")
    print(f"❌ Invalid links: {summary['invalid_links']}")
    print("="*60)
    
    if report["invalid_links"]:
        print("\n⚠️  INVALID LINKS FOUND:")
        print("-"*60)
        for link in report["invalid_links"]:
            print(f"❌ {link['provider']} - {link['type'].upper()}")
            print(f"   URL: {link['url']}")
            print(f"   Status: {link['status']} | Error: {link['error']}")
            print()
    else:
        print("\n✅ All links are valid!")
    
    print("="*60 + "\n")


def save_report(report: Dict):
    """Save report to JSON file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Report saved to: {REPORT_FILE}")


async def main():
    """Main entry point."""
    try:
        report = await check_all_links()
        print_report(report)
        save_report(report)
        
        # Exit with error code if any links are invalid
        if not report["summary"]["all_valid"]:
            print("⚠️  Some links are invalid. Please review the report.")
            sys.exit(1)
        else:
            print("✅ All links validated successfully!")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Error during link checking: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

