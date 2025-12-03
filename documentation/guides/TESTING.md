# Testing Guide

## Rask testing

### 1. Test kun datainnsamling (uten analyse)
```bash
python main.py --collect-only --days 7
```
- Samler data fra HN og GitHub
- Lagrer til `output/raw_posts_YYYY-MM.json`
- Ingen API-kostnader (bruker ikke Claude)

### 2. Test kun analyse (bruker cached data)
```bash
python main.py --analyze-only --days 7
```
- Bruker eksisterende data fra `output/raw_posts_*.json`
- Kjører Claude-analyse
- Nyttig for å teste analyse uten å samle data på nytt

### 3. Test full pipeline (samle + analyser)
```bash
python main.py --days 7
```
- Samler data og analyserer
- Full kostnad (samling + Claude API)

### 4. Test med kortere periode (billigere)
```bash
python main.py --days 1
```
- Mindre data = lavere API-kostnader
- Raskere testing

## Test individuelle collectors

### Test Hacker News collector
```bash
python -m collectors.hackernews
```

### Test GitHub collector
```bash
python -m collectors.github
```

## Test HTML-generering

```bash
# Først, sørg for at du har rankings data
python main.py --days 7

# Generer HTML
python generate_html.py

# Sjekk resultatet
open docs/index.html
```

## Test GitHub Actions workflow

### Lokalt (simuler workflow)
```bash
# Installer dependencies
pip install -r requirements.txt

# Kjør samme kommandoer som workflow
python main.py --days 7
python generate_html.py
```

### På GitHub
1. Gå til: https://github.com/carlfrankalbert/ai-news-agent/actions
2. Klikk "Daily AI News Scan"
3. Klikk "Run workflow" (øverst til høyre)
4. Velg branch: `main`
5. Klikk "Run workflow"

## Verifisering

### Sjekk output
```bash
# Se rådata
cat output/raw_posts_2025-12.json | python -m json.tool | head -50

# Se rankings
cat output/rankings_2025-12.json | python -m json.tool | head -100

# Sjekk HTML
ls -lh docs/index.html
```

### Sjekk at begge kilder er med
```bash
# Tell items per kilde
cat output/raw_posts_2025-12.json | python -c "import json, sys; data=json.load(sys.stdin); sources={}; [sources.update({item['source']: sources.get(item['source'], 0) + 1}) for item in data]; print('Sources:', sources)"
```

## Troubleshooting

### Hvis GitHub collector ikke finner repos
- Sjekk at du har internett-tilgang
- Prøv med lengre periode: `--days 30`
- Sjekk debug output i konsollen

### Hvis Claude-analyse feiler
- Sjekk at `ANTHROPIC_API_KEY` er satt i `.env`
- Test: `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Key:', os.getenv('ANTHROPIC_API_KEY')[:20] + '...')"`

### Hvis HTML ikke genereres
- Sjekk at `output/rankings_*.json` eksisterer
- Kjør `python generate_html.py` manuelt
- Sjekk for feilmeldinger

