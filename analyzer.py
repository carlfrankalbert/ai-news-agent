"""
AI Tool Analyzer - bruker Claude til å analysere og rangere AI-verktøy
"""
import json
import os
from datetime import datetime
from anthropic import Anthropic
from config import CATEGORIES


def create_analysis_prompt(posts, period: str) -> str:
    """
    Lag prompt for Claude-analyse.
    """
    posts_summary = "\n".join([
        f"- [{p['points']} pts, {p['num_comments']} comments] [{p.get('source', 'unknown')}] {p['title']}"
        for p in posts[:200]  # Begrens for context window
    ])
    
    categories_desc = "\n".join([
        f"- {c['slug']}: {c['name']} (eks: {', '.join(c['examples'])})"
        for c in CATEGORIES
    ])
    
    # Tell kilder
    sources = {}
    for p in posts:
        source = p.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    sources_str = ", ".join([f"{k}: {v}" for k, v in sources.items()])
    
    return f"""Analyser disse postene om AI-verktøy fra ulike kilder (siste 90 dager) og lag en rangering.

Kilder: {sources_str}

## Posts (sortert etter points):
{posts_summary}

## Kategorier å rangere:
{categories_desc}

## Oppgave:
1. Identifiser hvilke AI-verktøy/modeller som nevnes mest og har mest momentum
2. For hver kategori, ranger topp 3 verktøy basert på:
   - Hvor mye de diskuteres (buzz/momentum)
   - Generell sentiment (positivt/negativt)
   - Nytte for kunnskapsarbeidere
   - Pris/ytelse-forhold (hvis relevant)

3. Identifiser 2-3 "new & noteworthy" verktøy som er nye/spennende men ikke topp 3 ennå

## Output JSON-format (følg eksakt):
{{
  "period": "{period}",
  "generated_at": "{datetime.now().isoformat()}",
  "data_source": "hackernews",
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
        {{ "rank": 3, "medal": "bronze", ... }}
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
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
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
        print(f"Feil ved parsing av JSON: {e}")
        print(f"Raw response:\n{response_text[:500]}...")
        return {"error": str(e), "raw_response": response_text}


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
