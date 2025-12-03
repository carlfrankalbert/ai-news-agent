# Quick Start Guide

## 🚀 Lokal utvikling

### 1. Installer dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Sett API-nøkkel

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Kjør

```bash
# Full pipeline (samler data + analyserer med Claude)
python main.py

# Bare samle data (gratis test)
python main.py --collect-only

# Generer HTML
python generate_html.py

# Test med dummy-data
python generate_html.py --dummy
```

## 🧪 Test-scripts

```bash
./scripts/start_test_env.sh    # Sett opp test-miljø
./scripts/test_quick.sh        # Samle data (ingen API)
./scripts/test_full.sh         # Full test (bruker Claude)
./scripts/test_ui.sh           # Test HTML med dummy-data
./scripts/serve_local.sh       # Lokal webserver
```

## 🚢 Deployment

### GitHub Secrets

Legg til disse i GitHub repo → Settings → Secrets:
- `ANTHROPIC_API_KEY` - Claude API-nøkkel
- `CLOUDFLARE_API_TOKEN` - For Pages deployment (valgfritt)
- `CLOUDFLARE_ACCOUNT_ID` - For Pages deployment (valgfritt)

### Automatisk deployment

GitHub Actions kjører daglig (`daily.yml`):
1. Samler data
2. Analyserer med Claude
3. Genererer HTML
4. Committer til repo
5. Cloudflare Pages deployer automatisk fra `docs/`

### Manuell deployment

1. Gå til GitHub → Actions
2. Velg "Daily AI News Scan"
3. Klikk "Run workflow"

---

Se [README.md](./README.md) for mer informasjon.
