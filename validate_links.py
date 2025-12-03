#!/usr/bin/env python3
"""
Validate all links in tool_links.json.
Simple script to check if URLs are accessible.
"""
import json
import sys
from pathlib import Path
import httpx

DATA_DIR = Path("data")
TOOL_LINKS_FILE = DATA_DIR / "tool_links.json"

def validate_url(url: str, timeout: int = 5) -> tuple[bool, str]:
    """Check if URL is accessible. Returns (success, message)."""
    try:
        response = httpx.head(url, follow_redirects=True, timeout=timeout)
        if response.status_code < 400:
            return True, f"✓ OK ({response.status_code})"
        else:
            return False, f"✗ FAILED ({response.status_code})"
    except httpx.TimeoutException:
        return False, "✗ FAILED (timeout)"
    except httpx.RequestError as e:
        return False, f"✗ FAILED ({str(e)})"
    except Exception as e:
        return False, f"✗ FAILED ({str(e)})"

def main():
    """Validate all links in tool_links.json."""
    if not TOOL_LINKS_FILE.exists():
        print(f"Error: {TOOL_LINKS_FILE} not found")
        sys.exit(1)
    
    try:
        with open(TOOL_LINKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: Could not load {TOOL_LINKS_FILE}: {e}")
        sys.exit(1)
    
    tools = data.get("tools", {})
    if not tools:
        print("No tools found in tool_links.json")
        sys.exit(1)
    
    print(f"Validating {len(tools)} tools...\n")
    
    all_passed = True
    failed_tools = []
    
    for tool_name, tool_data in sorted(tools.items()):
        tool_url = tool_data.get("tool_url", "")
        provider_url = tool_data.get("provider_url", "")
        
        print(f"{tool_name}:")
        
        # Validate tool URL
        if tool_url:
            success, message = validate_url(tool_url)
            print(f"  Tool: {tool_url}")
            print(f"    {message}")
            if not success:
                all_passed = False
                failed_tools.append((tool_name, "tool", tool_url))
        else:
            print(f"  Tool: (no URL)")
            print(f"    ⚠ WARNING (missing URL)")
        
        # Validate provider URL
        if provider_url:
            success, message = validate_url(provider_url)
            print(f"  Provider: {provider_url}")
            print(f"    {message}")
            if not success:
                all_passed = False
                failed_tools.append((tool_name, "provider", provider_url))
        else:
            print(f"  Provider: (no URL)")
            print(f"    ⚠ WARNING (missing URL)")
        
        print()
    
    # Summary
    print("=" * 60)
    if all_passed:
        print("✓ All links validated successfully!")
        sys.exit(0)
    else:
        print(f"✗ {len(failed_tools)} link(s) failed:")
        for tool_name, link_type, url in failed_tools:
            print(f"  - {tool_name} ({link_type}): {url}")
        sys.exit(1)

if __name__ == "__main__":
    main()

