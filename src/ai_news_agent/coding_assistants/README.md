# Coding Assistant Scoring Agent

Automatically scores and ranks AI coding assistant tools using data from GitHub, Hacker News, and Reddit.

## Features

- **Multi-source data collection**: GitHub API, Hacker News Algolia API, Reddit JSON API
- **Sentiment analysis**: Uses VADER sentiment analyzer for HN and Reddit comments
- **Percentile-based scoring**: Ranks tools relative to each other
- **Comprehensive scoring**: Buzz (30%), Sentiment (25%), Utility (25%), Price (20%)

## Usage

### Basic usage (all tools)

```bash
python score_coding_assistants.py
```

### Process specific tool

```bash
python score_coding_assistants.py --tool "Cursor"
```

### Custom lookback period

```bash
python score_coding_assistants.py --days 60
```

## Output Files

1. **Raw data**: `data/coding_assistants/raw/{date}_raw.json`
   - Contains all raw API responses

2. **Scores**: `data/coding_assistants/scores/{date}_scores.json`
   - Contains calculated scores for each tool

3. **Rankings**: `output/coding_assistants_rankings.json`
   - Final ranked list with all metrics

## Configuration

### Tools

Edit `src/ai_news_agent/coding_assistants/config.py` to add/modify tools.

### Manual Scores

- **Features**: `data/coding_assistants/features.json`
  - Utility scores (multi-language, IDE integration, etc.)

- **Pricing**: `data/coding_assistants/pricing.json`
  - Pricing tiers and scores

## Scoring Formula

### Buzz Score (30%)
- GitHub stars percentile: 40%
- GitHub stars growth percentile: 30%
- HN mentions percentile: 15%
- Reddit mentions percentile: 15%

### Sentiment Score (25%)
- GitHub issue health (closed/total): 30%
- HN sentiment average: 35%
- Reddit sentiment average: 35%

### Utility Score (25%)
- Loaded from `features.json` (manual scoring)

### Price Score (20%)
- Loaded from `pricing.json` (manual scoring)

### Final Score
```
FINAL = (BUZZ × 0.30) + (SENTIMENT × 0.25) + (UTILITY × 0.25) + (PRICE × 0.20)
```

## Environment Variables

- `GITHUB_TOKEN`: Optional GitHub token for higher rate limits (5000 req/hour vs 60)

## Rate Limiting

The script includes rate limiting:
- GitHub: 0.5s delay (authenticated) or 2s (unauthenticated)
- Hacker News: 0.5s delay
- Reddit: 1s delay per subreddit

## Dependencies

- `httpx`: HTTP client
- `nltk`: Sentiment analysis (VADER)

