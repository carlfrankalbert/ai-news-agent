# AI News Agent

En AI-agent som scanner Hacker News og GitHub for omtaler av AI-verktøy, analyserer dataene med Claude, og genererer en rangert oversikt i JSON og HTML-format.

## 🚀 Rask start

```bash
# 1. Installer dependencies
pip install -r requirements.txt

# 2. Sett Anthropic API-nøkkel
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Kjør
python main.py
```

## 📁 Struktur

```
ai-news-agent/
├── src/ai_news_agent/     # Hovedpakke
│   ├── collectors/         # Datainnsamling (HN, GitHub)
│   ├── analyzer/           # Analyse med Claude
│   ├── generator/          # HTML-generering
│   └── utils/              # Hjelpefunksjoner
├── infra/                  # Infrastruktur (deployment, scripts)
├── scripts/                # Test-scripts
├── docs/                   # HTML-output og dokumentasjon
│   ├── guides/             # Setup-guider
│   └── infrastructure/     # Infrastruktur-dokumentasjon
└── output/                 # JSON-output
```

## 🎯 Bruk

```bash
# Full pipeline (samle + analyser)
python main.py

# Bare samle data
python main.py --collect-only

# Analyser eksisterende data
python main.py --analyze-only

# Override antall dager
python main.py --days 30

# Generer HTML
python generate_html.py
```

## 📚 Dokumentasjon

- **[QUICKSTART.md](docs/infrastructure/QUICKSTART.md)** - Rask start for deployment
- **[DEPLOYMENT.md](docs/infrastructure/DEPLOYMENT.md)** - Komplett deployment-guide
- **[REFACTORING.md](REFACTORING.md)** - Refaktoreringsdetaljer
- **[TESTING.md](docs/guides/TESTING.md)** - Testing-guide

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
- **GitHub Actions** - CI/CD

## 📦 Output

Genererer to filer i `output/`:

1. `raw_posts_YYYY-MM.json` - Rå data fra kilder
2. `rankings_YYYY-MM.json` - Analyserte rankings med trender

HTML-output genereres i `docs/index.html` for GitHub Pages.

## 🚢 Deployment

Se [DEPLOYMENT.md](docs/infrastructure/DEPLOYMENT.md) for komplett guide.

**Kortversjon:**
- Slack: `/deploy dev` eller `/deploy prod`
- Makefile: `make deploy-dev` eller `make deploy-prod`
- GitHub Actions: Manuell trigger i Actions-tab

## 📝 Lisens

Laget for FYRK 🚀
