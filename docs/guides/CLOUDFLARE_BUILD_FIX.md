# Fikse Cloudflare Pages Build-konfigurasjon - Intern feil

## Problem
"An internal error prevented the form from submitting" når du prøver å oppdatere build-konfigurasjonen.

## Løsning: Fjern "None" fra Deploy command

### Steg 1: Fjern "None" fra Deploy command

1. I build-konfigurasjonsmodalen:
   - **Build command:** La stå TOM (ikke "None")
   - **Deploy command:** La stå TOM (ikke "None") ← Dette er problemet
   - **Non-production branch deploy command:** La stå TOM
   - **Path:** `/`

2. **Viktig:** Slett teksten "None" fra "Deploy command" feltet
   - Klikk i feltet
   - Marker alt (Cmd+A / Ctrl+A)
   - Slett (Delete / Backspace)
   - La feltet stå helt tomt

### Steg 2: Prøv igjen

1. Klikk **"Update"** knappen
2. Hvis det fortsatt feiler, prøv:
   - Refresh siden (F5)
   - Logg ut og inn igjen
   - Prøv i en annen nettleser

## Alternativ løsning: Bruk Wrangler CLI

Hvis web UI fortsatt feiler, kan du konfigurere via Wrangler CLI:

```bash
# Installer Wrangler
npm install -g wrangler

# Login til Cloudflare
wrangler login

# Opprett wrangler.toml i repoet
```

Men for statisk HTML er det enklere å fikse i UI.

## Hvis ingenting fungerer

1. **Slett og opprett prosjektet på nytt:**
   - Pages → ai-news-agent → Settings → General
   - Scroll ned til "Delete project"
   - Slett prosjektet
   - Opprett på nytt med riktig konfigurasjon fra start

2. **Eller kontakt Cloudflare support:**
   - Dette kan være en midlertidig bug i UI

## Riktig konfigurasjon (alle felt tomme bortsett fra Path)

```
Build command: (tomt felt)
Deploy command: (tomt felt)
Non-production branch deploy command: (tomt felt)
Path: /
Build output directory: docs
```

**Husk:** "None" er tekst, ikke en tom verdi. Feltet må være helt tomt.

