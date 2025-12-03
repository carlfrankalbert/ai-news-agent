# SSL-fiksing for fyrk.eu

## Problem
`ERR_SSL_VERSION_OR_CIPHER_MISMATCH` - SSL-sertifikatet er ikke riktig konfigurert.

## Løsning: Aktiver SSL i Cloudflare

### Steg 1: Sjekk SSL/TLS-innstillinger

1. Gå til: https://dash.cloudflare.com
2. Velg domenet `fyrk.eu`
3. Klikk på **"SSL/TLS"** i venstre meny

### Steg 2: Sett SSL/TLS-modus

Du skal se en oversikt over SSL/TLS-innstillinger. Sjekk følgende:

1. **SSL/TLS encryption mode:**
   - Sett til **"Full"** eller **"Full (strict)"**
   - **Full (strict)** er best hvis Cloudflare Pages støtter det
   - **Full** er minimum for å få HTTPS til å fungere

2. **Always Use HTTPS:**
   - Aktiver denne (slå på)
   - Dette omdirigerer all HTTP-trafikk til HTTPS

### Steg 3: Sjekk Custom Domain i Pages

1. Gå til: **Pages → ai-news-agent → Custom domains**
2. Sjekk at `fyrk.eu` er listet
3. Status skal være:
   - ✅ **Active** (når alt er klart)
   - ⏳ **Pending** (venter på SSL-generering)

### Steg 4: Vent på SSL-generering

- Cloudflare genererer SSL-sertifikat automatisk
- Dette tar vanligvis **5-30 minutter** etter at DNS er riktig
- Hvis du nettopp la til domenet, kan det ta opptil **24 timer**

### Steg 5: Verifiser

Etter noen minutter:
1. Prøv å besøke `https://fyrk.eu` igjen
2. Sjekk at det er en grønn lås i nettleseren
3. Sjekk at `docs/index.html` vises

## Troubleshooting

### Hvis SSL fortsatt ikke fungerer etter 30 minutter:

1. **Sjekk SSL/TLS-modus:**
   - Gå til SSL/TLS → Overview
   - Endre modus til "Full" hvis den er satt til "Flexible"
   - "Flexible" fungerer ikke med Cloudflare Pages

2. **Sjekk Edge Certificates:**
   - Gå til SSL/TLS → Edge Certificates
   - Se at "Always Use HTTPS" er aktivert
   - Se at "Automatic HTTPS Rewrites" er aktivert

3. **Sjekk DNS:**
   - Gå til DNS
   - Verifiser at CNAME-record for `fyrk.eu` peker til Pages-URL
   - Proxy-status skal være **Proxied** (orange sky)

4. **Purge Cloudflare Cache:**
   - Gå til Caching → Configuration
   - Klikk "Purge Everything"
   - Dette kan hjelpe hvis det er cache-problemer

5. **Redeploy Pages:**
   - Gå til Pages → ai-news-agent → Deployments
   - Klikk på tre prikker ved siste deployment
   - Velg "Retry deployment"

## Hvis ingenting fungerer

1. **Fjern og legg til custom domain igjen:**
   - Pages → Custom domains → Fjern `fyrk.eu`
   - Vent 5 minutter
   - Legg til `fyrk.eu` igjen

2. **Sjekk at Pages-prosjektet er deployet:**
   - Gå til Pages → ai-news-agent
   - Se at det finnes en vellykket deployment
   - Hvis ikke, trigger en ny deployment

## Status-sjekk

Etter at du har endret SSL/TLS-modus:
- Vent 5-10 minutter
- Prøv `https://fyrk.eu` igjen
- SSL-sertifikatet skal nå være generert

