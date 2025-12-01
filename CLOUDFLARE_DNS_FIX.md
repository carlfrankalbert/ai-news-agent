# Cloudflare DNS Fix for fyrk.eu

## Problem
Error 1001: DNS resolution error - Cloudflare kan ikke løse opp `fyrk.eu`

## Løsning: Konfigurer DNS i Cloudflare

### Steg 1: Sjekk at domenet er lagt til i Cloudflare

1. Gå til: https://dash.cloudflare.com
2. Sjekk at `fyrk.eu` er i listen over domener
3. Hvis ikke, legg det til:
   - Klikk "Add a site"
   - Skriv `fyrk.eu`
   - Følg instruksjonene for å verifisere domenet

### Steg 2: Konfigurer DNS Records i Cloudflare

1. Gå til ditt `fyrk.eu` domene i Cloudflare Dashboard
2. Klikk på **"DNS"** i venstre meny
3. Sjekk om det finnes eksisterende records

### Steg 3: Legg til DNS Records for Cloudflare Pages

**For Cloudflare Pages må du legge til en CNAME record:**

1. Klikk **"Add record"**
2. Konfigurer:
   - **Type:** `CNAME`
   - **Name:** `@` (eller la stå tomt for root domain)
   - **Target:** `<your-pages-project>.pages.dev`
     - Finn dette i Cloudflare Pages → ditt prosjekt → Custom domains
     - Eksempel: `ai-news-agent.pages.dev`
   - **Proxy status:** 🟠 Proxied (anbefalt - gir DDoS-beskyttelse)
   - **TTL:** Auto
3. Klikk **"Save"**

### Steg 4: Konfigurer Custom Domain i Cloudflare Pages

1. Gå til: **Cloudflare Dashboard → Pages → ditt prosjekt**
2. Klikk på **"Custom domains"** tab
3. Klikk **"Set up a custom domain"**
4. Skriv inn: `fyrk.eu`
5. Klikk **"Continue"**
6. Cloudflare vil automatisk konfigurere DNS (hvis domenet er i samme Cloudflare-konto)

### Steg 5: Vent på DNS Propagation

- DNS endringer kan ta **5-30 minutter** å propagere i Cloudflare
- Hvis domenet nettopp ble lagt til, kan det ta noen minutter ekstra

### Steg 6: Verifiser

1. Gå tilbake til **Pages → Custom domains**
2. Du skal se `fyrk.eu` med status:
   - ✅ **Active** (når alt er klart)
   - ⏳ **Pending** (venter på DNS propagation)

## Troubleshooting

### Hvis DNS fortsatt ikke fungerer:

1. **Sjekk at domenet er i Cloudflare:**
   - Gå til Dashboard → se om `fyrk.eu` er i listen
   - Hvis ikke, legg det til først

2. **Sjekk DNS records:**
   - Gå til DNS → se at CNAME record eksisterer
   - Verifiser at Target peker til riktig Pages URL

3. **Sjekk Pages-konfigurasjon:**
   - Gå til Pages → ditt prosjekt → Custom domains
   - Se at `fyrk.eu` er lagt til
   - Sjekk eventuelle feilmeldinger

4. **Sjekk at Pages-prosjektet er deployet:**
   - Gå til Pages → ditt prosjekt → Deployments
   - Se at det finnes en vellykket deployment

### Hvis domenet er kjøpt fra annen registrar:

Hvis `fyrk.eu` er kjøpt fra en annen registrar (ikke Cloudflare), må du:

1. **Endre nameservers hos din registrar:**
   - Cloudflare vil gi deg nameservers når du legger til domenet
   - Eksempel: `lola.ns.cloudflare.com` og `milo.ns.cloudflare.com`
   - Gå til din registrar (hvor du kjøpte domenet) og endre nameservers

2. **Vent på nameserver propagation:**
   - Dette kan ta opptil 24-48 timer
   - Vanligvis tar det 1-4 timer

## Quick Check

Test om DNS er riktig konfigurert:

```bash
# Sjekk DNS records
dig fyrk.eu CNAME

# Eller
nslookup fyrk.eu
```

Du skal se at `fyrk.eu` peker til din Cloudflare Pages URL.

