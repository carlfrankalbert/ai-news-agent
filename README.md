# AI News Agent MVP

En enkel agent som samler AI-verktøy-mentions fra Hacker News og rangerer dem med Claude.

## Arkitektur

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│   main.py   │────▶│  collectors/ │────▶│  analyzer   │────▶│  output/ │
│ (orchestrer)│     │ (HN Algolia) │     │  (Claude)   │     │  (JSON)  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
```

## Rask start

```bash
# 1. Opprett virtuelt miljø (anbefalt)
python3 -m venv venv
source venv/bin/activate  # På Windows: venv\Scripts\activate

# 2. Installer dependencies
pip install -r requirements.txt

# 3. Sett Anthropic API-nøkkel
export ANTHROPIC_API_KEY="sk-ant-..."

# 4. Kjør
python3 main.py
# Eller hvis du er i venv: python main.py
```

## Bruk

```bash
# Aktiver virtuelt miljø først (hvis du bruker det)
source venv/bin/activate

# Full pipeline (samle + analyser)
python3 main.py

# Bare samle data (for manuell review først)
python3 main.py --collect-only

# Analyser allerede innsamlet data
python3 main.py --analyze-only

# Override antall dager
python3 main.py --days 30
```

## Output

Genererer to filer i `output/`:

1. `raw_posts_YYYY-MM.json` - Rå HN-posts
2. `rankings_YYYY-MM.json` - Analyserte rankings

### Rankings JSON-struktur

```json
{
  "period": "2025-03",
  "categories": [
    {
      "name": "Kjerne-LLM-er",
      "slug": "core-llms",
      "top3": [
        {
          "rank": 1,
          "medal": "gold",
          "name": "Claude 3.5",
          "provider": "Anthropic",
          "short_reason": "...",
          "scores": { ... }
        }
      ]
    }
  ],
  "new_and_noteworthy": [ ... ]
}
```

## Deployment

### Cloudflare Pages (Nåværende setup)

Nettsiden er deployet til **Cloudflare Pages** på domenet **fyrk.eu**.

- **Automatisk deployment:** Når GitHub Actions pusher endringer til `docs/` mappen
- **Custom domain:** fyrk.eu
- **Build:** Ingen build nødvendig (statisk HTML)
- **Output directory:** `docs/`

Se [CLOUDFLARE_SETUP.md](./CLOUDFLARE_SETUP.md) for detaljer.

### Option 1: GitHub Actions (alternativ)

Lag `.github/workflows/daily-run.yml`:

```yaml
name: Daily AI News Scan

on:
  schedule:
    - cron: '0 6 * * *'  # Kjør 06:00 UTC daglig
  workflow_dispatch:  # Manuell trigger

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python main.py --days 7
      
      - name: Commit results
        run: |
          git config user.name "AI News Bot"
          git config user.email "bot@example.com"
          git add output/
          git commit -m "Daily scan $(date +%Y-%m-%d)" || exit 0
          git push
```

### Option 2: Modal.com (serverless)

```python
# modal_app.py
import modal

app = modal.App("ai-news-agent")

@app.function(
    schedule=modal.Cron("0 6 * * *"),
    secrets=[modal.Secret.from_name("anthropic-key")]
)
async def daily_scan():
    from main import main
    await main()
```

### Option 3: Railway/Render

1. Push til GitHub
2. Koble til Railway/Render
3. Sett `ANTHROPIC_API_KEY` som env var
4. Sett opp cron job via deres UI

## Semi-manuell review workflow

1. Kjør `python main.py --collect-only`
2. Se gjennom `output/raw_posts_*.json`
3. Eventuelt filtrer/juster manuelt
4. Kjør `python main.py --analyze-only`
5. Review `output/rankings_*.json`
6. Publiser/del

## Utvidelser

- [x] Legg til Reddit-collector (r/MachineLearning, r/LocalLLaMA, r/artificial, etc.)
- [x] Legg til Product Hunt (grunnleggende struktur - kan utvides med API key)
- [ ] Web UI for review
- [ ] Slack/Discord-notifikasjoner
- [ ] Historisk trending (sammenlign med forrige måned)
- [ ] GitHub Trending collector
- [ ] Twitter/X collector

## Kostnader

- **Hacker News API**: Gratis (Algolia)
- **Claude API**: ~$0.01-0.05 per kjøring (avhenger av datamengde)
- **Hosting**: Gratis med GitHub Actions

---

Laget for FYRK 🚀
