# Cloudflare Pages Setup - fyrk.eu

## Oversikt

AI News Agent er deployet til Cloudflare Pages på domenet **fyrk.eu**.

## Deployment Flow

1. **GitHub Actions** kjører daglig (06:00 UTC)
2. Agent samler data fra Hacker News, Reddit, Product Hunt
3. Claude analyserer og rangerer verktøyene
4. HTML-generator lager `docs/index.html`
5. Endringer committes og pushes til GitHub
6. **Cloudflare Pages** deployer automatisk fra `main` branch, `docs/` mappe

## Cloudflare Pages Konfigurasjon

### Build Settings

- **Build command:** (tom - statisk site)
- **Build output directory:** `docs`
- **Root directory:** `/` (root av repoet)

### Environment Variables

Hvis du trenger environment variables i Cloudflare:
- Gå til Cloudflare Dashboard → Pages → ditt prosjekt → Settings → Environment Variables
- Legg til: `ANTHROPIC_API_KEY` (hvis nødvendig for frontend)

**Merk:** API-nøkkelen brukes kun i GitHub Actions, ikke i frontend.

## Custom Domain

Domenet `fyrk.eu` er satt opp via Cloudflare Pages:
- Gå til Cloudflare Dashboard → Pages → ditt prosjekt → Custom domains
- Verifiser at `fyrk.eu` er konfigurert

## Verifisering

Etter deployment, sjekk:
- https://fyrk.eu - skal vise AI Verktøy Radar
- https://github.com/carlfrankalbert/ai-news-agent/actions - sjekk at workflows kjører

## Oppdatering av HTML

HTML-generatoren (`generate_html.py`) lager statisk HTML i `docs/` mappen. 
Cloudflare Pages deployer automatisk når filene i `docs/` oppdateres.

## Troubleshooting

### Siden viser ikke oppdatert innhold
- Sjekk at GitHub Actions workflow har kjørt og pushet endringer
- Sjekk Cloudflare Pages deployment logs
- Vent noen minutter (Cloudflare kan ha cache)

### Build feiler
- Sjekk at `docs/index.html` eksisterer
- Verifiser at GitHub Actions har generert HTML

### Custom domain fungerer ikke
- Sjekk DNS-innstillinger i Cloudflare
- Verifiser at SSL/TLS er aktivert

