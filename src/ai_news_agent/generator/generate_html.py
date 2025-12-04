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
    all_items = category.get("top3", [])
    
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

# Read the design template and extract the HTML structure
DESIGN_HTML = """<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FYRK AI Radar – {period_display}</title>
    <meta name="description" content="En månedlig oversikt over hva som faktisk skjer i AI. Basert på signaler fra Hacker News, Github, X og sentimentanalyse.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #fafafa;
            --bg-card: #ffffff;
            --bg-muted: #f4f4f5;
            --text-primary: #18181b;
            --text-secondary: #71717a;
            --text-muted: #a1a1aa;
            --border: rgba(0, 0, 0, 0.05);
            --border-subtle: rgba(0, 0, 0, 0.03);
            --transition-base: 150ms ease;
            --transition-fast: 120ms ease;
            --transition-slow: 180ms ease;
            --accent-primary: #2563eb;
            --accent-primary-light: #dbeafe;
            --accent-success: #16a34a;
            --accent-success-light: #dcfce7;
            --accent-warning: #ea580c;
            --accent-warning-light: #fed7aa;
            --accent-danger: #dc2626;
            --gold: #ca8a04;
            --silver: #71717a;
            --bronze: #a16207;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
            --space-2xl: 48px;
            --space-3xl: 64px;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'DM Sans', system-ui, -apple-system, sans-serif;
            background: linear-gradient(180deg, #fafafa 0%, #f8f8f8 100%);
            color: var(--text-primary);
            line-height: 1.6;
            font-size: 15px;
            -webkit-font-smoothing: antialiased;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1080px;
            margin: 0 auto;
            padding: 0 var(--space-lg);
        }}

        /* Header / Logo */
        .site-header {{
            padding: var(--space-lg) 0;
            border-bottom: 0.5px solid var(--border);
            transition: border-color var(--transition-base);
        }}

        .site-header .container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .logo {{
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            text-decoration: none;
            color: var(--text-primary);
        }}

        .logo-mark {{
            width: 32px;
            height: 32px;
            background: var(--text-primary);
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: -0.5px;
        }}

        .logo-text {{
            font-weight: 700;
            font-size: 18px;
            letter-spacing: -0.3px;
        }}

        .header-nav {{
            display: flex;
            gap: var(--space-lg);
        }}

        .header-nav a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color var(--transition-base);
        }}

        .header-nav a:hover {{
            color: var(--text-primary);
        }}

        .lang-switcher {{
            display: flex;
            gap: 2px;
            background: var(--bg-muted);
            border-radius: var(--radius-sm);
            padding: 2px;
        }}

        .lang-btn {{
            background: transparent;
            border: none;
            padding: 4px 10px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-radius: 4px;
            font-family: inherit;
            transition: all var(--transition-base);
        }}

        .lang-btn:hover {{
            color: var(--text-primary);
        }}

        .lang-btn.active {{
            background: var(--bg-card);
            color: var(--text-primary);
            box-shadow: var(--shadow-sm);
        }}

        .logo-picture {{
            display: block;
        }}

        .logo-img {{
            height: 40px;
            width: auto;
            display: block;
        }}
        
        .logo-img[style*="display: none"] {{
            display: none !important;
        }}

        /* Hero Section */
        .hero {{
            padding: calc(var(--space-3xl) * 1.2) 0 calc(var(--space-2xl) * 1.2);
            text-align: center;
            position: relative;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 800px;
            height: 100%;
            background: radial-gradient(ellipse at center, rgba(37, 99, 235, 0.03) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }}

        .hero > * {{
            position: relative;
            z-index: 1;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: var(--space-xs);
            background: var(--accent-primary-light);
            color: var(--accent-primary);
            padding: 6px 12px;
            border-radius: 100px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: var(--space-lg);
        }}

        .hero-badge::before {{
            content: '';
            width: 6px;
            height: 6px;
            background: var(--accent-primary);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}

        .hero h1 {{
            font-size: clamp(32px, 5vw, 48px);
            font-weight: 700;
            letter-spacing: -1px;
            line-height: 1.1;
            margin-bottom: var(--space-md);
            color: var(--text-primary);
        }}

        .hero-subtitle {{
            font-size: 17px;
            color: var(--text-secondary);
            max-width: 560px;
            margin: 0 auto;
            line-height: 1.6;
            letter-spacing: 0.01em;
        }}

        /* Highlights Row - Compact inline style */
        .highlights {{
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-md);
            margin-bottom: var(--space-xl);
            align-items: center;
        }}

        .highlight-card {{
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            background: var(--bg-card);
            border: 0.5px solid var(--border);
            border-radius: 100px;
            padding: var(--space-xs) var(--space-xl);
            box-shadow: var(--shadow-sm);
            position: relative;
            transition: all var(--transition-base);
            box-shadow: 0 1px 2px rgba(0,0,0,0.04), inset 0 0.5px 0 rgba(255,255,255,0.8);
        }}

        .highlight-card::before {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 100px;
            padding: 0.5px;
            background: linear-gradient(135deg, rgba(255,255,255,0.5), rgba(0,0,0,0.02));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }}

        .highlight-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.08), inset 0 0.5px 0 rgba(255,255,255,0.8);
            transform: translateY(-1px);
        }}

        .highlight-card:first-of-type {{
            background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
        }}

        .highlight-card:last-of-type {{
            background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
        }}

        .highlight-card h3 {{
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin: 0;
            display: flex;
            align-items: center;
            gap: var(--space-xs);
            white-space: nowrap;
        }}

        .highlight-card h3 .icon {{
            font-size: 14px;
        }}

        .highlight-list {{
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-xs);
            margin: 0;
            padding: 0;
        }}

        .highlight-list li {{
            display: inline-flex;
            align-items: center;
            gap: var(--space-xs);
            padding: 0;
            border: none;
        }}

        .highlight-list li:not(:last-child)::after {{
            content: "•";
            color: var(--text-muted);
            margin-left: var(--space-xs);
        }}

        .highlight-name {{
            font-weight: 500;
            font-size: 13px;
            color: var(--text-primary);
        }}

        .highlight-meta {{
            font-size: 11px;
            color: var(--text-muted);
            font-family: 'IBM Plex Mono', monospace;
        }}

        .trend-up {{
            color: var(--accent-success);
        }}

        .trend-down {{
            color: var(--accent-danger);
        }}

        .new-badge {{
            background: var(--accent-success-light);
            color: var(--accent-success);
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 100px;
            text-transform: uppercase;
        }}

        /* Metrics Info */
        .metrics-info {{
            background: var(--bg-card);
            border: 0.5px solid var(--border);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            margin-bottom: var(--space-2xl);
            box-shadow: var(--shadow-sm);
            position: relative;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04), inset 0 0.5px 0 rgba(255,255,255,0.8);
        }}

        .metrics-info::before {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: var(--radius-lg);
            padding: 0.5px;
            background: linear-gradient(135deg, rgba(255,255,255,0.5), rgba(0,0,0,0.02));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }}

        .metrics-info h3 {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: var(--space-md);
            color: var(--text-primary);
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--space-md);
        }}

        .metric-item {{
            display: flex;
            align-items: flex-start;
            gap: var(--space-sm);
        }}

        .metric-label {{
            font-weight: 600;
            color: var(--text-primary);
            font-size: 13px;
            min-width: 70px;
        }}

        .metric-desc {{
            font-size: 13px;
            color: var(--text-secondary);
        }}

        /* Filter Controls */
        .filter-bar {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: var(--space-md);
            margin-bottom: var(--space-xl);
            padding-bottom: var(--space-lg);
            border-bottom: 0.5px solid var(--border);
        }}

        .filter-label {{
            font-size: 13px;
            font-weight: 500;
            color: var(--text-secondary);
        }}
        
        .filter-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-sm);
        }}

        .filter-pill {{
            background: var(--bg-muted);
            border: 0.5px solid transparent;
            border-radius: 100px;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all var(--transition-base);
            font-family: inherit;
        }}

        .filter-pill:hover {{
            background: var(--bg-card);
            border-color: var(--border);
            color: var(--text-primary);
            transform: scale(1.02);
        }}

        .filter-pill.active {{
            background: linear-gradient(135deg, var(--text-primary) 0%, #2a2a2e 100%);
            color: white;
            border-color: var(--text-primary);
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.2), 0 1px 2px rgba(0,0,0,0.1);
        }}

        /* Category Sections */
        .category-section {{
            margin-bottom: var(--space-2xl);
        }}

        .category-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: var(--space-lg);
        }}

        .category-title {{
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.3px;
        }}

        .category-count {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        /* Rankings Table */
        .rankings-table {{
            background: var(--bg-card);
            border: 0.5px solid var(--border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
            position: relative;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04), inset 0 0.5px 0 rgba(255,255,255,0.8);
        }}

        .rankings-table::before {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: var(--radius-lg);
            padding: 0.5px;
            background: linear-gradient(135deg, rgba(255,255,255,0.5), rgba(0,0,0,0.02));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
            z-index: 1;
        }}

        .rankings-header {{
            display: grid;
            grid-template-columns: 50px 1fr 80px 80px 80px 80px 60px 30px;
            gap: var(--space-md);
            padding: var(--space-md) var(--space-lg);
            background: var(--bg-muted);
            border-bottom: 0.5px solid var(--border);
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: sticky;
            top: 0;
            z-index: 10;
            backdrop-filter: blur(8px);
            background: rgba(244, 244, 245, 0.95);
        }}
        
        .rankings-header span {{
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            user-select: none;
        }}

        .rankings-header span:hover {{
            color: var(--text-primary);
        }}

        .sort-icon {{
            font-size: 10px;
            opacity: 0.5;
        }}

        .sort-icon.active {{
            opacity: 1;
        }}

        .ranking-row {{
            display: grid;
            grid-template-columns: 50px 1fr 80px 80px 80px 80px 60px 30px;
            gap: var(--space-md);
            padding: var(--space-md) var(--space-lg);
            border-bottom: 0.5px solid var(--border-subtle);
            align-items: center;
            transition: all var(--transition-base);
            position: relative;
            cursor: pointer;
        }}

        .ranking-row:last-child {{
            border-bottom: none;
        }}

        .ranking-row:hover {{
            background: rgba(0, 0, 0, 0.02);
        }}

        .ranking-row::after {{
            content: '›';
            position: absolute;
            right: var(--space-lg);
            color: var(--text-muted);
            font-size: 18px;
            opacity: 0;
            transition: opacity var(--transition-base), transform var(--transition-base);
            transform: translateX(-4px);
        }}

        .ranking-row:hover::after {{
            opacity: 1;
            transform: translateX(0);
        }}

        .rank-badge {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 13px;
            border: 2px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }}

        .rank-1 {{ 
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 237, 78, 0.2), rgba(255, 215, 0, 0.15));
            color: #b8860b;
            border-color: rgba(184, 134, 11, 0.2);
            box-shadow: 0 1px 3px rgba(184, 134, 11, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.6), inset 0 -1px 0 rgba(0, 0, 0, 0.05);
        }}
        .rank-2 {{ 
            background: linear-gradient(135deg, rgba(192, 192, 192, 0.15), rgba(232, 232, 232, 0.2), rgba(192, 192, 192, 0.15));
            color: #6b6b6b;
            border-color: rgba(107, 107, 107, 0.2);
            box-shadow: 0 1px 3px rgba(107, 107, 107, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.6), inset 0 -1px 0 rgba(0, 0, 0, 0.05);
        }}
        .rank-3 {{ 
            background: linear-gradient(135deg, rgba(205, 127, 50, 0.15), rgba(230, 168, 87, 0.2), rgba(205, 127, 50, 0.15));
            color: #8b4513;
            border-color: rgba(139, 69, 19, 0.2);
            box-shadow: 0 1px 3px rgba(139, 69, 19, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.5), inset 0 -1px 0 rgba(0, 0, 0, 0.05);
        }}
        .rank-default {{ 
            background: var(--bg-muted); 
            color: var(--text-muted);
            border-color: transparent;
            box-shadow: none;
        }}

        .item-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .item-name {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .item-provider {{
            font-size: 13px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .provider-logo {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            object-fit: contain;
            flex-shrink: 0;
        }}

        .provider-text {{
            display: inline;
        }}

        .provider-link {{
            color: var(--text-muted);
            text-decoration: none;
            transition: color var(--transition-base);
        }}

        .provider-link:hover {{
            color: var(--accent-primary);
            text-decoration: underline;
        }}

        .score-cell {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 14px;
            font-weight: 500;
            text-align: center;
        }}

        .score-high {{ color: var(--accent-success); }}
        .score-mid {{ color: var(--text-secondary); }}
        .score-low {{ color: var(--accent-danger); }}

        .trend-cell {{
            display: flex;
            justify-content: center;
            color: var(--text-muted);
            font-size: 14px;
        }}

        .trend-cell.up {{ color: var(--accent-success); }}
        .trend-cell.down {{ color: var(--accent-danger); }}

        /* CTA Section */
        .cta-section {{
            background: var(--bg-card);
            border: 0.5px solid var(--border);
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            text-align: center;
            margin: var(--space-3xl) 0;
            box-shadow: var(--shadow-sm);
            position: relative;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04), inset 0 0.5px 0 rgba(255,255,255,0.8);
        }}

        .cta-section::before {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: var(--radius-lg);
            padding: 0.5px;
            background: linear-gradient(135deg, rgba(255,255,255,0.5), rgba(0,0,0,0.02));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }}

        .cta-section h3 {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: var(--space-sm);
            letter-spacing: -0.3px;
        }}

        .cta-section p {{
            color: var(--text-secondary);
            margin-bottom: var(--space-lg);
            max-width: 480px;
            margin-left: auto;
            margin-right: auto;
        }}

        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            background: var(--text-primary);
            color: white;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 14px;
            transition: all var(--transition-base);
        }}

        .cta-button:hover {{
            background: #3f3f46;
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}

        /* Footer */
        .site-footer {{
            border-top: 0.5px solid var(--border);
            padding: calc(var(--space-xl) * 1.2) 0;
            margin-top: var(--space-2xl);
            position: relative;
        }}

        .site-footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 40px;
            background: linear-gradient(180deg, rgba(250, 250, 250, 0) 0%, rgba(250, 250, 250, 1) 100%);
            pointer-events: none;
        }}

        .footer-content {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: var(--space-md);
        }}

        .footer-brand {{
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .footer-brand .logo-mark {{
            width: 24px;
            height: 24px;
            font-size: 11px;
        }}

        .footer-links {{
            display: flex;
            gap: var(--space-lg);
        }}

        .footer-links a {{
            font-size: 13px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: color var(--transition-base);
        }}

        .footer-links a:hover {{
            color: var(--text-primary);
        }}

        .footer-meta {{
            font-size: 11px;
            color: var(--text-muted);
            font-family: 'IBM Plex Mono', monospace;
            opacity: 0.8;
        }}

        .footer-logo-img {{
            height: 32px;
            width: auto;
            display: inline-block;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .rankings-header,
            .ranking-row {{
                grid-template-columns: 40px 1fr 60px 60px 30px;
            }}

            .rankings-header span:nth-child(5),
            .rankings-header span:nth-child(6),
            .rankings-header span:nth-child(7),
            .ranking-row > *:nth-child(5),
            .ranking-row > *:nth-child(6),
            .ranking-row > *:nth-child(7) {{
                display: none;
            }}

            .ranking-row::after {{
                right: var(--space-md);
            }}

            .header-nav {{
                display: none;
            }}

            .highlights {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .highlight-card {{
                width: 100%;
                flex-wrap: wrap;
            }}

            .metrics-grid {{
                grid-template-columns: 1fr;
            }}

            .filter-bar {{
                flex-direction: column;
                align-items: flex-start;
            }}

            .footer-content {{
                flex-direction: column;
                text-align: center;
            }}
        }}

        /* Hidden category sections */
        .category-section.hidden {{
            display: none;
        }}
        
        /* Expandable rows */
        .ranking-row.hidden-row {{
            display: none;
        }}
        
        .ranking-row.hidden-row.expanded {{
            display: grid;
        }}
        
        .expand-section {{
            padding: var(--space-md) var(--space-lg);
            text-align: center;
            border-top: 1px solid var(--border-subtle);
        }}
        
        .expand-button {{
            background: transparent;
            border: 0.5px solid var(--border);
            border-radius: var(--radius-md);
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all var(--transition-base);
            font-family: inherit;
            display: inline-flex;
            align-items: center;
            gap: var(--space-xs);
        }}
        
        .expand-button:hover {{
            background: var(--bg-muted);
            border-color: var(--text-muted);
            color: var(--text-primary);
        }}
        
        .expand-icon {{
            transition: transform 0.2s;
            font-size: 12px;
        }}
        
        .expand-button.expanded .expand-icon {{
            transform: rotate(180deg);
        }}
        
        .expand-text {{
            margin-right: 4px;
        }}

        /* Tab Navigation */
        .tab-bar {{
            display: flex;
            gap: var(--space-xl);
            border-bottom: 1px solid var(--border);
            margin-bottom: var(--space-lg);
            padding: 0 var(--space-lg);
        }}

        .tab {{
            padding: var(--space-md) 0;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            background: none;
            border: none;
            cursor: pointer;
            position: relative;
            font-family: inherit;
            transition: color var(--transition-base);
        }}

        .tab:hover {{
            color: var(--text-primary);
        }}

        .tab.active {{
            color: var(--text-primary);
        }}

        .tab.active::after {{
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--text-primary);
        }}

        .tab-content {{
            display: block;
        }}

        .tab-content.hidden {{
            display: none;
        }}

        /* Lab Banner */
        .lab-banner {{
            display: flex;
            align-items: center;
            gap: var(--space-md);
            background: var(--bg-muted);
            padding: 8px 16px;
            border-radius: var(--radius-md);
            margin-bottom: var(--space-lg);
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .lab-banner.hidden {{
            display: none;
        }}

        .lab-badge {{
            background: rgba(0,0,0,0.05);
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            font-weight: 600;
            color: var(--text-primary);
            white-space: nowrap;
        }}

        .lab-text {{
            flex: 1;
        }}

        .lab-text a {{
            color: var(--accent-primary);
            text-decoration: none;
        }}

        .lab-dismiss {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 20px;
            line-height: 1;
            cursor: pointer;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        /* Capabilities Section */
        .capabilities-section {{
            margin-bottom: var(--space-lg);
            background: var(--bg-card);
            border: 0.5px solid var(--border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }}

        .capabilities-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: var(--space-md) var(--space-lg);
            border-bottom: 0.5px solid var(--border);
        }}

        .capabilities-title-group {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .capabilities-title {{
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .capabilities-subtitle {{
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .capabilities-legend {{
            display: flex;
            align-items: center;
            gap: var(--space-md);
            font-size: 12px;
            color: var(--text-secondary);
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .capabilities-content {{
            overflow-x: auto;
        }}

        .capabilities-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .capabilities-table th {{
            padding: var(--space-md);
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            color: var(--text-primary);
            border-bottom: 1px solid var(--border);
        }}

        .capabilities-table td {{
            padding: var(--space-md);
            border-bottom: 1px solid var(--border-subtle);
        }}

        .capability-cell {{
            text-align: center;
            font-size: 16px;
        }}

        .capabilities-mobile {{
            display: none;
        }}

        /* About Section */
        .about-section {{
            margin-top: var(--space-2xl);
            padding: var(--space-xl);
            background: var(--bg-card);
            border-radius: var(--radius-lg);
        }}

        .about-section h2 {{
            font-size: 24px;
            margin-bottom: var(--space-md);
        }}

        .about-section h3 {{
            font-size: 18px;
            margin-top: var(--space-lg);
            margin-bottom: var(--space-sm);
        }}

        .about-section ul {{
            list-style: none;
            padding-left: 0;
        }}

        .about-section ul li {{
            padding-left: var(--space-lg);
            position: relative;
        }}

        .about-section ul li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--text-secondary);
        }}

        .disclaimer {{
            margin-top: var(--space-lg);
            padding: var(--space-md);
            background: var(--bg-muted);
            border-radius: var(--radius-md);
            font-style: italic;
            color: var(--text-secondary);
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="site-header">
    <div class="container">
            <a href="https://fyrk.no" class="logo">
                <picture class="logo-picture">
                    <img src="assets/fyrk-logo-primary-navy.svg" alt="FYRK" class="logo-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                </picture>
                <div class="logo-mark" style="display: none;">F</div>
            </a>
            <nav class="header-nav">
                <div class="lang-switcher">
                    <button class="lang-btn active" data-lang="no">NO</button>
                    <button class="lang-btn" data-lang="sv">SV</button>
                    <button class="lang-btn" data-lang="en">EN</button>
                </div>
                <a href="mailto:hei@fyrk.no?subject=FYRK%20AI%20Radar">Kontakt</a>
            </nav>
        </div>
        </header>
        
    <main>
        <div class="container">
            <!-- Tab Navigation -->
            <nav class="tab-bar" role="tablist">
                <button class="tab active" role="tab" aria-selected="true" data-tab="scores" id="tab-btn-scores" data-i18n="tab-scores">Scores</button>
                <button class="tab" role="tab" aria-selected="false" data-tab="kapabiliteter" id="tab-btn-kapabiliteter" data-i18n="tab-capabilities">Kapabiliteter</button>
            </nav>

            <!-- Lab Banner -->
            <div class="lab-banner" id="lab-banner">
                <span class="lab-badge" data-i18n="lab-badge">🧪 FYRK Lab</span>
                <span class="lab-text"><span data-i18n="lab-text">Et eksperiment – ikke en benchmark.</span> <a href="#om" data-i18n="les-mer">Les mer</a></span>
                <button class="lab-dismiss" aria-label="Lukk" data-i18n-attr="aria-label" data-i18n-attr-key="close" onclick="dismissLabBanner()">×</button>
            </div>

            <!-- Scores Tab Content -->
            <div class="tab-content" id="tab-scores" role="tabpanel" aria-labelledby="tab-btn-scores">
            <!-- Hero Section -->
            <section class="hero">
                <span class="hero-badge" data-i18n="hero-badge">Oppdatert {period_display}</span>
                <h1>FYRK AI Radar</h1>
                <p class="hero-subtitle" data-i18n="hero-subtitle">En månedlig oversikt over hva som faktisk skjer i AI. Basert på signaler fra Hacker News, Github, X og sentimentanalyse.</p>
            </section>

{highlights_html}

            <!-- Metrics Explanation -->
            <section class="metrics-info">
                <h3 data-i18n="metrics-title">Slik leser du dataene</h3>
                <div class="metrics-grid">
                    <div class="metric-item">
                        <span class="metric-label">Buzz</span>
                        <span class="metric-desc" data-i18n="metric-buzz">Hvor mye modellen/verktøyet diskuteres (0–100)</span>
        </div>
                    <div class="metric-item">
                        <span class="metric-label">Sentiment</span>
                        <span class="metric-desc" data-i18n="metric-sentiment">Hvor positivt/negativt det omtales i communityet</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label" data-i18n="label-utility">Nytte</span>
                        <span class="metric-desc" data-i18n="metric-utility">Opplevd praktisk nytteverdi</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label" data-i18n="label-price">Pris</span>
                        <span class="metric-desc" data-i18n="metric-price">Opplevd kost/nytte (lavere = bedre verdi)</span>
                    </div>
                </div>
            </section>

            <!-- Filter Controls -->
            <section class="filter-bar">
                <span class="filter-label" data-i18n="filter-label">Filtrer etter kategori:</span>
                <div class="filter-pills">
                    <button class="filter-pill active" data-category="all" data-i18n="filter-all">Alle</button>
                    <button class="filter-pill" data-category="core-llm" data-i18n="cat-core-llm">Kjerne-LLM-er</button>
                    <button class="filter-pill" data-category="code-assistants" data-i18n="cat-code">Kodeassistenter</button>
                    <button class="filter-pill" data-category="builder-platform">Builder & API</button>
                    <button class="filter-pill" data-category="image-video" data-i18n="cat-image">Bilde & Video</button>
                    <button class="filter-pill" data-category="audio-voice" data-i18n="cat-audio">Lyd & Stemme</button>
                    <button class="filter-pill" data-category="agents" data-i18n="cat-agents">Agenter</button>
                </div>
            </section>

{categories_html}

            <!-- CTA Section -->
            <section class="cta-section">
                <h3 data-i18n="cta-title">Vil du bruke AI mer effektivt i teamet ditt?</h3>
                <p data-i18n="cta-text">FYRK hjelper bedrifter å velge riktige verktøy og bygge AI-drevne arbeidsflyter.</p>
                <a href="mailto:hei@fyrk.no?subject=FYRK%20AI%20Radar" class="cta-button">
                    <span data-i18n="cta-button">Kontakt oss</span>
                    <span>→</span>
                </a>
            </section>
            </div>

            <!-- Kapabiliteter Tab Content -->
            <div class="tab-content hidden" id="tab-kapabiliteter" role="tabpanel" aria-labelledby="tab-btn-kapabiliteter">
                <!-- Capabilities Matrix -->
                <section class="capabilities-section" id="capabilities-section">
                    <div class="capabilities-header">
                        <div class="capabilities-title-group">
                            <h2 class="capabilities-title" data-i18n="capabilities-title">Kapabiliteter</h2>
                            <p class="capabilities-subtitle" data-i18n="capabilities-subtitle">Hva kan hver modell?</p>
                        </div>
                        <div class="capabilities-legend">
                            <span class="legend-item">
                                <span>⭐</span>
                                <span data-i18n="legend-best">Best</span>
                            </span>
                            <span class="legend-item">
                                <span>✓</span>
                                <span data-i18n="legend-yes">Ja</span>
                            </span>
                            <span class="legend-item">
                                <span>✗</span>
                                <span data-i18n="legend-no">Nei</span>
                            </span>
                        </div>
                    </div>
                    <div class="capabilities-content">
                        <table class="capabilities-table">
                            <thead>
                                <tr>
                                    <th></th>
                                    <th data-tool-index="0">Claude</th>
                                    <th data-tool-index="1">GPT-4o</th>
                                    <th data-tool-index="2">Gemini</th>
                                    <th data-tool-index="3">Llama</th>
                                    <th data-tool-index="4">DeepSeek</th>
                                    <th data-tool-index="5">Grok</th>
                                </tr>
                            </thead>
                            <tbody id="capabilities-tbody">
                                <!-- Populated by JavaScript -->
                            </tbody>
                        </table>
                    </div>
                    <!-- Mobile card view -->
                    <div class="capabilities-mobile" id="capabilities-mobile">
                        <div class="model-tabs" id="model-tabs">
                            <!-- Populated by JavaScript -->
                        </div>
                        <div id="model-cards">
                            <!-- Populated by JavaScript -->
                        </div>
                    </div>
                </section>

                <!-- About Section -->
                <section id="om" class="about-section">
                    <h2 data-i18n="about-title">Om AI Score</h2>
                    <p data-i18n="about-intro">Et eksperiment fra FYRK Lab hvor vi utforsker hvordan man kan sammenligne AI-modeller på en enkel måte.</p>
                    
                    <h3 data-i18n="about-sources-title">Datakilder</h3>
                    <ul>
                        <li data-i18n="source-1">Offentlig tilgjengelig informasjon</li>
                        <li data-i18n="source-2">Egne praktiske tester</li>
                        <li data-i18n="source-3">Inntrykk fra utviklere og AI-miljøer</li>
                        <li data-i18n="source-4">Vurderinger generert og validert med AI</li>
                    </ul>
                    
                    <p class="disclaimer" data-i18n="disclaimer">Ikke vitenskapelig – bruk som inspirasjon, ikke fasit.</p>
                </section>
            </div>
    </div>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <img src="assets/fyrk-monogram-secondary-cyan.svg" alt="FYRK" class="footer-logo-img" onerror="this.style.display='none';">
                    <span>© FYRK – AI Product Leadership</span>
                </div>
                <div class="footer-links">
                    <a href="https://fyrk.no">fyrk.no</a>
                    <a href="mailto:hei@fyrk.no?subject=FYRK%20AI%20Radar" data-i18n="contact">Kontakt</a>
                </div>
                <div class="footer-meta" data-i18n="last-updated">
                    Sist oppdatert: {last_updated}
                </div>
            </div>
        </div>
    </footer>

    <!-- Lightweight JS for filtering, sorting & i18n -->
    <script>
        // Translations
        const translations = {{
            no: {{
                'hero-badge': 'Oppdatert {period_display}',
                'hero-subtitle': 'En månedlig oversikt over hva som faktisk skjer i AI. Basert på signaler fra Hacker News, Github, X og sentimentanalyse.',
                'new-this-month': 'Ny denne måneden',
                'biggest-changes': 'Største endringer',
                'metrics-title': 'Slik leser du dataene',
                'metric-buzz': 'Hvor mye modellen/verktøyet diskuteres (0–100)',
                'metric-sentiment': 'Hvor positivt/negativt det omtales i communityet',
                'metric-utility': 'Opplevd praktisk nytteverdi',
                'metric-price': 'Opplevd kost/nytte (lavere = bedre verdi)',
                'label-utility': 'Nytte',
                'label-price': 'Pris',
                'filter-label': 'Filtrer etter kategori:',
                'filter-all': 'Alle',
                'cat-core-llm': 'Kjerne-LLM-er',
                'cat-code': 'Kodeassistenter',
                'cat-image': 'Bilde & Video',
                'cat-audio': 'Lyd & Stemme',
                'cat-agents': 'Agenter & Automatisering',
                'models': 'modeller',
                'tools': 'verktøy',
                'platforms': 'plattformer',
                'cta-title': 'Vil du bruke AI mer effektivt i teamet ditt?',
                'cta-text': 'FYRK hjelper bedrifter å velge riktige verktøy og bygge AI-drevne arbeidsflyter.',
                'cta-button': 'Kontakt oss',
                'contact': 'Kontakt',
                'last-updated': 'Sist oppdatert: {last_updated}',
                'show-all': 'Vis alle',
                'show-fewer': 'Vis færre',
                'tab-scores': 'Scores',
                'tab-capabilities': 'Kapabiliteter',
                'lab-badge': '🧪 FYRK Lab',
                'lab-text': 'Et eksperiment – ikke en benchmark.',
                'les-mer': 'Les mer',
                'close': 'Lukk',
                'capabilities-title': 'Kapabiliteter',
                'capabilities-subtitle': 'Hva kan hver modell?',
                'legend-best': 'Best',
                'legend-yes': 'Ja',
                'legend-no': 'Nei',
                'cap-header-cognitive': 'Kognitiv',
                'cap-koding': 'Koding',
                'cap-resonnering': 'Resonnering',
                'cap-norsk-short': 'Norsk',
                'cap-header-visual': 'Visuell',
                'cap-bildegenerering-short': 'Bildegenerering',
                'cap-header-audio': 'Audio',
                'cap-stemme-short': 'Stemme',
                'cap-header-system': 'System',
                'cap-websok': 'Websøk',
                'cap-dokument-short': 'Dokument',
                'cap-api-short': 'API',
                'cap-computer-use-short': 'Computer Use',
                'about-title': 'Om AI Score',
                'about-intro': 'Et eksperiment fra FYRK Lab hvor vi utforsker hvordan man kan sammenligne AI-modeller på en enkel måte.',
                'about-sources-title': 'Datakilder',
                'source-1': 'Offentlig tilgjengelig informasjon',
                'source-2': 'Egne praktiske tester',
                'source-3': 'Inntrykk fra utviklere og AI-miljøer',
                'source-4': 'Vurderinger generert og validert med AI',
                'disclaimer': 'Ikke vitenskapelig – bruk som inspirasjon, ikke fasit.'
            }},
            sv: {{
                'hero-badge': 'Uppdaterad {period_display}',
                'hero-subtitle': 'En månadsvis översikt över vad som faktiskt händer inom AI. Baserat på signaler från Hacker News, Github, X och sentimentanalys.',
                'new-this-month': 'Nytt denna månad',
                'biggest-changes': 'Största förändringarna',
                'metrics-title': 'Så här läser du datan',
                'metric-buzz': 'Hur mycket modellen/verktyget diskuteras (0–100)',
                'metric-sentiment': 'Hur positivt/negativt det omtalas i communityt',
                'metric-utility': 'Upplevd praktisk nytta',
                'metric-price': 'Upplevd kostnad/nytta (lägre = bättre värde)',
                'label-utility': 'Nytta',
                'label-price': 'Pris',
                'filter-label': 'Filtrera efter kategori:',
                'filter-all': 'Alla',
                'cat-core-llm': 'Kärn-LLM:er',
                'cat-code': 'Kodassistenter',
                'cat-image': 'Bild & Video',
                'cat-audio': 'Ljud & Röst',
                'cat-agents': 'Agenter & Automatisering',
                'models': 'modeller',
                'tools': 'verktyg',
                'platforms': 'plattformar',
                'cta-title': 'Vill du använda AI mer effektivt i ditt team?',
                'cta-text': 'FYRK hjälper företag att välja rätt verktyg och bygga AI-drivna arbetsflöden.',
                'cta-button': 'Kontakta oss',
                'contact': 'Kontakt',
                'last-updated': 'Senast uppdaterad: {last_updated}',
                'show-all': 'Visa alla',
                'show-fewer': 'Visa färre',
                'tab-scores': 'Scores',
                'tab-capabilities': 'Kapabiliteter',
                'lab-badge': '🧪 FYRK Lab',
                'lab-text': 'Ett experiment – inte en benchmark.',
                'les-mer': 'Läs mer',
                'close': 'Stäng',
                'capabilities-title': 'Kapabiliteter',
                'capabilities-subtitle': 'Vad kan varje modell?',
                'legend-best': 'Bäst',
                'legend-yes': 'Ja',
                'legend-no': 'Nej',
                'cap-header-cognitive': 'Kognitiv',
                'cap-koding': 'Kodning',
                'cap-resonnering': 'Resonemang',
                'cap-norsk-short': 'Norska',
                'cap-header-visual': 'Visuell',
                'cap-bildegenerering-short': 'Bildgenerering',
                'cap-header-audio': 'Audio',
                'cap-stemme-short': 'Röst',
                'cap-header-system': 'System',
                'cap-websok': 'Webbsök',
                'cap-dokument-short': 'Dokument',
                'cap-api-short': 'API',
                'cap-computer-use-short': 'Computer Use',
                'about-title': 'Om AI Score',
                'about-intro': 'Ett experiment från FYRK Lab där vi utforskar hur man kan jämföra AI-modeller på ett enkelt sätt.',
                'about-sources-title': 'Datakällor',
                'source-1': 'Offentligt tillgänglig information',
                'source-2': 'Egna praktiska tester',
                'source-3': 'Intryck från utvecklare och AI-miljöer',
                'source-4': 'Bedömningar genererade och validerade med AI',
                'disclaimer': 'Inte vetenskapligt – använd som inspiration, inte facit.'
            }},
            en: {{
                'hero-badge': 'Updated {period_display}',
                'hero-subtitle': 'A monthly overview of what\\'s actually happening in AI. Based on signals from Hacker News, Github, X, and sentiment analysis.',
                'new-this-month': 'New This Month',
                'biggest-changes': 'Biggest Movers',
                'metrics-title': 'How to Read the Data',
                'metric-buzz': 'How much the model/tool is being discussed (0–100)',
                'metric-sentiment': 'How positively/negatively it\\'s talked about in the community',
                'metric-utility': 'Perceived practical usefulness',
                'metric-price': 'Perceived cost/value (lower = better value)',
                'label-utility': 'Utility',
                'label-price': 'Price',
                'filter-label': 'Filter by category:',
                'filter-all': 'All',
                'cat-core-llm': 'Core LLMs',
                'cat-code': 'Code Assistants',
                'cat-image': 'Image & Video',
                'cat-audio': 'Audio & Voice',
                'cat-agents': 'Agents & Automation',
                'models': 'models',
                'tools': 'tools',
                'platforms': 'platforms',
                'cta-title': 'Want to use AI more effectively in your team?',
                'cta-text': 'FYRK helps companies choose the right tools and build AI-powered workflows.',
                'cta-button': 'Contact Us',
                'contact': 'Contact',
                'last-updated': 'Last updated: {last_updated}',
                'show-all': 'Show all',
                'show-fewer': 'Show fewer',
                'tab-scores': 'Scores',
                'tab-capabilities': 'Capabilities',
                'lab-badge': '🧪 FYRK Lab',
                'lab-text': 'An experiment – not a benchmark.',
                'les-mer': 'Read more',
                'close': 'Close',
                'capabilities-title': 'Capabilities',
                'capabilities-subtitle': 'What can each model do?',
                'legend-best': 'Best',
                'legend-yes': 'Yes',
                'legend-no': 'No',
                'cap-header-cognitive': 'Cognitive',
                'cap-koding': 'Coding',
                'cap-resonnering': 'Reasoning',
                'cap-norsk-short': 'Norwegian',
                'cap-header-visual': 'Visual',
                'cap-bildegenerering-short': 'Image Generation',
                'cap-header-audio': 'Audio',
                'cap-stemme-short': 'Voice',
                'cap-header-system': 'System',
                'cap-websok': 'Web Search',
                'cap-dokument-short': 'Documents',
                'cap-api-short': 'API',
                'cap-computer-use-short': 'Computer Use',
                'about-title': 'About AI Score',
                'about-intro': 'An experiment from FYRK Lab exploring how to compare AI models in a simple way.',
                'about-sources-title': 'Data Sources',
                'source-1': 'Publicly available information',
                'source-2': 'Own practical tests',
                'source-3': 'Impressions from developers and AI communities',
                'source-4': 'Assessments generated and validated with AI',
                'disclaimer': 'Not scientific – use as inspiration, not fact.'
            }}
        }};

        let currentLang = localStorage.getItem('fyrk-lang') || 'no';

        function setLanguage(lang) {{
            currentLang = lang;
            localStorage.setItem('fyrk-lang', lang);
            
            // Update active button
            document.querySelectorAll('.lang-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.dataset.lang === lang);
            }});
            
            // Translate all elements
            document.querySelectorAll('[data-i18n]').forEach(el => {{
                const key = el.dataset.i18n;
                if (translations[lang] && translations[lang][key]) {{
                    el.textContent = translations[lang][key];
                }}
            }});
            
            // Translate expand buttons based on their expanded state
            document.querySelectorAll('.expand-toggle, .expand-button').forEach(button => {{
                const expandText = button.querySelector('.expand-text');
                if (expandText) {{
                    const isExpanded = button.classList.contains('expanded');
                    const key = isExpanded ? 'show-fewer' : 'show-all';
                    if (translations[lang] && translations[lang][key]) {{
                        expandText.textContent = translations[lang][key];
                    }}
                }}
            }});
            
            // Re-render capabilities to update translations
            renderCapabilitiesTable();
            renderCapabilitiesMobile();
            
            // Update html lang attribute
            document.documentElement.lang = lang === 'no' ? 'no' : lang === 'sv' ? 'sv' : 'en';
        }}

        // Lab Banner Dismissal
        function dismissLabBanner() {{
            const banner = document.getElementById('lab-banner');
            if (banner) {{
                banner.classList.add('hidden');
                localStorage.setItem('fyrk-lab-banner-dismissed', 'true');
            }}
        }}

        // Tab Navigation
        function switchTab(tabName) {{
            // Update tabs
            document.querySelectorAll('.tab').forEach(tab => {{
                const isActive = tab.dataset.tab === tabName;
                tab.classList.toggle('active', isActive);
                tab.setAttribute('aria-selected', isActive);
            }});

            // Update content
            document.querySelectorAll('.tab-content').forEach(content => {{
                const isActive = content.id === 'tab-' + tabName;
                content.classList.toggle('hidden', !isActive);
                content.setAttribute('aria-hidden', !isActive);
            }});

            // Update URL hash
            window.location.hash = tabName;

            // Store in localStorage
            localStorage.setItem('fyrk-active-tab', tabName);
        }}

        // Capabilities Configuration
        const CAPABILITIES_CONFIG = {{
            tools: ['Claude', 'GPT-4o', 'Gemini', 'Llama', 'DeepSeek', 'Grok'],
            providerNames: {{
                'Claude': 'Anthropic',
                'GPT-4o': 'OpenAI',
                'Gemini': 'Google',
                'Llama': 'Meta',
                'DeepSeek': 'DeepSeek',
                'Grok': 'xAI'
            }},
            scoreSymbols: {{
                'best': '⭐',
                'yes': '✓',
                'no': '✗'
            }},
            categories: [
                {{ type: 'header', key: 'cap-header-cognitive' }},
                {{ key: 'cap-koding', shortKey: 'cap-koding', scores: ['yes', 'yes', 'best', 'yes', 'yes', 'yes'] }},
                {{ key: 'cap-resonnering', shortKey: 'cap-resonnering', scores: ['yes', 'yes', 'best', 'yes', 'yes', 'yes'] }},
                {{ key: 'cap-norsk', shortKey: 'cap-norsk-short', scores: ['yes', 'yes', 'yes', 'best', 'yes', 'no'] }},
                {{ type: 'header', key: 'cap-header-visual' }},
                {{ key: 'cap-bildegenerering', shortKey: 'cap-bildegenerering-short', scores: ['no', 'no', 'yes', 'yes', 'best', 'no'] }},
                {{ type: 'header', key: 'cap-header-audio' }},
                {{ key: 'cap-stemme', shortKey: 'cap-stemme-short', scores: ['yes', 'yes', 'no', 'best', 'yes', 'no'] }},
                {{ type: 'header', key: 'cap-header-system' }},
                {{ key: 'cap-websok', shortKey: 'cap-websok', scores: ['yes', 'yes', 'yes', 'yes', 'yes', 'no'] }},
                {{ key: 'cap-dokument', shortKey: 'cap-dokument-short', scores: ['yes', 'yes', 'yes', 'yes', 'best', 'no'] }},
                {{ key: 'cap-api', shortKey: 'cap-api-short', scores: ['yes', 'yes', 'yes', 'yes', 'yes', 'yes'] }},
                {{ key: 'cap-computer-use', shortKey: 'cap-computer-use-short', scores: ['yes', 'yes', 'best', 'yes', 'no', 'no'] }},
            ]
        }};

        // Capabilities Utilities
        const CapabilitiesUtils = {{
            getTranslation: (key) => {{
                return translations[currentLang] && translations[currentLang][key] || key;
            }},
            
            getCapabilityName: (category) => {{
                const nameKey = category.shortKey || category.key;
                return CapabilitiesUtils.getTranslation(nameKey);
            }},
            
            createScoreCell: (score) => {{
                const cell = document.createElement('td');
                const cellContent = document.createElement('div');
                cellContent.className = `capability-cell capability-${{score}}`;
                cellContent.textContent = CAPABILITIES_CONFIG.scoreSymbols[score] || '';
                cell.appendChild(cellContent);
                return cell;
            }},
            
            createCategoryHeader: (category) => {{
                const row = document.createElement('tr');
                row.className = 'category-header';
                const headerCell = document.createElement('td');
                headerCell.setAttribute('data-i18n', category.key);
                headerCell.setAttribute('colspan', CAPABILITIES_CONFIG.tools.length + 1);
                headerCell.textContent = CapabilitiesUtils.getTranslation(category.key);
                row.appendChild(headerCell);
                return row;
            }},
            
            createCapabilityRow: (category) => {{
                const row = document.createElement('tr');
                const nameCell = document.createElement('td');
                const nameKey = category.shortKey || category.key;
                nameCell.setAttribute('data-i18n', nameKey);
                nameCell.textContent = CapabilitiesUtils.getCapabilityName(category);
                row.appendChild(nameCell);
                
                category.scores.forEach(score => {{
                    row.appendChild(CapabilitiesUtils.createScoreCell(score));
                }});
                
                return row;
            }}
        }};

        // Render Capabilities Table
        function renderCapabilitiesTable() {{
            const tbody = document.getElementById('capabilities-tbody');
            if (!tbody) return;

            tbody.innerHTML = '';

            CAPABILITIES_CONFIG.categories.forEach(category => {{
                if (category.type === 'header') {{
                    tbody.appendChild(CapabilitiesUtils.createCategoryHeader(category));
                }} else {{
                    tbody.appendChild(CapabilitiesUtils.createCapabilityRow(category));
                }}
            }});
        }}

        function renderCapabilitiesMobile() {{
            // Mobile view can be implemented later if needed
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            // Initialize language
            setLanguage(currentLang);
            
            // Language switcher
            document.querySelectorAll('.lang-btn').forEach(btn => {{
                btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
            }});

            // Initialize tabs
            const hash = window.location.hash.slice(1);
            const savedTab = localStorage.getItem('fyrk-active-tab');
            const defaultTab = hash || savedTab || 'scores';
            switchTab(defaultTab);

            // Tab click handlers
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.addEventListener('click', function() {{
                    switchTab(this.dataset.tab);
                }});
            }});

            // Handle browser back/forward
            window.addEventListener('hashchange', function() {{
                const hash = window.location.hash.slice(1);
                if (hash === 'scores' || hash === 'kapabiliteter') {{
                    switchTab(hash);
                }}
            }});

            // Check if lab banner was dismissed
            if (localStorage.getItem('fyrk-lab-banner-dismissed') === 'true') {{
                const banner = document.getElementById('lab-banner');
                if (banner) banner.classList.add('hidden');
            }}

            // Render capabilities
            renderCapabilitiesTable();
            renderCapabilitiesMobile();

            // Category filtering
            const filterPills = document.querySelectorAll('.filter-pill');
            const categorySections = document.querySelectorAll('.category-section');

            filterPills.forEach(pill => {{
                pill.addEventListener('click', function() {{
                    const category = this.dataset.category;
                    
                    // Update active state
                    filterPills.forEach(p => p.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Show/hide categories
                    categorySections.forEach(section => {{
                        if (category === 'all' || section.dataset.category === category) {{
                            section.classList.remove('hidden');
                        }} else {{
                            section.classList.add('hidden');
                        }}
                    }});
                }});
            }});

            // Column sorting
            document.querySelectorAll('.rankings-header span[data-sort]').forEach(header => {{
                header.addEventListener('click', function() {{
                    const sortKey = this.dataset.sort;
                    const table = this.closest('.rankings-table');
                    const expandSection = table.querySelector('.expand-section');
                    const rows = Array.from(table.querySelectorAll('.ranking-row'));
                    const isAsc = this.classList.contains('sort-asc');
                    
                    // Reset all sort indicators in this table
                    table.querySelectorAll('.rankings-header span[data-sort]').forEach(h => {{
                        h.classList.remove('sort-asc', 'sort-desc');
                    }});
                    
                    // Set new sort direction
                    this.classList.add(isAsc ? 'sort-desc' : 'sort-asc');
                    
                    // Sort rows
                    rows.sort((a, b) => {{
                        let valA, valB;
                        
                        if (sortKey === 'name') {{
                            valA = a.querySelector('.item-name').textContent.toLowerCase();
                            valB = b.querySelector('.item-name').textContent.toLowerCase();
                            return isAsc ? valB.localeCompare(valA) : valA.localeCompare(valB);
                        }} else {{
                            valA = parseInt(a.dataset[sortKey]) || 0;
                            valB = parseInt(b.dataset[sortKey]) || 0;
                            return isAsc ? valA - valB : valB - valA;
                        }}
                    }});
                    
                    // Re-append rows and update rank badges
                    rows.forEach((row, index) => {{
                        if (expandSection) {{
                            table.insertBefore(row, expandSection);
                        }} else {{
                            table.appendChild(row);
                        }}
                        const badge = row.querySelector('.rank-badge');
                        badge.textContent = index + 1;
                        badge.className = 'rank-badge';
                        if (index === 0) badge.classList.add('rank-1');
                        else if (index === 1) badge.classList.add('rank-2');
                        else if (index === 2) badge.classList.add('rank-3');
                        else badge.classList.add('rank-default');
                    }});
                }});
            }});
        }});
    </script>
    
    <script>
        // Expand/collapse functionality - defined globally
        function toggleExpand(categoryId) {{
            try {{
                // Find button by data-category attribute
                const button = document.querySelector('.expand-button[data-category="' + categoryId + '"]');
                if (!button) {{
                    console.error('Expand button not found for category:', categoryId);
                    return;
                }}
                
                // Find the table container (parent of expand-section)
                const expandSection = button.closest('.expand-section');
                if (!expandSection) {{
                    console.error('Expand section not found');
                    return;
                }}
                
                const table = expandSection.parentElement;
                if (!table || !table.classList.contains('rankings-table')) {{
                    console.error('Table not found');
                    return;
                }}
                
                const hiddenRows = table.querySelectorAll('.ranking-row.hidden-row');
                const expandText = button.querySelector('.expand-text');
                
                if (button.classList.contains('expanded')) {{
                    // Collapse
                    hiddenRows.forEach(row => {{
                        row.classList.remove('expanded');
                    }});
                    button.classList.remove('expanded');
                    if (expandText) {{
                        // Use translation - button is now collapsed, so show "show-all"
                        const key = 'show-all';
                        const lang = localStorage.getItem('fyrk-lang') || 'no';
                        if (translations[lang] && translations[lang][key]) {{
                            expandText.textContent = translations[lang][key];
                        }} else {{
                            expandText.textContent = 'Vis alle';
                        }}
                    }}
                }} else {{
                    // Expand
                    hiddenRows.forEach(row => {{
                        row.classList.add('expanded');
                    }});
                    button.classList.add('expanded');
                    if (expandText) {{
                        // Use translation - button is now expanded, so show "show-fewer"
                        const key = 'show-fewer';
                        const lang = localStorage.getItem('fyrk-lang') || 'no';
                        if (translations[lang] && translations[lang][key]) {{
                            expandText.textContent = translations[lang][key];
                        }} else {{
                            expandText.textContent = 'Vis færre';
                        }}
                    }}
                }}
            }} catch (error) {{
                console.error('Error in toggleExpand:', error);
            }}
        }}
        
        // Make function available globally
        window.toggleExpand = toggleExpand;
    </script>
</body>
</html>"""

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
