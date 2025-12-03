# Fikse Cloudflare Pages Build-konfigurasjon

## Problem
Build feiler fordi deploy command er feil konfigurert.

## Løsning: Fjern deploy command

### Steg 1: Endre Build-konfigurasjon

1. Gå til: Cloudflare Dashboard → Pages → ai-news-agent → Settings → Builds & deployments
2. Klikk på **edit-ikonet** ved "Build configuration"
3. Endre følgende:

**FJERN disse:**
- ❌ **Deploy command:** `npx wrangler deploy` → **La stå TOM**
- ❌ **Version command:** `npx wrangler versions upload` → **La stå TOM**

**BEHOLD disse:**
- ✅ **Build command:** `None` (eller tom)
- ✅ **Root directory:** `/`
- ✅ **Build output directory:** `docs`

### Steg 2: Lagre og redeploy

1. Klikk **"Save"**
2. Gå til **Deployments** tab
3. Klikk **"Retry deployment"** på siste deployment
4. Eller push en liten endring til `main` branch for å trigge ny deployment

## Riktig konfigurasjon for statisk HTML

For et statisk HTML-prosjekt (som dette) skal konfigurasjonen være:

```
Build command: (tom)
Deploy command: (tom)
Version command: (tom)
Root directory: /
Build output directory: docs
```

**Forklaring:**
- `wrangler` er for Cloudflare Workers, ikke Pages
- Pages deployer automatisk fra output directory
- Ingen build eller deploy commands nødvendig

## Verifisering

Etter retry:
1. Gå til Deployments tab
2. Sjekk at siste deployment har status **"Success"** (grønn)
3. Test `https://fyrk.eu` - skal nå fungere

## Hvis det fortsatt feiler

1. **Sjekk build logs:**
   - Klikk på deployment → se build logs
   - Se etter feilmeldinger

2. **Sjekk at `docs/index.html` eksisterer:**
   - Gå til GitHub: https://github.com/carlfrankalbert/ai-news-agent/tree/main/docs
   - Verifiser at `index.html` er der

3. **Clear build cache:**
   - Settings → Builds & deployments → Build cache → Clear Cache
   - Prøv deploy igjen

