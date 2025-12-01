# Test Workflow - Steg-for-steg

## Første gang: Sett opp Secret

### 1. Legg til Anthropic API-nøkkel

1. Gå til: https://github.com/carlfrankalbert/ai-news-agent/settings/secrets/actions
2. Klikk **"New repository secret"**
3. Fyll inn:
   - **Name:** `ANTHROPIC_API_KEY` (må være nøyaktig dette)
   - **Secret:** Din API-nøkkel (starter med `sk-ant-...`)
4. Klikk **"Add secret"**

## Test Workflow

### Metode 1: Via GitHub UI (anbefalt)

1. Gå til: https://github.com/carlfrankalbert/ai-news-agent/actions

2. Klikk på **"Daily AI News Scan"** i venstre meny

3. Klikk på **"Run workflow"** (knapp øverst til høyre)

4. Velg:
   - **Branch:** `main`
   - Klikk **"Run workflow"**

5. Vent 2-5 minutter mens workflow kjører

6. Klikk på den nye workflow-kjøringen for å se progress

7. Sjekk at alle steg har grønn hake ✅

### Metode 2: Test lokalt først (valgfritt)

```bash
cd /Users/carl/Desktop/FYRK/ai-news-agent
source venv/bin/activate
export ANTHROPIC_API_KEY="sk-ant-din-nøkkel-her"
python3 main.py --days 7
python3 generate_html.py
```

## Hva skal skje

1. ✅ **Checkout repo** - Henter kode
2. ✅ **Setup Python** - Setter opp Python 3.11
3. ✅ **Install dependencies** - Installerer httpx, anthropic, etc.
4. ✅ **Run AI News Agent** - Samler data og analyserer
5. ✅ **Generate HTML report** - Lager HTML i docs/
6. ✅ **Commit and push** - Pusher endringer til GitHub
7. ✅ **Cloudflare Pages** - Deployer automatisk til fyrk.eu

## Verifisering

Etter workflow er ferdig:

1. Gå til **Code**-fanen
2. Sjekk at `docs/index.html` er oppdatert
3. Sjekk at `output/rankings_*.json` er opprettet
4. Sjekk https://fyrk.eu - skal vise nytt innhold

## Feilsøking

### "ANTHROPIC_API_KEY not found"
- Sjekk at secret heter nøyaktig `ANTHROPIC_API_KEY`
- Sjekk at du har lagt den til i Settings → Secrets

### Workflow feiler på "Run AI News Agent"
- Sjekk workflow logs for detaljer
- Verifiser at API-nøkkelen er gyldig

### "Permission denied" ved push
- Workflow har allerede `contents: write` permission
- Sjekk at repoet er ditt og du har push-tilgang

### HTML genereres ikke
- Sjekk at `output/rankings_*.json` eksisterer
- Sjekk workflow logs for feil i `generate_html.py`

