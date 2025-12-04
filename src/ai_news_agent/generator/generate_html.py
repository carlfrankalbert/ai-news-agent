#!/usr/bin/env python3
"""
Generate HTML report from rankings JSON.
Output goes to docs/ for GitHub Pages publishing.
"""
import json
from pathlib import Path
from datetime import datetime

from ..config import OUTPUT_DIR

OUTPUT_DIR_PATH = Path(OUTPUT_DIR)
DOCS_DIR = Path("docs")
DATA_DIR = Path("data")

# Load tool links mapping
TOOL_LINKS = {}
TOOL_LINKS_FILE = DATA_DIR / "tool_links.json"
if TOOL_LINKS_FILE.exists():
    try:
        with open(TOOL_LINKS_FILE, "r", encoding="utf-8") as f:
            tool_links_data = json.load(f)
            TOOL_LINKS = tool_links_data.get("tools", {})
    except Exception as e:
        print(f"Warning: Could not load tool_links.json: {e}")

def get_tool_link(tool_name: str) -> str:
    """Get tool URL from mapping, or return empty string if not found."""
    return TOOL_LINKS.get(tool_name, {}).get("tool_url", "")

def get_provider_link_from_tool(tool_name: str) -> str:
    """Get provider URL from tool mapping, or return empty string if not found."""
    return TOOL_LINKS.get(tool_name, {}).get("provider_url", "")

# Map category slugs to design category names
CATEGORY_MAP = {
    "core-llms": "core-llm",
    "code-assistants": "code-assistants",
    "builder-platform": "builder-platform",
    "image-video": "image-video",
    "audio-voice": "audio-voice",
    "agents-automation": "agents"
}

# Map category names to display names
CATEGORY_DISPLAY_NAMES = {
    "core-llms": "Kjerne-LLM-er",
    "code-assistants": "Kodeassistenter",
    "builder-platform": "Builder & API",
    "image-video": "Bilde & Video",
    "audio-voice": "Lyd & Stemme",
    "agents-automation": "Agenter & Automatisering"
}

# Map provider names to logos and websites
PROVIDER_INFO = {
    "Anthropic": {
        "logo": "https://www.anthropic.com/favicon.ico",
        "website": "https://www.anthropic.com"
    },
    "OpenAI": {
        "logo": "https://openai.com/favicon.ico",
        "website": "https://openai.com"
    },
    "Google": {
        "logo": "https://www.google.com/favicon.ico",
        "website": "https://ai.google.dev"
    },
    "Meta": {
        "logo": "https://www.meta.com/favicon.ico",
        "website": "https://ai.meta.com"
    },
    "Mistral AI": {
        "logo": "https://mistral.ai/favicon.ico",
        "website": "https://mistral.ai"
    },
    "DeepSeek": {
        "logo": "https://www.deepseek.com/favicon.ico",
        "website": "https://www.deepseek.com"
    },
    "xAI": {
        "logo": "https://x.ai/favicon.ico",
        "website": "https://x.ai"
    },
    "Cohere": {
        "logo": "https://cohere.com/favicon.ico",
        "website": "https://cohere.com"
    },
    "Microsoft": {
        "logo": "https://www.microsoft.com/favicon.ico",
        "website": "https://www.microsoft.com"
    },
    "Alibaba": {
        "logo": "https://www.alibaba.com/favicon.ico",
        "website": "https://www.alibaba.com"
    },
    "Anysphere": {
        "logo": "https://cursor.sh/favicon.ico",
        "website": "https://cursor.sh"
    },
    "Microsoft/GitHub": {
        "logo": "https://github.com/favicon.ico",
        "website": "https://github.com/features/copilot"
    },
    "Continue": {
        "logo": "https://continue.dev/favicon.ico",
        "website": "https://continue.dev"
    },
    "Aider": {
        "logo": "https://aider.chat/favicon.ico",
        "website": "https://aider.chat"
    },
    "Codeium": {
        "logo": "https://codeium.com/favicon.ico",
        "website": "https://codeium.com"
    },
    "Sourcegraph": {
        "logo": "https://sourcegraph.com/favicon.ico",
        "website": "https://sourcegraph.com"
    },
    "Tabnine": {
        "logo": "https://www.tabnine.com/favicon.ico",
        "website": "https://www.tabnine.com"
    },
    "JetBrains": {
        "logo": "https://www.jetbrains.com/favicon.ico",
        "website": "https://www.jetbrains.com"
    },
    "Amazon": {
        "logo": "https://aws.amazon.com/favicon.ico",
        "website": "https://aws.amazon.com/codewhisperer"
    },
    "Ollama": {
        "logo": "https://ollama.com/favicon.ico",
        "website": "https://ollama.com"
    },
    "LangChain": {
        "logo": "https://www.langchain.com/favicon.ico",
        "website": "https://www.langchain.com"
    },
    "Hugging Face": {
        "logo": "https://huggingface.co/favicon.ico",
        "website": "https://huggingface.co"
    },
    "LlamaIndex": {
        "logo": "https://www.llamaindex.ai/favicon.ico",
        "website": "https://www.llamaindex.ai"
    },
    "vLLM Team": {
        "logo": "https://vllm.readthedocs.io/favicon.ico",
        "website": "https://vllm.ai"
    },
    "Together": {
        "logo": "https://together.ai/favicon.ico",
        "website": "https://together.ai"
    },
    "Groq": {
        "logo": "https://groq.com/favicon.ico",
        "website": "https://groq.com"
    },
    "Replicate": {
        "logo": "https://replicate.com/favicon.ico",
        "website": "https://replicate.com"
    },
    "Midjourney": {
        "logo": "https://www.midjourney.com/favicon.ico",
        "website": "https://www.midjourney.com"
    },
    "AUTOMATIC1111": {
        "logo": "https://github.com/AUTOMATIC1111/stable-diffusion-webui/favicon.ico",
        "website": "https://github.com/AUTOMATIC1111/stable-diffusion-webui"
    },
    "Black Forest Labs": {
        "logo": "https://blackforestlabs.ai/favicon.ico",
        "website": "https://blackforestlabs.ai"
    },
    "Runway": {
        "logo": "https://runwayml.com/favicon.ico",
        "website": "https://runwayml.com"
    },
    "ComfyUI": {
        "logo": "https://github.com/comfyanonymous/ComfyUI/favicon.ico",
        "website": "https://github.com/comfyanonymous/ComfyUI"
    },
    "Leonardo": {
        "logo": "https://leonardo.ai/favicon.ico",
        "website": "https://leonardo.ai"
    },
    "Ideogram": {
        "logo": "https://ideogram.ai/favicon.ico",
        "website": "https://ideogram.ai"
    },
    "Kling": {
        "logo": "https://klingai.com/favicon.ico",
        "website": "https://klingai.com"
    },
    "ElevenLabs": {
        "logo": "https://elevenlabs.io/favicon.ico",
        "website": "https://elevenlabs.io"
    },
    "Suno AI": {
        "logo": "https://suno.ai/favicon.ico",
        "website": "https://suno.ai"
    },
    "Suno": {
        "logo": "https://suno.ai/favicon.ico",
        "website": "https://suno.ai"
    },
    "Udio": {
        "logo": "https://udio.com/favicon.ico",
        "website": "https://udio.com"
    },
    "2noise": {
        "logo": "https://github.com/2noise/ChatTTS/favicon.ico",
        "website": "https://github.com/2noise/ChatTTS"
    },
    "Piper": {
        "logo": "https://github.com/rhasspy/piper/favicon.ico",
        "website": "https://github.com/rhasspy/piper"
    },
    "Coqui": {
        "logo": "https://coqui.ai/favicon.ico",
        "website": "https://coqui.ai"
    },
    "RVC": {
        "logo": "https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/favicon.ico",
        "website": "https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI"
    },
    "MeloTTS": {
        "logo": "https://github.com/myshell-ai/MeloTTS/favicon.ico",
        "website": "https://github.com/myshell-ai/MeloTTS"
    },
    "Significant Gravitas": {
        "logo": "https://github.com/Significant-Gravitas/AutoGPT/favicon.ico",
        "website": "https://github.com/Significant-Gravitas/AutoGPT"
    },
    "n8n": {
        "logo": "https://n8n.io/favicon.ico",
        "website": "https://n8n.io"
    },
    "joaomdmoura": {
        "logo": "https://github.com/joaomdmoura/crewAI/favicon.ico",
        "website": "https://github.com/joaomdmoura/crewAI"
    },
    "LangChain": {
        "logo": "https://www.langchain.com/favicon.ico",
        "website": "https://www.langchain.com/langgraph"
    },
    "AgentGPT": {
        "logo": "https://agentgpt.reworkd.ai/favicon.ico",
        "website": "https://agentgpt.reworkd.ai"
    },
    "SuperAGI": {
        "logo": "https://superagi.com/favicon.ico",
        "website": "https://superagi.com"
    },
    "BabyAGI": {
        "logo": "https://github.com/yoheinakajima/babyagi/favicon.ico",
        "website": "https://github.com/yoheinakajima/babyagi"
    },
    "Swarm": {
        "logo": "https://github.com/swarmdotai/swarm/favicon.ico",
        "website": "https://github.com/swarmdotai/swarm"
    }
}

def get_provider_logo(provider: str) -> str:
    """Get logo URL for a provider, or return empty string if not found."""
    info = PROVIDER_INFO.get(provider)
    if info:
        return info.get("logo", "")
    return ""

def get_provider_website(provider: str) -> str:
    """Get website URL for a provider, or return empty string if not found."""
    info = PROVIDER_INFO.get(provider)
    if info:
        return info.get("website", "")
    return ""

def convert_score(score_1_5):
    """Convert score from 1-5 scale to 0-100 scale."""
    if score_1_5 is None:
        return 0
    return int((score_1_5 / 5) * 100)

def get_trend_symbol(trend):
    """Get trend symbol (↑, ↓, →, —) from trend data."""
    if not trend:
        return "—"
    
    status = trend.get("status", "")
    rank_change = trend.get("rank_change")
    
    if status == "new":
        return "—"  # New items show as dash
    elif status == "rising" or (rank_change and rank_change > 0):
        return "↑"
    elif status == "falling" or (rank_change and rank_change < 0):
        return "↓"
    elif status == "stable" or rank_change == 0:
        return "→"
    else:
        return "—"

def get_trend_class(trend):
    """Get CSS class for trend cell."""
    if not trend:
        return ""
    
    status = trend.get("status", "")
    rank_change = trend.get("rank_change")
    
    if status == "rising" or (rank_change and rank_change > 0):
        return "up"
    elif status == "falling" or (rank_change and rank_change < 0):
        return "down"
    else:
        return ""

def generate_highlights_html(rankings: dict) -> str:
    """Generate highlights section (New This Month, Biggest Changes)."""
    # Collect new items
    new_items = []
    for cat in rankings.get("categories", []):
        for item in cat.get("top3", []):
            trend = item.get("trend", {})
            if trend.get("status") == "new":
                new_items.append({
                    "name": item.get("name", ""),
                    "provider": item.get("provider", "")
                })
    
    # Also include new_and_noteworthy
    for item in rankings.get("new_and_noteworthy", []):
        new_items.append({
            "name": item.get("name", ""),
            "provider": item.get("provider", "")
        })
    
    # Limit to top 4
    new_items = new_items[:4]
    
    # Collect biggest changes (rising/falling)
    changes = []
    for cat in rankings.get("categories", []):
        for item in cat.get("top3", []):
            trend = item.get("trend", {})
            rank_change = trend.get("rank_change")
            if rank_change and rank_change != 0:
                scores = item.get("scores", {})
                buzz_change = abs(rank_change) * 10  # Approximate
                changes.append({
                    "name": item.get("name", ""),
                    "change": rank_change,
                    "buzz_change": buzz_change,
                    "sentiment_change": abs(rank_change) * 5
                })
    
    # Sort by absolute change
    changes.sort(key=lambda x: abs(x["change"]), reverse=True)
    changes = changes[:4]
    
    new_html = ""
    for item in new_items:
        new_html += f"""<li><span class="highlight-name">{item['name']}</span><span class="new-badge">Ny</span></li>"""
    
    changes_html = ""
    for change in changes:
        direction = "trend-up" if change["change"] > 0 else "trend-down"
        arrow = "↑" if change["change"] > 0 else "↓"
        changes_html += f"""<li><span class="highlight-name">{change['name']}</span><span class="highlight-meta {direction}">{arrow}</span></li>"""
    
    # Only show sections that have content
    sections = []
    
    if new_items:
        sections.append(f"""
                <div class="highlight-card">
                    <h3><span class="icon">✦</span> <span data-i18n="new-this-month">Nytt</span></h3>
                    <ul class="highlight-list">{new_html}</ul>
                </div>""")
    
    if changes:
        sections.append(f"""
                <div class="highlight-card">
                    <h3><span class="icon">📈</span> <span data-i18n="biggest-changes">Trending</span></h3>
                    <ul class="highlight-list">{changes_html}</ul>
                </div>""")
    
    if not sections:
        return ""
    
    return f"""
            <!-- Highlights - Compact inline -->
            <section class="highlights">{''.join(sections)}
            </section>"""

def generate_category_table_html(category: dict) -> str:
    """Generate table HTML for a category with expandable rows."""
    slug = category.get("slug", "")
    display_name = CATEGORY_DISPLAY_NAMES.get(slug, category.get("name", ""))
    category_data_attr = CATEGORY_MAP.get(slug, slug)
    
    rows_html = ""
    # Try top10 first, fallback to top3, then items
    all_items = category.get("top10", category.get("top3", category.get("items", [])))
    
    # Limit to max 10 items
    all_items = all_items[:10]
    
    # Add rank numbers
    for idx, item in enumerate(all_items, 1):
        rank = item.get("rank", idx)
        rank_class = "rank-1" if rank == 1 else "rank-2" if rank == 2 else "rank-3" if rank == 3 else "rank-default"
        
        # Hide rows after the first 3 by default
        hidden_class = "hidden-row" if idx > 3 else ""
        
        scores = item.get("scores", {})
        buzz = convert_score(scores.get("buzz_momentum", 0))
        sentiment = convert_score(scores.get("sentiment", 0))
        utility = convert_score(scores.get("utility_for_knowledge_work", 0))
        price = convert_score(scores.get("price_performance", 0))
        
        # Score classes for color coding
        buzz_class = "score-high" if buzz >= 70 else "score-mid" if buzz >= 40 else "score-low"
        sentiment_class = "score-high" if sentiment >= 70 else "score-mid" if sentiment >= 40 else "score-low"
        utility_class = "score-high" if utility >= 70 else "score-mid" if utility >= 40 else "score-low"
        price_class = "score-high" if price >= 70 else "score-mid" if price >= 40 else "score-low"
        
        trend = item.get("trend", {})
        trend_symbol = get_trend_symbol(trend)
        trend_class = get_trend_class(trend)
        
        # Get provider info
        provider = item.get("provider", "")
        provider_logo = get_provider_logo(provider)
        provider_website = get_provider_website(provider)
        
        # Get tool and provider links from tool_links.json
        tool_name = item.get("name", "")
        tool_url = get_tool_link(tool_name)
        provider_url_from_tool = get_provider_link_from_tool(tool_name)
        
        # Prefer provider URL from tool mapping, fallback to PROVIDER_INFO
        if provider_url_from_tool:
            provider_website = provider_url_from_tool
        elif not provider_website:
            provider_website = ""
        
        # Build logo HTML
        logo_html = ""
        if provider_logo:
            logo_html = f'<img src="{provider_logo}" alt="{provider}" class="provider-logo" onerror="this.style.display=\'none\'">'
        
        # Build tool name HTML with link if available
        tool_name_html = tool_name
        if tool_url:
            tool_name_html = f'<a href="{tool_url}" target="_blank" rel="noopener noreferrer" class="item-name">{tool_name}</a>'
        else:
            tool_name_html = f'<span class="item-name">{tool_name}</span>'
        
        # Build provider HTML with link if available
        provider_html = provider
        if provider_website:
            provider_html = f'<a href="{provider_website}" target="_blank" rel="noopener noreferrer" class="item-provider">{provider}</a>'
        else:
            provider_html = f'<span class="item-provider">{provider}</span>'
        
        rows_html += f"""
                    <div class="ranking-row {hidden_class}" data-buzz="{buzz}" data-sentiment="{sentiment}" data-utility="{utility}" data-price="{price}">
                        <div class="rank-badge {rank_class}">{rank}</div>
                        <div class="item-info">
                            {tool_name_html}
                            <span class="item-provider">{logo_html}<span class="provider-text">{provider_html}</span></span>
                        </div>
                        <span class="score-cell {buzz_class}">{buzz}</span>
                        <span class="score-cell {sentiment_class}">{sentiment}</span>
                        <span class="score-cell {utility_class}">{utility}</span>
                        <span class="score-cell {price_class}">{price}</span>
                        <span class="trend-cell {trend_class}">{trend_symbol}</span>
                    </div>"""
    
    # Add expand button if there are more than 3 items
    expand_button = ""
    if len(all_items) > 3:
        expand_button = f"""
                    <div class="expand-section">
                        <button class="expand-button" data-category="{category_data_attr}" onclick="toggleExpand('{category_data_attr}')">
                            <span class="expand-text">Vis flere ({len(all_items) - 3} flere)</span>
                            <span class="expand-icon">↓</span>
                        </button>
                    </div>"""
    
    count_label = "modeller" if "llm" in slug.lower() else "verktøy" if "code" in slug.lower() or "image" in slug.lower() or "audio" in slug.lower() or "agents" in slug.lower() else "plattformer"
    
    return f"""
            <!-- {display_name} Category -->
            <section class="category-section" data-category="{category_data_attr}">
                <div class="category-header">
                    <h2 class="category-title" data-i18n="cat-{slug}">{display_name}</h2>
                    <span class="category-count">{len(all_items)} <span data-i18n="{count_label}">{count_label}</span></span>
                </div>
                <div class="rankings-table">
                    <div class="rankings-header">
                        <span>#</span>
                        <span data-sort="name">Navn <span class="sort-icon">↕</span></span>
                        <span data-sort="buzz">Buzz <span class="sort-icon">↕</span></span>
                        <span data-sort="sentiment">Sentiment <span class="sort-icon">↕</span></span>
                        <span data-sort="utility">Nytte <span class="sort-icon">↕</span></span>
                        <span data-sort="price">Pris <span class="sort-icon">↕</span></span>
                        <span>Trend</span>
                        <span></span>
                    </div>
{rows_html}{expand_button}
                </div>
            </section>"""

def format_period(period: str) -> str:
    """Format period string (YYYY-MM) to readable format."""
    try:
        year, month = period.split("-")
        month_names = {
            "01": "januar", "02": "februar", "03": "mars", "04": "april",
            "05": "mai", "06": "juni", "07": "juli", "08": "august",
            "09": "september", "10": "oktober", "11": "november", "12": "desember"
        }
        month_name = month_names.get(month, month)
        return f"{month_name} {year}"
    except:
        return period

# Load the HTML template from file
TEMPLATE_DIR = Path(__file__).parent / "templates"
TEMPLATE_FILE = TEMPLATE_DIR / "design.html"

def load_template() -> str:
    """Load the HTML template from file."""
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Template file not found: {TEMPLATE_FILE}\n"
            f"Make sure the template file exists in {TEMPLATE_DIR}"
        )

DESIGN_HTML = load_template()

def generate_html(rankings: dict) -> str:
    period = rankings.get("period", "")
    period_display = format_period(period)
    
    # Format last updated date
    generated_at = rankings.get("generated_at", "")
    if generated_at:
        try:
            dt = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
            day = dt.day
            month_num = dt.month
            year = dt.year
            month_names = {
                1: "jan", 2: "feb", 3: "mar", 4: "apr",
                5: "mai", 6: "jun", 7: "jul", 8: "aug",
                9: "sep", 10: "okt", 11: "nov", 12: "des"
            }
            month_name = month_names.get(month_num, "jan")
            last_updated = f"{day}. {month_name} {year}"
        except:
            last_updated = period_display
    else:
        last_updated = period_display
    
    # Generate highlights
    highlights_html = generate_highlights_html(rankings)
    
    # Generate categories
    categories_html = ""
    for cat in rankings.get("categories", []):
        categories_html += generate_category_table_html(cat)
    
    return DESIGN_HTML.format(
        period_display=period_display,
        highlights_html=highlights_html,
        categories_html=categories_html,
        last_updated=last_updated
    )


def main():
    import sys
    
    # Sjekk om --dummy flagg er satt
    use_dummy = "--dummy" in sys.argv
    
    if use_dummy:
        dummy_file = OUTPUT_DIR_PATH / "rankings_dummy.json"
        if not dummy_file.exists():
            print(f"❌ Dummy-fil ikke funnet: {dummy_file}")
            print("💡 Opprett output/rankings_dummy.json med test-data")
            return
        rankings_file = dummy_file
        print(f"🎨 Bruker dummy-data: {rankings_file}")
    else:
        # Finn nyeste rankings-fil
        rankings_files = list(OUTPUT_DIR_PATH.glob("rankings_*.json"))
        # Ekskluder dummy-fil fra automatisk valg
        rankings_files = [f for f in rankings_files if "dummy" not in f.name]
        
        if not rankings_files:
            print("Ingen rankings-filer funnet i output/")
            print("💡 Kjør med --dummy for å bruke test-data")
            return
        
        rankings_file = max(rankings_files, key=lambda f: f.stat().st_mtime)
        print(f"Genererer HTML fra {rankings_file}")
    
    with open(rankings_file) as f:
        rankings = json.load(f)
    
    # Håndter error case - prøv å ekstraktere data fra raw_response eller bruk forrige måned
    if "error" in rankings and "raw_response" in rankings:
        print("⚠️  Rankings har error, prøver å finne alternativ data...")
        
        # Først: prøv å bruke forrige måneds data hvis den finnes
        try:
            from datetime import datetime, timedelta
            period = rankings.get("period", "")
            if period:
                year, month = map(int, period.split("-"))
                prev_date = datetime(year, month, 1) - timedelta(days=1)
                prev_period = prev_date.strftime("%Y-%m")
                prev_file = OUTPUT_DIR_PATH / f"rankings_{prev_period}.json"
                
                if prev_file.exists():
                    with open(prev_file) as f:
                        prev_rankings = json.load(f)
                    if "categories" in prev_rankings and not ("error" in prev_rankings):
                        print(f"✅ Bruker forrige måneds data ({prev_period})")
                        rankings = prev_rankings
                        rankings["period"] = period  # Behold nåværende periode
                    else:
                        raise FileNotFoundError
                else:
                    raise FileNotFoundError
        except:
            # Fallback: prøv å ekstraktere fra raw_response
            print("⚠️  Ingen forrige måneds data, prøver å ekstraktere fra raw_response...")
            try:
                import json as json_module
                raw_response = rankings["raw_response"]
                if isinstance(raw_response, str):
                    # Fjern markdown code blocks
                    if "```json" in raw_response:
                        raw_response = raw_response.split("```json")[1].split("```")[0]
                    elif "```" in raw_response:
                        raw_response = raw_response.split("```")[1].split("```")[0]
                    
                    # Bruk dummy data som fallback
                    dummy_file = OUTPUT_DIR_PATH / "rankings_dummy.json"
                    if dummy_file.exists():
                        with open(dummy_file) as f:
                            rankings = json_module.load(f)
                        print("✅ Bruker dummy-data som fallback")
                    else:
                        raise FileNotFoundError("No fallback data available")
            except Exception as e:
                print(f"❌ Kunne ikke ekstraktere data: {e}")
                print("⚠️  HTML vil være tom - vennligst kjør pipeline på nytt")
    
    html = generate_html(rankings)
    
    # Lagre til docs/ for GitHub Pages
    DOCS_DIR.mkdir(exist_ok=True)
    output_path = DOCS_DIR / "index.html"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ HTML generert: {output_path}")


if __name__ == "__main__":
    main()
