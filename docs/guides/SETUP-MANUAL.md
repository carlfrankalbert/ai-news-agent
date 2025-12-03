# AI News Agent - Oppsettmanual

**For:** Carl @ FYRK  
**Verktøy:** Cursor, GitHub, Domeneshop  
**Tid:** ~30 minutter

---

## Oversikt

Denne guiden tar deg gjennom:

1. Sette opp prosjektet lokalt i Cursor
2. Pushe til GitHub
3. Konfigurere automatisk kjøring
4. Publisere nettsiden via GitHub Pages
5. Koble til eget domene via Domeneshop

---

## Del 1: Lokal oppsett i Cursor

### 1.1 Last ned og pakk ut prosjektet

1. Last ned `ai-news-agent-v2.zip` fra Claude
2. Pakk ut til en mappe, f.eks. `~/Projects/ai-news-agent`

### 1.2 Åpne i Cursor

1. Åpne Cursor
2. `File` → `Open Folder` → velg `ai-news-agent`-mappen

### 1.3 Sett opp Python-miljø

Åpne terminal i Cursor (`Ctrl+`` ` eller `View` → `Terminal`):

```bash
# Lag virtuelt miljø
python -m venv venv

# Aktiver miljøet
# På Mac/Linux:
source venv/bin/activate
# På Windows:
.\venv\Scripts\activate

# Installer dependencies
pip install -r requirements.txt
```

### 1.4 Test lokalt (valgfritt)

```bash
# Sett API-nøkkel midlertidig
export ANTHROPIC_API_KEY="sk-ant-din-nøkkel-her"

# Kjør agent
python main.py --days 7

# Generer HTML
python generate_html.py
```

Sjekk at `output/` og `docs/` har filer.

---

## Del 2: Push til GitHub

### 2.1 Opprett nytt repository

1. Gå til [github.com/new](https://github.com/new)
2. **Repository name:** `ai-news-agent` (eller hva du vil)
3. **Description:** `AI verktøy-radar basert på Hacker News`
4. Velg **Private** eller **Public**
5. **IKKE** huk av for "Add a README file" (du har allerede en)
6. Klikk **Create repository**

### 2.2 Push koden fra Cursor

I Cursor-terminalen:

```bash
# Initialiser git (hvis ikke allerede gjort)
git init

# Legg til alle filer
git add .

# Første commit
git commit -m "Initial commit: AI News Agent"

# Koble til GitHub (erstatt med ditt brukernavn)
git remote add origin https://github.com/DITT_BRUKERNAVN/ai-news-agent.git

# Push
git branch -M main
git push -u origin main
```

> **Tips:** Hvis du bruker SSH i stedet for HTTPS:
> ```bash
> git remote add origin git@github.com:DITT_BRUKERNAVN/ai-news-agent.git
> ```

---

## Del 3: Konfigurer GitHub Actions

### 3.1 Legg til Anthropic API-nøkkel som secret

1. Gå til ditt repo på GitHub
2. Klikk **Settings** (tannhjul-ikon)
3. I venstre meny: **Secrets and variables** → **Actions**
4. Klikk **New repository secret**
5. **Name:** `ANTHROPIC_API_KEY`
6. **Secret:** Din Anthropic API-nøkkel (starter med `sk-ant-...`)
7. Klikk **Add secret**

### 3.2 Verifiser workflow-filen

Sjekk at `.github/workflows/daily.yml` finnes i prosjektet. Den skal se slik ut:

```yaml
name: Daily AI News Scan

on:
  schedule:
    - cron: '0 6 * * *'  # 06:00 UTC daglig
  workflow_dispatch:      # Manuell trigger

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run AI News Agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python main.py --days 7
      - name: Generate HTML report
        run: python generate_html.py
      - name: Commit and push results
        run: |
          git config user.name "AI News Bot"
          git config user.email "bot@users.noreply.github.com"
          git add output/ docs/
          git diff --staged --quiet || git commit -m "🤖 Scan $(date +%Y-%m-%d)"
          git push
```

### 3.3 Kjør workflow manuelt (første gang)

1. Gå til **Actions**-fanen i ditt repo
2. Klikk på **Daily AI News Scan** i venstre meny
3. Klikk **Run workflow** → **Run workflow**
4. Vent 2-3 minutter mens den kjører
5. Sjekk at den fullførte (grønn hake)

---

## Del 4: Aktiver GitHub Pages

### 4.1 Slå på GitHub Pages

1. Gå til **Settings** i ditt repo
2. Scroll ned til **Pages** i venstre meny
3. Under **Source**, velg:
   - **Deploy from a branch**
4. Under **Branch**, velg:
   - Branch: `main`
   - Folder: `/docs`
5. Klikk **Save**

### 4.2 Vent på deployment

1. Gå tilbake til **Actions**-fanen
2. Du ser en ny workflow "pages build and deployment"
3. Vent til den er ferdig (1-2 min)

### 4.3 Åpne nettsiden

Din side er nå live på:
```
https://DITT_BRUKERNAVN.github.io/ai-news-agent/
```

---

## Del 5: Koble til eget domene (Domeneshop)

### 5.1 Velg domene-oppsett

Du har to valg:

**A) Subdomene** (anbefalt for testing):  
`ai.fyrk.no` eller `radar.fyrk.no`

**B) Egen mappe på hoveddomene:**  
Ikke mulig med GitHub Pages alene - krever redirect

Vi går for **subdomene** her.

### 5.2 Legg til CNAME i GitHub

1. I Cursor, lag en ny fil: `docs/CNAME`
2. Skriv inn domenet (uten `https://`):
   ```
   ai.fyrk.no
   ```
3. Commit og push:
   ```bash
   git add docs/CNAME
   git commit -m "Add custom domain"
   git push
   ```

### 5.3 Konfigurer DNS i Domeneshop

1. Logg inn på [domeneshop.no](https://domeneshop.no)
2. Gå til **Mine domener** → velg `fyrk.no`
3. Klikk på **DNS**-fanen
4. Legg til ny **CNAME-record**:

   | Type | Navn | Verdi |
   |------|------|-------|
   | CNAME | ai | DITT_BRUKERNAVN.github.io |

   > Erstatt `DITT_BRUKERNAVN` med ditt GitHub-brukernavn

5. Klikk **Lagre**

### 5.4 Aktiver HTTPS i GitHub

1. Gå til repo **Settings** → **Pages**
2. Under **Custom domain**, skriv: `ai.fyrk.no`
3. Klikk **Save**
4. Vent noen minutter (DNS-propagering)
5. Huk av **Enforce HTTPS** når den blir tilgjengelig

### 5.5 Verifiser

Etter 5-30 minutter skal siden være tilgjengelig på:
```
https://ai.fyrk.no
```

---

## Vedlikehold

### Manuell kjøring

Gå til **Actions** → **Daily AI News Scan** → **Run workflow**

### Endre kjøretidspunkt

Rediger `.github/workflows/daily.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'   # 06:00 UTC = 07:00 norsk vintertid
  - cron: '0 7 * * *'   # 07:00 UTC = 08:00 norsk vintertid
  - cron: '0 18 * * *'  # 18:00 UTC = 19:00 norsk vintertid
```

### Legge til flere datakilder

Rediger `config.py` for å justere søkeord, eller lag nye collectors i `collectors/`-mappen.

### Se logger

Gå til **Actions** → klikk på en workflow-kjøring → klikk på **scan** → se output fra hvert steg.

---

## Feilsøking

### "Permission denied" ved push

```bash
git remote set-url origin https://github.com/DITT_BRUKERNAVN/ai-news-agent.git
```
Eller sett opp SSH-nøkler.

### Workflow feiler med "API key not found"

Sjekk at secret heter nøyaktig `ANTHROPIC_API_KEY` (case-sensitive).

### Siden viser 404

1. Sjekk at `docs/index.html` finnes
2. Sjekk at GitHub Pages er satt til `/docs`-mappen
3. Vent noen minutter etter push

### DNS fungerer ikke

- CNAME-endringer kan ta opptil 24 timer (vanligvis 5-30 min)
- Sjekk at CNAME-verdien er `brukernavn.github.io` (med punktum til slutt i noen DNS-paneler)

---

## Oppsummering

| Steg | Status |
|------|--------|
| 1. Lokal oppsett | ☐ |
| 2. Push til GitHub | ☐ |
| 3. API-nøkkel som secret | ☐ |
| 4. Første workflow-kjøring | ☐ |
| 5. GitHub Pages aktivert | ☐ |
| 6. Custom domain (valgfritt) | ☐ |

**Neste steg:** Når alt fungerer, kan du utvide med flere datakilder (Reddit, Product Hunt) eller justere HTML-designet.

---

*Laget for FYRK av Claude*
