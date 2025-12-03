# AI News Agent

En AI-agent som scanner Hacker News og GitHub for omtaler av AI-verktøy, analyserer dataene med Claude, og genererer en rangert oversikt i JSON og HTML-format.

**Live**: [FYRK AI Radar](https://ai-radar.fyrk.no)

## 🚀 Rask start

```bash
# 1. Installer dependencies
pip install -r requirements.txt

# 2. Sett Anthropic API-nøkkel
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Kjør full pipeline
python main.py

# 4. Generer HTML
python generate_html.py
```

## 📁 Struktur

```
ai-news-agent/
├── src/ai_news_agent/         # Hovedpakke (all Python-kode)
│   ├── collectors/            # Datainnsamling (HN, GitHub)
│   ├── analyzer/              # Analyse med Claude + trender
│   ├── generator/             # HTML-generering
│   └── utils/                 # Hjelpefunksjoner
├── main.py                    # Entry point
├── generate_html.py           # HTML-generator entry point
├── check_links.py             # Link validator entry point
├── docs/                      # Public website (Cloudflare Pages)
│   ├── index.html             # Hovedside med rankings
│   └── assets/                # Logoer og bilder
├── output/                    # JSON-output
│   ├── rankings_YYYY-MM.json  # Månedlige rankings
│   └── raw_posts_YYYY-MM.json # Rådata fra innsamling
├── data/                      # Statisk data
│   └── tool_links.json        # Verktøy-URLs
├── scripts/                   # Shell-scripts for testing
└── documentation/             # Intern dokumentasjon
```

## 🎯 Bruk

```bash
# Full pipeline (samle + analyser + trend)
python main.py

# Bare samle data (gratis, ingen API-kall)
python main.py --collect-only

# Analyser eksisterende data
python main.py --analyze-only

# Override antall dager (default: 90)
python main.py --days 30

# Generer HTML fra siste rankings
python generate_html.py

# Test med dummy-data
python generate_html.py --dummy
```

## 🏗 Arkitektur

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│   main.py   │────▶│  collectors/ │────▶│  analyzer   │────▶│  output/ │
│ (orkestrer) │     │ (HN, GitHub) │     │  (Claude)   │     │  (JSON)  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
                                                                   │
                                                                   ▼
                                                            ┌──────────┐
                                                            │  docs/   │
                                                            │  (HTML)  │
                                                            └──────────┘
```

## 🔧 Teknisk stack

- **Python 3.11+**
- **httpx** - Async HTTP-klient
- **anthropic** - Claude SDK
- **Cloudflare Pages** - Hosting
- **GitHub Actions** - Daglig kjøring

## 📦 Output

Genererer to filer i `output/`:

1. `raw_posts_YYYY-MM.json` - Rå data fra kilder
2. `rankings_YYYY-MM.json` - Analyserte rankings med trender

HTML-output genereres i `docs/index.html` for Cloudflare Pages.

## 🚢 Deployment

GitHub Actions kjører automatisk daglig (`daily.yml`):
1. Samler data fra HN og GitHub
2. Analyserer med Claude
3. Genererer HTML
4. Committer og pusher til repo
5. Cloudflare Pages deployer automatisk

**Manuell kjøring**: Trigger `Daily AI News Scan` workflow i GitHub Actions.

## 📚 Dokumentasjon

Intern dokumentasjon ligger i `documentation/`:
- `guides/` - Setup og deployment-guider
- `infrastructure/` - Infrastruktur-dokumentasjon

## 📝 Lisens

Laget for FYRK 🚀
