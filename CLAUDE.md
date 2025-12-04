# CLAUDE.md - AI Assistant Guide

**Last Updated**: 2025-12-04
**Repository**: AI News Agent (FYRK AI Radar)
**Live Site**: https://ai-radar.fyrk.no

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Key Modules](#key-modules)
- [Development Workflow](#development-workflow)
- [Coding Conventions](#coding-conventions)
- [Testing Strategy](#testing-strategy)
- [Deployment](#deployment)
- [Common Tasks](#common-tasks)
- [Important Patterns](#important-patterns)

---

## Project Overview

**AI News Agent** is an automated system that monitors and ranks AI tools based on public discourse across multiple platforms.

### Purpose
- Collects mentions of AI tools from Hacker News, GitHub, Reddit, and Twitter
- Analyzes data using Claude API for intelligent ranking
- Generates rankings in multiple categories
- Tracks trends month-over-month
- Publishes results as HTML to Cloudflare Pages

### Language
- Primary language: **Norwegian (Bokmål)** for user-facing content
- Code comments: Mix of English and Norwegian
- Documentation: Mix of English and Norwegian

### Tech Stack
- **Python 3.11+** with async/await
- **httpx** for async HTTP requests
- **anthropic** SDK for Claude API
- **pytest** for testing
- **GitHub Actions** for automation
- **Cloudflare Pages** for hosting

---

## Architecture

### High-Level Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│   main.py   │────▶│  collectors/ │────▶│  analyzer   │────▶│  output/ │
│ (orchestr.) │     │ (HN, GitHub, │     │  (Claude)   │     │  (JSON)  │
│             │     │  Reddit, X)  │     │             │     │          │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
                                                                   │
                                                                   ▼
                                                            ┌──────────┐
                                                            │generator/│
                                                            │  (HTML)  │
                                                            └──────────┘
                                                                   │
                                                                   ▼
                                                            ┌──────────┐
                                                            │  docs/   │
                                                            │ (Deploy) │
                                                            └──────────┘
```

### Data Flow

1. **Collection Phase** (`collectors/`)
   - Fetch data from 4 sources (HN, GitHub, Reddit, Twitter)
   - Filter for AI-relevant content using keywords
   - Normalize to common schema
   - Save raw data to `output/raw_posts_YYYY-MM.json`

2. **Analysis Phase** (`analyzer/`)
   - Send aggregated data to Claude API
   - Extract structured rankings per category
   - Validate JSON output
   - Save to `output/rankings_YYYY-MM.json`

3. **Trend Analysis** (`analyzer/trend_analyzer.py`)
   - Compare current rankings with previous month
   - Calculate rank changes
   - Identify new/rising/falling/stable tools

4. **Generation Phase** (`generator/`)
   - Load rankings JSON
   - Generate HTML with embedded data
   - Output to `docs/index.html`

5. **Deployment**
   - GitHub Actions commits results
   - Cloudflare Pages auto-deploys from `docs/`

---

## Directory Structure

```
ai-news-agent/
├── src/ai_news_agent/              # Main Python package
│   ├── main.py                     # Primary entry point (orchestrates pipeline)
│   ├── config.py                   # Global config (keywords, categories, constants)
│   │
│   ├── collectors/                 # Data collection from external sources
│   │   ├── hackernews.py           # HN Firebase API + Algolia
│   │   ├── github.py               # GitHub trending repos
│   │   ├── reddit.py               # Reddit JSON API (no auth)
│   │   └── twitter.py              # Twitter/X API (requires bearer token)
│   │
│   ├── analyzer/                   # Claude-powered analysis
│   │   ├── analyzer.py             # Main Claude API integration
│   │   └── trend_analyzer.py       # Month-over-month comparison
│   │
│   ├── generator/                  # HTML output generation
│   │   ├── generate_html.py        # Main HTML generator (2531 LOC)
│   │   └── templates/              # Embedded templates
│   │
│   ├── utils/                      # Shared utilities
│   │   ├── __init__.py             # Helper functions (save/load/date)
│   │   └── link_checker.py         # URL validation
│   │
│   ├── coding_assistants/          # Separate scoring system for coding tools
│   │   ├── main.py                 # Coding assistant scorer
│   │   ├── config.py               # Tool definitions
│   │   ├── fetchers/               # Data fetchers (HN, GitHub, Reddit)
│   │   └── analyzers/              # Scoring algorithms (sentiment, buzz)
│   │
│   └── capability_monitor/         # Monthly AI model capability tracking
│       ├── main.py                 # Entry point
│       ├── config.py               # Model and capability definitions
│       ├── fetcher.py              # Search for latest model info
│       ├── analyzer.py             # Determine best-in-category
│       └── table_generator.py      # Generate markdown table
│
├── data/                           # Static data files
│   ├── tool_links.json             # AI tool URLs (manually curated)
│   ├── coding_assistants/          # Coding tool configs (features, pricing)
│   └── capability_monitor/         # Capability tracking data
│       ├── current_table.md        # Current capability comparison table
│       └── history/                # Historical capability snapshots
│
├── output/                         # Generated JSON outputs
│   ├── rankings_YYYY-MM.json       # Monthly tool rankings
│   ├── raw_posts_YYYY-MM.json      # Raw collected data
│   └── capability_report.md        # Monthly capability update report
│
├── docs/                           # Public website (Cloudflare Pages)
│   ├── index.html                  # Main rankings page (auto-generated)
│   └── assets/                     # Logos and images
│
├── tests/                          # Test suite
│   ├── conftest.py                 # Shared pytest fixtures
│   ├── unit/                       # Unit tests
│   └── README.md                   # Testing documentation
│
├── scripts/                        # Development shell scripts
│   ├── test_quick.sh               # Quick data collection test
│   ├── test_full.sh                # Full pipeline test
│   └── serve_local.sh              # Local web server
│
├── .github/workflows/              # GitHub Actions automation
│   ├── daily.yml                   # Daily data collection & analysis
│   ├── monthly-capability-update.yml  # Monthly capability tracking
│   └── check_links.yml             # Link validation
│
├── main.py                         # Root entry point (imports from src/)
├── generate_html.py                # HTML generator entry point
├── check_links.py                  # Link checker entry point
├── score_coding_assistants.py      # Coding assistant scorer entry point
├── update_capabilities.py          # Capability monitor entry point
│
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Package configuration
├── pytest.ini                      # Test configuration
├── .cursorrules                    # Cursor IDE rules (project context)
│
├── README.md                       # Main documentation
├── DEVELOPMENT.md                  # Development workflow guide
├── QUICKSTART.md                   # Quick start guide
└── CLAUDE.md                       # This file (AI assistant guide)
```

---

## Key Modules

### 1. Main Pipeline (`src/ai_news_agent/main.py`)

**Responsibilities:**
- Orchestrates the entire data collection and analysis pipeline
- Handles CLI arguments (`--collect-only`, `--analyze-only`, `--days`)
- Manages error handling and fallbacks
- Coordinates all phases of execution

**Key Functions:**
- `run_collection(days)` - Runs all collectors in sequence
- `run_analysis(posts, period)` - Analyzes with Claude
- `print_summary(rankings)` - Terminal output
- `main()` - Entry point with argparse

**Usage Patterns:**
```python
# Full pipeline
await run_collection(days=90)
rankings = run_analysis(posts, period="2025-12")
rankings = add_trends_to_rankings(rankings)
save_output(rankings, "rankings_2025-12.json")
```

### 2. Collectors (`src/ai_news_agent/collectors/`)

**Purpose:** Fetch data from external sources, normalize to common schema

**Common Schema:**
```python
{
    "title": str,           # Post/repo title
    "url": str,             # Link to source
    "points": int,          # Score/stars/upvotes
    "num_comments": int,    # Comment count
    "timestamp": str,       # ISO 8601 timestamp
    "source": str,          # "hackernews"|"github"|"reddit"|"twitter"
    "raw_data": dict        # Original API response
}
```

**Collectors:**

- **`hackernews.py`**
  - Uses Firebase API + Algolia search
  - Filters by `AI_KEYWORDS` from config
  - Min threshold: `MIN_HN_POINTS` (default: 10)
  - Returns: List of normalized posts

- **`github.py`**
  - Fetches trending repositories
  - Filters by AI-related topics/keywords
  - Uses optional `GITHUB_TOKEN` for higher rate limits
  - Returns: List of normalized repos

- **`reddit.py`**
  - Uses public JSON API (no auth required)
  - Searches multiple AI-related subreddits
  - Returns: List of normalized posts

- **`twitter.py`**
  - Requires `TWITTER_BEARER_TOKEN`
  - Searches for AI-related tweets with high engagement
  - Returns: List of normalized tweets

**Important:** All collectors use **async/await** with `httpx.AsyncClient`

### 3. Analyzer (`src/ai_news_agent/analyzer/`)

**`analyzer.py` - Claude Integration**

**Responsibilities:**
- Sends collected data to Claude API
- Extracts structured rankings in JSON format
- Validates output against schema
- Handles JSON parsing errors (markdown wrapping, truncation)

**Key Functions:**
- `create_analysis_prompt(posts, period)` - Builds Claude prompt
- `analyze_with_claude(posts, period)` - Main API call
- `extract_json_from_text(text)` - Robust JSON extraction
- `validate_rankings(rankings)` - Schema validation

**Prompt Strategy:**
- Summarizes top 200 posts by points
- Provides category definitions from `config.CATEGORIES`
- Requests structured JSON output
- Asks for top 10 per category with medals (gold/silver/bronze for top 3)
- Requests "new & noteworthy" section

**Output Schema:**
```python
{
    "period": "YYYY-MM",
    "generated_at": "ISO timestamp",
    "data_source": "hackernews,github,reddit,twitter",
    "total_posts_analyzed": int,
    "categories": [
        {
            "name": str,
            "slug": str,
            "top3": [  # Actually top 10, but top 3 get medals
                {
                    "rank": int,
                    "medal": "gold"|"silver"|"bronze"|null,
                    "name": str,
                    "provider": str,
                    "short_reason": str,
                    "tags": [str],
                    "scores": {
                        "buzz_momentum": 0-5,
                        "sentiment": 0-5,
                        "utility_for_knowledge_work": 0-5,
                        "price_performance": 0-5
                    },
                    "evidence": [str]
                }
            ]
        }
    ],
    "new_and_noteworthy": [...]
}
```

**`trend_analyzer.py` - Month-over-Month Comparison**

**Responsibilities:**
- Loads previous month's rankings
- Compares current vs previous ranks
- Adds trend metadata to each tool

**Trend Schema:**
```python
{
    "trend": {
        "status": "new"|"rising"|"falling"|"stable",
        "previous_rank": int|null,
        "rank_change": int  # Positive = moved up
    }
}
```

### 4. Generator (`src/ai_news_agent/generator/generate_html.py`)

**Responsibilities:**
- Loads rankings JSON
- Generates standalone HTML file
- Embeds all CSS, JavaScript inline
- Creates responsive, mobile-friendly UI
- Handles dummy data mode for testing

**Key Features:**
- Medal system (🥇🥈🥉)
- Trend indicators (✨📈📉➡️)
- Category tabs
- Responsive grid layout
- Dark/light mode toggle
- Provider logos

**Usage:**
```bash
python generate_html.py              # Use latest rankings
python generate_html.py --dummy      # Generate with test data
```

### 5. Coding Assistants (`src/ai_news_agent/coding_assistants/`)

**Purpose:** Separate scoring system specifically for coding assistant tools

**Differs from main pipeline:**
- Uses percentile-based scoring algorithm
- Includes VADER sentiment analysis
- Manual feature/pricing scores from JSON files
- Outputs separate rankings

**Scoring Formula:**
```
FINAL = (BUZZ × 0.30) + (SENTIMENT × 0.25) + (UTILITY × 0.25) + (PRICE × 0.20)
```

**Components:**
- Buzz: GitHub stars, star growth, mentions
- Sentiment: HN/Reddit comment analysis
- Utility: Manual scoring from `data/coding_assistants/features.json`
- Price: Manual scoring from `data/coding_assistants/pricing.json`

### 6. Capability Monitor (`src/ai_news_agent/capability_monitor/`)

**Purpose:** Monthly tracking of AI model capabilities across providers

**Responsibilities:**
- Searches for latest model versions
- Determines best-in-category for each capability
- Generates comparison table
- Tracks changes month-over-month

**Models Tracked:**
- Claude Opus 4.5 (Anthropic)
- GPT-5 (OpenAI)
- Gemini 2.5/3 Pro (Google)
- Grok 3/4 (xAI)
- Llama 4 (Meta)
- DeepSeek V3/R1

**Output:** Markdown table with ✔︎/✗/~/⭐ symbols

---

## Development Workflow

### Branch Strategy

**Two-branch model:**
- **`main`** - Production (auto-deploys to ai-radar.fyrk.no)
- **`dev`** - Staging (preview deployment)

**Important:** All development should happen on feature branches or `dev`, then merge to `main` only after testing.

### Git Workflow

```bash
# 1. Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/my-feature

# 2. Make changes and test locally
python main.py --days 30
pytest

# 3. Merge to dev for staging
git checkout dev
git merge feature/my-feature
git push origin dev

# 4. Test on preview deployment (check Cloudflare Pages)

# 5. Merge to main when ready
git checkout main
git merge dev
git push origin main
```

### Local Development Setup

```bash
# 1. Clone and install
git clone https://github.com/carlfrankalbert/ai-news-agent.git
cd ai-news-agent
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# 2. Set up environment
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."  # Optional, for higher rate limits

# 3. Test collection (free, no API calls)
python main.py --collect-only --days 7

# 4. Test analysis (uses Claude API)
python main.py --days 7

# 5. Generate HTML
python generate_html.py

# 6. Run tests
pytest

# 7. Serve locally
python -m http.server 8000 --directory docs
# Visit http://localhost:8000
```

### Environment Variables

**Required:**
- `ANTHROPIC_API_KEY` - Claude API key (required for analysis)

**Optional:**
- `GITHUB_TOKEN` - GitHub personal access token (increases rate limits)
- `TWITTER_BEARER_TOKEN` - Twitter API bearer token (enables Twitter collection)

---

## Coding Conventions

### Python Style

1. **Type Hints:** Use where helpful, but not mandatory
   ```python
   async def collect_ai_mentions(days_back: int = 90) -> list[dict]:
   ```

2. **Async/Await:** All I/O operations use async
   ```python
   async with httpx.AsyncClient() as client:
       response = await client.get(url)
   ```

3. **Error Handling:** Graceful degradation
   ```python
   try:
       posts = await collect_ai_mentions()
   except Exception as e:
       print(f"⚠️  Feil ved innsamling: {e}")
       posts = []  # Continue with empty list
   ```

4. **Docstrings:** Norwegian or English, focus on purpose
   ```python
   """
   Samler AI-relaterte posts fra Hacker News.

   Returns:
       List of normalized posts with common schema
   """
   ```

5. **Emoji in Output:** Use emoji in user-facing terminal output
   ```python
   print(f"✅ Fant {len(posts)} AI-relaterte posts")
   print(f"⚠️  Advarsel: ingen data funnet")
   ```

### Configuration Management

**All configuration in `config.py`:**
- API endpoints
- Keywords for filtering
- Category definitions
- Constants (lookback days, min scores, etc.)

**Do NOT hardcode:**
- API keys (use environment variables)
- Magic numbers (use constants from config)
- Category definitions (use `CATEGORIES` from config)

### Naming Conventions

- **Functions:** `snake_case`, verb phrases
  - `collect_ai_mentions()`, `analyze_with_claude()`, `save_output()`

- **Variables:** `snake_case`, descriptive
  - `hn_posts`, `github_repos`, `all_posts`

- **Constants:** `UPPER_SNAKE_CASE`
  - `LOOKBACK_DAYS`, `MIN_HN_POINTS`, `AI_KEYWORDS`

- **Files:** `snake_case.py`
  - `trend_analyzer.py`, `generate_html.py`

### Data Normalization

**Always normalize external data to common schema immediately:**

```python
# Good: Normalize as soon as data is fetched
async def collect_hackernews():
    stories = await fetch_stories()
    return [normalize_hn_post(s) for s in stories]

def normalize_hn_post(story: dict) -> dict:
    return {
        "title": story.get("title", ""),
        "url": story.get("url", f"https://news.ycombinator.com/item?id={story['id']}"),
        "points": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "timestamp": datetime.fromtimestamp(story.get("time", 0)).isoformat(),
        "source": "hackernews",
        "raw_data": story
    }
```

### Output File Naming

**Consistent naming pattern:**
- Raw data: `raw_posts_YYYY-MM.json`
- Rankings: `rankings_YYYY-MM.json`
- HTML: `index.html` (always overwrites)
- Capability reports: `capability_report.md`

**Period string format:** `YYYY-MM` (e.g., `2025-12`)

---

## Testing Strategy

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests (fast, no I/O)
│   ├── test_scoring.py
│   ├── test_data_normalization.py
│   └── test_claude_json_parsing.py
└── integration/             # Integration tests (slower, may use I/O)
    └── (future)
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src/ai_news_agent --cov-report=html

# Specific test file
pytest tests/unit/test_scoring.py

# Verbose output
pytest -v

# Show print statements
pytest -s
```

### Test Coverage Goals

**Target:** 80%+ coverage for critical modules
- `collectors/` (data normalization)
- `analyzer/` (Claude integration, JSON parsing)
- `utils/` (helper functions)

### Writing Tests

**Use fixtures from `conftest.py`:**
```python
def test_normalize_post(sample_hn_story):
    result = normalize_hn_post(sample_hn_story)
    assert result["source"] == "hackernews"
    assert "title" in result
```

**Test async functions:**
```python
import pytest

@pytest.mark.asyncio
async def test_collect_mentions():
    posts = await collect_ai_mentions(days_back=7)
    assert isinstance(posts, list)
```

**Mock external API calls:**
```python
from unittest.mock import patch

@patch('httpx.AsyncClient.get')
async def test_with_mock(mock_get):
    mock_get.return_value.json.return_value = {"id": 123}
    # Test code here
```

### Pre-commit Testing

**Before pushing to `dev`:**
```bash
pytest                           # All tests pass
python main.py --collect-only    # Collection works
python main.py --days 7          # Analysis works (small dataset)
python generate_html.py --dummy  # HTML generation works
```

---

## Deployment

### Automatic Deployment

**Three GitHub Actions workflows:**

#### 1. Daily AI News Scan (`.github/workflows/daily.yml`)

**Triggers:**
- Scheduled: 06:00 UTC daily (on `main` only)
- Manual: Via workflow_dispatch
- Push: On push to `main` or `dev`

**Steps:**
1. Checkout code
2. Install dependencies
3. Run `python main.py --days 30`
4. Run `python generate_html.py`
5. Commit results to current branch
6. Push to GitHub

**Output:**
- `output/rankings_YYYY-MM.json`
- `output/raw_posts_YYYY-MM.json`
- `docs/index.html`

**Branch Behavior:**
- Commits to `dev` are tagged `[DEV] Daily scan YYYY-MM-DD`
- Commits to `main` are tagged `Daily scan YYYY-MM-DD`

#### 2. Monthly Capability Update (`.github/workflows/monthly-capability-update.yml`)

**Triggers:**
- Scheduled: 09:00 UTC on 1st of month (on `main` only)
- Manual: Via workflow_dispatch
- Push: On push to `main` or `dev`

**Steps:**
1. Run capability monitor
2. Generate capability report
3. Commit results

**Output:**
- `data/capability_monitor/current_table.md`
- `output/capability_report.md`

#### 3. Check Provider Links (`.github/workflows/check_links.yml`)

**Triggers:**
- Scheduled: 02:00 UTC daily (on `main` only)
- Manual: Via workflow_dispatch
- Push: On push to `main` or `dev`

**Steps:**
1. Validate all URLs in `data/tool_links.json`
2. Generate report
3. Create GitHub issue if broken links found (on `main` only)

### Cloudflare Pages Deployment

**Automatic deployment:**
- Source: `docs/` directory
- Production: `main` branch → https://ai-radar.fyrk.no
- Preview: `dev` branch → preview URL (e.g., `dev-abc123.ai-radar.pages.dev`)

**Build Configuration:**
- Build command: None (static files)
- Output directory: `docs`
- Node version: N/A

**Finding Preview URLs:**
1. Go to Cloudflare Pages dashboard
2. Select project
3. Find latest `dev` deployment
4. Copy preview URL

### Manual Workflow Triggers

**From GitHub Actions tab:**
1. Navigate to repository → Actions
2. Select workflow (e.g., "Daily AI News Scan")
3. Click "Run workflow"
4. Select branch (`main` or `dev`)
5. Click "Run workflow" button

### Rollback Strategy

**If production breaks:**

```bash
# Quick rollback to previous commit
git checkout main
git revert HEAD
git push origin main

# Or revert to specific commit
git checkout main
git revert <commit-hash>
git push origin main
```

**Cloudflare Pages will automatically redeploy the reverted version.**

---

## Common Tasks

### Task 1: Add New AI Keyword

**File:** `src/ai_news_agent/config.py`

```python
AI_KEYWORDS = [
    # ... existing keywords ...
    "new-ai-tool",  # Add here
]
```

**Test:**
```bash
python main.py --collect-only --days 7
# Check if new keyword matches posts
```

### Task 2: Add New Category

**File:** `src/ai_news_agent/config.py`

```python
CATEGORIES = [
    # ... existing categories ...
    {
        "name": "New Category Name",
        "slug": "new-category",
        "description": "Description for Claude",
        "examples": ["Tool1", "Tool2", "Tool3"]
    }
]
```

**Note:** Claude will automatically rank tools in new category

**Test:**
```bash
python main.py --days 7
# Check output/rankings_YYYY-MM.json for new category
```

### Task 3: Update Tool Links

**File:** `data/tool_links.json`

```json
{
  "ToolName": "https://example.com"
}
```

**Validate:**
```bash
python check_links.py
```

### Task 4: Adjust Lookback Period

**File:** `src/ai_news_agent/config.py`

```python
LOOKBACK_DAYS = 90  # Change to desired days
```

**Or via CLI:**
```bash
python main.py --days 30  # Override without editing config
```

### Task 5: Debug Claude Output

**If Claude returns invalid JSON:**

1. Check `analyzer/analyzer.py` → `extract_json_from_text()`
2. Look for parsing errors in terminal output
3. Inspect raw Claude response (add debug print)
4. Validate against schema with `validate_rankings()`

**Common issues:**
- Markdown wrapping (`` ```json ... ``` ``)
- Truncated responses (incomplete JSON)
- Trailing commas
- Missing required fields

### Task 6: Test HTML Generation

**With real data:**
```bash
python generate_html.py
open docs/index.html  # macOS
# or
python -m http.server 8000 --directory docs
```

**With dummy data:**
```bash
python generate_html.py --dummy
open docs/index.html
```

### Task 7: Add New Collector

**Steps:**
1. Create `src/ai_news_agent/collectors/new_source.py`
2. Implement `async def collect_new_source(days_back: int) -> list[dict]`
3. Return normalized schema (same as other collectors)
4. Import in `src/ai_news_agent/main.py`
5. Add to `run_collection()` function
6. Update `data_source` field in analyzer prompt

**Template:**
```python
async def collect_new_source(days_back: int = 90) -> list[dict]:
    """Collect from new source."""
    async with httpx.AsyncClient() as client:
        # Fetch data
        response = await client.get(url)
        data = response.json()

        # Normalize
        posts = [
            {
                "title": item["title"],
                "url": item["link"],
                "points": item["score"],
                "num_comments": item["comments"],
                "timestamp": item["created_at"],
                "source": "new_source",
                "raw_data": item
            }
            for item in data
        ]

        return posts
```

---

## Important Patterns

### Pattern 1: Error Handling in Collectors

**Always gracefully degrade:**
```python
try:
    posts = await collect_hackernews()
    print(f"✅ Fant {len(posts)} posts")
except Exception as e:
    print(f"⚠️  Feil: {e}")
    posts = []  # Don't crash, continue with empty

all_posts.extend(posts)  # Safe even if empty
```

### Pattern 2: Rate Limiting

**Use delays between requests:**
```python
import asyncio

for item in items:
    await fetch_item(item)
    await asyncio.sleep(0.5)  # 500ms delay
```

### Pattern 3: Date/Time Handling

**Always use ISO 8601 format:**
```python
from datetime import datetime

# Generate period string
def get_period_string() -> str:
    return datetime.now().strftime("%Y-%m")  # "2025-12"

# Convert UNIX timestamp
timestamp = datetime.fromtimestamp(unix_time).isoformat()
```

### Pattern 4: JSON Validation

**Validate before using:**
```python
def validate_rankings(rankings: dict) -> tuple[bool, list[str]]:
    issues = []

    if "period" not in rankings:
        issues.append("Missing 'period' field")

    if "categories" not in rankings:
        issues.append("Missing 'categories' field")

    for cat in rankings.get("categories", []):
        if "top3" not in cat:
            issues.append(f"Category {cat.get('name')} missing 'top3'")

    return (len(issues) == 0, issues)
```

### Pattern 5: File I/O

**Use pathlib:**
```python
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

file_path = output_dir / f"rankings_{period}.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

### Pattern 6: Async Context Managers

**Reuse client connections:**
```python
async with httpx.AsyncClient() as client:
    # Multiple requests with same client
    r1 = await client.get(url1)
    r2 = await client.get(url2)
    # Client closes automatically
```

### Pattern 7: Configuration Access

**Import from config, don't hardcode:**
```python
from .config import LOOKBACK_DAYS, AI_KEYWORDS, MIN_HN_POINTS

# Good
if score >= MIN_HN_POINTS:
    posts.append(post)

# Bad
if score >= 10:  # Hardcoded
    posts.append(post)
```

### Pattern 8: Logging to User

**Use emoji and Norwegian for user output:**
```python
print(f"📡 Samler data fra Hacker News...")
print(f"✅ Fant {count} posts")
print(f"⚠️  Advarsel: {message}")
print(f"❌ Feil: {error}")
```

### Pattern 9: Fallback Data

**If analysis fails, use previous month:**
```python
if rankings.get("error"):
    print("❌ Analyse feilet")

    # Try previous month
    prev_file = Path(OUTPUT_DIR) / f"rankings_{prev_period}.json"
    if prev_file.exists():
        with open(prev_file) as f:
            rankings = json.load(f)
        rankings["period"] = current_period
        print(f"✅ Bruker data fra {prev_period} som fallback")
```

### Pattern 10: Trend Calculation

**Compare ranks, handle new/missing tools:**
```python
def calculate_trend(current_rank: int, previous_rank: int|None) -> dict:
    if previous_rank is None:
        return {"status": "new", "rank_change": None}

    change = previous_rank - current_rank  # Positive = moved up

    if change > 0:
        return {"status": "rising", "rank_change": change}
    elif change < 0:
        return {"status": "falling", "rank_change": change}
    else:
        return {"status": "stable", "rank_change": 0}
```

---

## AI Assistant Guidelines

### When Working with This Codebase

1. **Read Before Modifying**
   - Always read existing code before suggesting changes
   - Understand the data flow and dependencies
   - Check `config.py` for relevant constants

2. **Maintain Consistency**
   - Follow existing patterns (async/await, error handling)
   - Use Norwegian for user-facing output
   - Keep emoji usage consistent with existing code

3. **Test Thoroughly**
   - Run `pytest` after changes
   - Test with `--collect-only` first (free)
   - Test with small datasets (`--days 7`) before full runs

4. **Respect Rate Limits**
   - Don't remove delays from collectors
   - Don't increase request volume without considering costs

5. **Document Changes**
   - Update this CLAUDE.md if architecture changes
   - Update README.md for user-facing changes
   - Add comments for complex logic

6. **Handle Errors Gracefully**
   - Don't let one collector failure crash entire pipeline
   - Provide informative error messages
   - Use fallbacks where appropriate

7. **Validate External Data**
   - Always normalize API responses immediately
   - Validate JSON from Claude before using
   - Handle missing/null fields safely

8. **Consider Costs**
   - Claude API calls cost money (analyze phase)
   - Collection is free (except Twitter which requires auth)
   - Prefer `--collect-only` for testing

### Common Questions

**Q: How do I add a new data source?**
A: Follow "Task 7: Add New Collector" in Common Tasks section

**Q: Why is the HTML generator so large (2531 LOC)?**
A: It embeds all HTML, CSS, JavaScript inline for standalone deployment

**Q: Can I change the ranking categories?**
A: Yes, edit `config.CATEGORIES` and Claude will adapt automatically

**Q: How do I debug Claude JSON parsing errors?**
A: Check `analyzer.py` → `extract_json_from_text()` and add debug prints

**Q: What if GitHub Actions fails?**
A: Check workflow logs, test locally with same commands, verify secrets

**Q: How do trends work?**
A: `trend_analyzer.py` compares current `rankings_YYYY-MM.json` with previous month's file

**Q: Can I run without Claude API?**
A: Yes, use `--collect-only` to just collect data without analysis

**Q: Where are provider logos stored?**
A: In `docs/assets/` directory

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# or create .env file with ANTHROPIC_API_KEY=...
```

### Issue: GitHub rate limit exceeded

**Solution:**
```bash
export GITHUB_TOKEN="ghp_..."
# Increases rate limit from 60/hour to 5000/hour
```

### Issue: Claude returns invalid JSON

**Symptoms:** JSON parsing errors, validation failures

**Debug:**
1. Check `analyzer.py` → `extract_json_from_text()`
2. Print raw Claude response
3. Look for markdown wrapping, truncation, trailing commas

**Solution:** Improve JSON extraction logic in `extract_json_from_text()`

### Issue: No posts collected

**Check:**
1. Internet connection
2. API endpoints are accessible
3. Keywords in `config.AI_KEYWORDS` are correct
4. `MIN_HN_POINTS` threshold isn't too high

### Issue: Tests failing

**Debug:**
```bash
pytest -v  # Verbose output
pytest -s  # Show print statements
pytest tests/unit/test_specific.py  # Run specific test
```

### Issue: Workflow fails on push

**Check:**
1. GitHub Actions logs
2. Secrets are set correctly (Settings → Secrets)
3. Branch protection rules
4. Workflow permissions

### Issue: Cloudflare deployment not updating

**Check:**
1. GitHub push succeeded
2. Cloudflare Pages build logs
3. `docs/index.html` was committed
4. Cloudflare Pages source branch is correct

---

## Version History

**2025-12-04:** Initial CLAUDE.md creation
- Documented complete architecture
- Added development workflows
- Included all major modules and patterns
- Comprehensive troubleshooting guide

---

## Quick Reference

### Essential Commands

```bash
# Development
python main.py --collect-only        # Test collection (free)
python main.py --days 7              # Quick analysis
python generate_html.py --dummy      # Test HTML

# Testing
pytest                               # Run tests
pytest --cov=src/ai_news_agent      # With coverage

# Deployment
git checkout dev                     # Switch to dev
git merge feature/my-feature         # Merge feature
git push origin dev                  # Deploy to preview

# Utilities
python check_links.py                # Validate URLs
python score_coding_assistants.py    # Score coding tools
python update_capabilities.py        # Update capability table
```

### Key Files

| File | Purpose |
|------|---------|
| `src/ai_news_agent/main.py` | Main pipeline orchestrator |
| `src/ai_news_agent/config.py` | All configuration |
| `src/ai_news_agent/analyzer/analyzer.py` | Claude integration |
| `src/ai_news_agent/generator/generate_html.py` | HTML generation |
| `data/tool_links.json` | Tool URLs (manual curation) |
| `output/rankings_YYYY-MM.json` | Monthly rankings output |
| `.github/workflows/daily.yml` | Daily automation |

### Important URLs

- **Production:** https://ai-radar.fyrk.no
- **Repository:** https://github.com/carlfrankalbert/ai-news-agent
- **Cloudflare Pages:** (Check Cloudflare dashboard for preview URLs)

---

**Remember:** When in doubt, read the existing code, follow established patterns, and test thoroughly before merging to `main`. 🚀
