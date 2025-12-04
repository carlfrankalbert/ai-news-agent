# AI Capability Monitor

Monthly automated agent that monitors and updates an AI model capability comparison table.

## Overview

This module automatically:
1. Searches for the latest capabilities of major AI models
2. Fetches benchmark results to determine best-in-category models
3. Generates an updated capability comparison table
4. Tracks changes from previous updates
5. Commits results to the repository

## Models Tracked

- Claude Opus 4.5 (Anthropic)
- ChatGPT (GPT-5) (OpenAI)
- Gemini (2.5/3 Pro) (Google)
- Grok 3/4 (xAI)
- Llama 4 (Meta)
- DeepSeek (V3/R1)

## Capability Categories

### Cognitive abilities
- Reasoning
- Coding
- Memory (context)
- Multilingual / Norwegian

### Visual abilities
- Image generation
- Image understanding
- Video generation
- Video understanding

### Audio & speech
- Speech-to-text
- Text-to-speech
- Audio understanding
- Audio generation

### System abilities
- Web search / browsing
- Document & PDF understanding
- File handling
- API calling
- Computer use

### Automation
- Agents / autonomous actions
- Multi-step workflows
- Scheduling
- Tool use

## Usage

### Manual Run

```bash
# Set API key
export ANTHROPIC_API_KEY=your_key_here

# Run the monitor
python -m src.ai_news_agent.capability_monitor.main

# With custom directories
python -m src.ai_news_agent.capability_monitor.main \
  --data-dir data/capability_monitor \
  --output-dir output

# Dry run (fetch but don't save)
python -m src.ai_news_agent.capability_monitor.main --dry-run
```

### Automated Run

The GitHub Actions workflow runs automatically on the 1st of each month at 09:00 UTC.

You can also trigger it manually from the Actions tab in GitHub.

## Output Files

- `data/capability_monitor/current_table.md` - Current capability table
- `data/capability_monitor/current_capabilities.json` - JSON data for comparison
- `data/capability_monitor/previous_capabilities.json` - Previous version for diff
- `data/capability_monitor/history/capabilities_YYYY-MM.json` - Monthly history
- `output/capability_report.md` - Full report with changes

## Symbols

- `✔︎` = Supported
- `✗` = Not supported
- `~` = Partial support
- `⭐` = Best in category (only ONE model per row can have this)

## Requirements

- Python 3.11+
- Anthropic API key (set as `ANTHROPIC_API_KEY` environment variable)
- `anthropic` package (included in requirements.txt)

## Configuration

Edit `config.py` to:
- Add/remove models
- Modify capability categories
- Update search queries
- Change symbols

