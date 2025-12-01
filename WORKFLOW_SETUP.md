# GitHub Actions Workflow Setup

## Steg-for-steg guide

### 1. Legg til Anthropic API-nøkkel som Secret

1. Gå til ditt repo på GitHub:
   https://github.com/carlfrankalbert/ai-news-agent

2. Klikk på **Settings** (tannhjul-ikonet øverst til høyre)

3. I venstre meny, klikk på **Secrets and variables** → **Actions**

4. Klikk på **New repository secret**

5. Fyll inn:
   - **Name:** `ANTHROPIC_API_KEY` (må være nøyaktig dette, case-sensitive)
   - **Secret:** Din Anthropic API-nøkkel (starter med `sk-ant-...`)

6. Klikk **Add secret**

### 2. Verifiser workflow-filen

Workflow-filen er allerede lagt til i repoet:
- `.github/workflows/daily.yml`

Den kjører:
- **Daglig klokken 06:00 UTC** (07:00 norsk vintertid)
- **Manuelt** når du klikker "Run workflow" i Actions-fanen

### 3. Test workflow (første gang)

1. Gå til **Actions**-fanen i ditt repo:
   https://github.com/carlfrankalbert/ai-news-agent/actions

2. Klikk på **Daily AI News Scan** i venstre meny

3. Klikk på **Run workflow** (øverst til høyre)

4. Velg **main** branch og klikk **Run workflow**

5. Vent 2-5 minutter mens workflow kjører

6. Sjekk at den fullførte (grønn hake ✅)

### 4. Verifiser resultatet

Etter workflow er ferdig:

1. Gå tilbake til **Code**-fanen
2. Sjekk at `docs/index.html` er oppdatert
3. Sjekk at `output/rankings_*.json` er opprettet
4. Cloudflare Pages vil automatisk deploye til **fyrk.eu**

## Hva workflow gjør

1. ✅ Checkout kode fra GitHub
2. ✅ Setter opp Python 3.11
3. ✅ Installerer dependencies (`pip install -r requirements.txt`)
4. ✅ Kjører agent (`python main.py --days 7`)
   - Samler data fra Hacker News, Reddit, Product Hunt
   - Analyserer med Claude
   - Genererer rankings JSON
5. ✅ Genererer HTML (`python generate_html.py`)
6. ✅ Committer og pusher endringer til GitHub
7. ✅ Cloudflare Pages deployer automatisk

## Endre kjøretidspunkt

Hvis du vil endre når workflow kjører, rediger `.github/workflows/daily.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'   # 06:00 UTC = 07:00 norsk vintertid
  - cron: '0 18 * * *'  # 18:00 UTC = 19:00 norsk vintertid (kveld)
```

Cron-format: `minutt time dag måned ukedag`
- `0 6 * * *` = Hver dag klokken 06:00 UTC
- `0 */6 * * *` = Hver 6. time
- `0 0 * * 1` = Hver mandag klokken 00:00 UTC

## Feilsøking

### "ANTHROPIC_API_KEY not found"
- Sjekk at secret heter nøyaktig `ANTHROPIC_API_KEY` (case-sensitive)
- Sjekk at du har lagt den til i Settings → Secrets and variables → Actions

### Workflow feiler med "Permission denied"
- Sjekk at workflow har `permissions: contents: write` (den har det allerede)
- Sjekk at du har push-tilgang til repoet

### "No module named 'httpx'"
- Dependencies installeres automatisk, men hvis det feiler:
  - Sjekk at `requirements.txt` er korrekt
  - Sjekk workflow logs for detaljer

### HTML genereres ikke
- Sjekk at `output/rankings_*.json` eksisterer
- Sjekk workflow logs for feil i `generate_html.py`

## Automatisk deployment til Cloudflare

Cloudflare Pages vil automatisk deploye når:
- Endringer pushes til `main` branch
- Filer i `docs/` mappen endres

Sjekk Cloudflare Dashboard → Pages → ditt prosjekt → Deployments for status.

