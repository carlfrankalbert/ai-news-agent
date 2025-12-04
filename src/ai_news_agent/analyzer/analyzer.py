"""
AI Tool Analyzer - bruker Claude til å analysere og rangere AI-verktøy
"""
import json
import re
from datetime import datetime
from anthropic import Anthropic
from ..config import CATEGORIES


def create_analysis_prompt(posts: list[dict], period: str) -> str:
    """
    Lag prompt for Claude-analyse.
    """
    posts_summary = "\n".join([
        f"- [{p['points']} pts, {p['num_comments']} comments] {p['title']}"
        for p in posts[:200]  # Begrens for context window
    ])
    
    categories_desc = "\n".join([
        f"- {c['slug']}: {c['name']} (eks: {', '.join(c['examples'])})"
        for c in CATEGORIES
    ])
    
    # Tell hvor mange fra hver kilde
    hn_count = sum(1 for p in posts if p.get("source") == "hackernews")
    github_count = sum(1 for p in posts if p.get("source") == "github")
    
    return f"""Analyser disse AI-verktøy-mentions fra Hacker News diskusjoner og GitHub trending repositories fra de siste 90 dagene og lag en rangering.

Data collected from:
- Hacker News: {hn_count} posts
- GitHub Trending: {github_count} repositories

## Posts (sortert etter points):
{posts_summary}

## Kategorier å rangere:
{categories_desc}

## Oppgave:
1. Identifiser hvilke AI-verktøy/modeller som nevnes mest og har mest momentum
2. For hver kategori, ranger topp 10 verktøy basert på:
   - Hvor mye de diskuteres (buzz/momentum)
   - Generell sentiment (positivt/negativt)
   - Nytte for kunnskapsarbeidere
   - Pris/ytelse-forhold (hvis relevant)
   
   Rang 1-3 får medaljer (gold, silver, bronze), rang 4-10 får ingen medalje.

3. Identifiser 2-3 "new & noteworthy" verktøy som er nye/spennende men ikke topp 10 ennå

## Output JSON-format (følg eksakt):
{{
  "period": "{period}",
  "generated_at": "{datetime.now().isoformat()}",
  "data_source": "hackernews,github",
  "total_posts_analyzed": {len(posts)},
  "categories": [
    {{
      "name": "Kategori-navn",
      "slug": "kategori-slug",
      "top3": [
        {{
          "rank": 1,
          "medal": "gold",
          "name": "VERKTØY_NAVN",
          "provider": "LEVERANDØR",
          "short_reason": "1 setning: hvorfor #1 akkurat nå",
          "tags": ["relevant", "tags"],
          "scores": {{
            "buzz_momentum": 5,
            "sentiment": 4,
            "utility_for_knowledge_work": 5,
            "price_performance": 4
          }},
          "evidence": ["Tittel på relevant HN-post 1", "Tittel 2"]
        }},
        {{ "rank": 2, "medal": "silver", ... }},
        {{ "rank": 3, "medal": "bronze", ... }},
        {{ "rank": 4, "medal": null, ... }},
        {{ "rank": 5, "medal": null, ... }},
        {{ "rank": 6, "medal": null, ... }},
        {{ "rank": 7, "medal": null, ... }},
        {{ "rank": 8, "medal": null, ... }},
        {{ "rank": 9, "medal": null, ... }},
        {{ "rank": 10, "medal": null, ... }}
      ]
    }}
  ],
  "new_and_noteworthy": [
    {{
      "name": "NYTT_VERKTØY",
      "provider": "LEVERANDØR",
      "category_hint": "relevant-slug",
      "short_reason": "Hvorfor dette er spennende nå",
      "tags": ["beta", "experimental"]
    }}
  ],
  "summary": "2-3 setninger om hovedtrender denne perioden"
}}

Svar KUN med valid JSON, ingen annen tekst."""


def analyze_with_claude(posts: list[dict], period: str) -> dict:
    """
    Send posts til Claude for analyse og rangering.
    """
    client = Anthropic()
    
    prompt = create_analysis_prompt(posts, period)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16384,  # Increased to prevent truncation of large JSON responses
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    # Check if response was truncated
    if message.stop_reason == "max_tokens":
        print("⚠️  Claude response ble trunkert (nådde max_tokens). Prøver å parse uansett...")
    
    # Parse JSON fra response
    try:
        # Håndter eventuell markdown code block
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        rankings = json.loads(response_text.strip())
        return rankings
    
    except json.JSONDecodeError as e:
        print(f"⚠️  Feil ved parsing av JSON: {e}")
        print(f"Prøver å ekstraktere gyldig JSON fra respons...")
        
        # Strategy 1: Extract from markdown code blocks more carefully
        import re
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',  # JSON in ```json blocks
            r'```\s*(\{.*?\})\s*```',      # JSON in ``` blocks
            r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})',  # Any complete JSON object
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response_text, re.DOTALL)
            if matches:
                # Try the longest match (most complete)
                for match in sorted(matches, key=len, reverse=True):
                    try:
                        rankings = json.loads(match.strip())
                        print(f"✅ Ekstraherte gyldig JSON fra markdown block")
                        return rankings
                    except:
                        continue
        
        # Strategy 2: Find the first complete JSON object by counting braces
        try:
            start_idx = response_text.find('{')
            if start_idx >= 0:
                brace_count = 0
                in_string = False
                escape_next = False
                
                for i in range(start_idx, len(response_text)):
                    char = response_text[i]
                    
                    if escape_next:
                        escape_next = False
                        continue
                    
                    if char == '\\':
                        escape_next = True
                        continue
                    
                    if char == '"' and not escape_next:
                        in_string = not in_string
                        continue
                    
                    if not in_string:
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                # Found complete object
                                json_str = response_text[start_idx:i+1]
                                rankings = json.loads(json_str)
                                print(f"✅ Ekstraherte gyldig JSON ved å telle braces")
                                return rankings
        except Exception as extract_error:
            print(f"   Strategy 2 feilet: {extract_error}")
        
        # Strategy 3: Try to fix common JSON issues
        try:
            # Remove trailing commas before } or ]
            fixed_json = re.sub(r',(\s*[}\]])', r'\1', response_text)
            # Try parsing again
            rankings = json.loads(fixed_json.strip())
            print(f"✅ Ekstraherte gyldig JSON etter å ha fikset komma-feil")
            return rankings
        except:
            pass
        
        print(f"❌ Kunne ikke ekstraktere gyldig JSON")
        print(f"Raw response (første 1000 tegn):\n{response_text[:1000]}...")
        
        # Return error structure that can be handled downstream
        return {
            "error": str(e),
            "raw_response": response_text,
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "data_source": "hackernews,github",
            "total_posts_analyzed": len(posts),
            "categories": []  # Empty categories so validation doesn't fail completely
        }


def validate_rankings(rankings: dict) -> tuple[bool, list[str]]:
    """
    Valider at rankings-strukturen er korrekt.
    Returnerer (is_valid, list_of_issues)
    """
    issues = []
    
    if "categories" not in rankings:
        issues.append("Mangler 'categories' felt")
        return False, issues
    
    for cat in rankings.get("categories", []):
        if "top3" not in cat:
            issues.append(f"Kategori '{cat.get('name', 'ukjent')}' mangler 'top3'")
        elif len(cat["top3"]) < 3:
            issues.append(f"Kategori '{cat.get('name')}' har færre enn 3 rangeringer")
        
        for item in cat.get("top3", []):
            if not item.get("name"):
                issues.append(f"Rangering i '{cat.get('name')}' mangler 'name'")
            if not item.get("short_reason"):
                issues.append(f"'{item.get('name', '?')}' mangler 'short_reason'")
    
    return len(issues) == 0, issues


# CLI for testing
if __name__ == "__main__":
    # Test med dummy data
    test_posts = [
        {"title": "Claude 3.5 Sonnet is now available", "points": 500, "num_comments": 200},
        {"title": "GPT-4o released with vision capabilities", "points": 450, "num_comments": 180},
        {"title": "Llama 3 70B beats GPT-4 on benchmarks", "points": 400, "num_comments": 150},
    ]
    
    print("Testing analyse med dummy-data...")
    result = analyze_with_claude(test_posts, "2025-03")
    print(json.dumps(result, indent=2, ensure_ascii=False))
