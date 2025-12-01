# Quick Start Guide

## Første gang oppsett

```bash
# 1. Gå til prosjektmappen
cd /Users/carl/Desktop/FYRK/ai-news-agent

# 2. Opprett virtuelt miljø
python3 -m venv venv

# 3. Aktiver virtuelt miljø
source venv/bin/activate

# 4. Installer dependencies
pip install -r requirements.txt

# 5. Sett API-nøkkel (midlertidig for testing)
export ANTHROPIC_API_KEY="sk-ant-din-nøkkel-her"

# 6. Test at det fungerer
python3 main.py --collect-only --days 7
```

## Hver gang du åpner prosjektet

```bash
# 1. Gå til prosjektmappen
cd /Users/carl/Desktop/FYRK/ai-news-agent

# 2. Aktiver virtuelt miljø
source venv/bin/activate

# 3. Kjør agenten
python3 main.py --collect-only --days 7
```

## Vanlige kommandoer

```bash
# Samle data fra alle kilder (uten analyse)
python3 main.py --collect-only --days 7

# Full pipeline (samle + analyser med Claude)
python3 main.py --days 7

# Analyser allerede innsamlet data
python3 main.py --analyze-only

# Test en spesifikk collector
python3 -m collectors.reddit
python3 -m collectors.hackernews
```

## Feilsøking

### "command not found: python"
- Bruk `python3` i stedet for `python` på macOS

### "ModuleNotFoundError"
- Sjekk at du har aktivert virtuelt miljø: `source venv/bin/activate`
- Installer dependencies: `pip install -r requirements.txt`

### "ANTHROPIC_API_KEY not found"
- Sett miljøvariabel: `export ANTHROPIC_API_KEY="sk-ant-..."`
- Eller legg den i `.env` fil (husk å legge til i .gitignore)

