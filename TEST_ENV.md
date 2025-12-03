# Test Environment Guide

## Quick Start

```bash
# Start test environment (activates venv and installs dependencies)
./scripts/start_test_env.sh

# Or manually:
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Status

✅ **Virtual Environment**: `venv/` (Python 3.9.6)  
✅ **Dependencies**: Installed  
✅ **Package Structure**: Verified  

## Available Commands

### Basic Commands

```bash
# Show help
python main.py --help

# Collect data only (no API costs)
python main.py --collect-only --days 1

# Full pipeline (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY='sk-ant-...'
python main.py --days 7

# Generate HTML with dummy data
python generate_html.py --dummy
```

### Test Scripts

```bash
# Quick test (collect only, no API costs)
./scripts/test_quick.sh

# Full test (includes Claude analysis)
./scripts/test_full.sh

# UI test (generate HTML with dummy data)
./scripts/test_ui.sh
```

## Environment Variables

### Required for Full Pipeline

```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Optional

```bash
export GITHUB_TOKEN='ghp_...'  # For higher GitHub API rate limits
```

## Verification

Test that everything works:

```bash
source venv/bin/activate

# Test imports
python -c "import sys; sys.path.insert(0, 'src'); from ai_news_agent.config import CATEGORIES; print(f'✅ {len(CATEGORIES)} categories loaded')"

# Test main entry point
python main.py --help

# Test HTML generator
python generate_html.py --dummy
```

## Troubleshooting

### Virtual environment not activating

```bash
# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import errors

```bash
# Make sure you're in project root
cd /path/to/ai-news-agent

# Verify src structure exists
ls -la src/ai_news_agent/
```

### Missing dependencies

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Next Steps

1. Set `ANTHROPIC_API_KEY` if you want to run full pipeline
2. Run `./scripts/test_quick.sh` for a quick test
3. Check `output/` directory for results
4. View HTML output in `docs/index.html`


