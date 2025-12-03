# Cloudflare Pages Setup for ai-news-agent

## Problem
404-feil fordi siden ikke er deployet til Cloudflare Pages ennå.

## Løsning: Konfigurer Cloudflare Pages

### Steg 1: Koble GitHub-repoet til Cloudflare Pages

1. Gå til: https://dash.cloudflare.com
2. Klikk **"Pages"** i venstre meny
3. Klikk **"Create a project"**
4. Velg **"Connect to Git"**
5. Velg **"GitHub"** og autoriser Cloudflare til å aksessere GitHub
6. Velg repository: `carlfrankalbert/ai-news-agent`
7. Klikk **"Begin setup"**

### Steg 2: Konfigurer Build Settings

**Viktig:** Dette er et statisk HTML-prosjekt, så vi trenger IKKE build command.

1. **Project name:** `ai-news-agent` (eller hva du vil)
2. **Production branch:** `main`
3. **Build command:** **La stå TOM** (ingen build nødvendig)
4. **Build output directory:** `docs`
5. **Root directory:** `/` (root av repoet)

### Steg 3: Environment Variables (valgfritt)

Hvis du vil at workflow skal kjøre automatisk:
- Du trenger ikke environment variables her (de er i GitHub Actions)

### Steg 4: Deploy

1. Klikk **"Save and Deploy"**
2. Cloudflare vil nå:
   - Hente koden fra GitHub
   - Deploye `docs/` mappen
   - Gi deg en URL som `ai-news-agent.pages.dev`

### Steg 5: Legg til Custom Domain

1. Etter første deployment, gå til prosjektet
2. Klikk **"Custom domains"** tab
3. Klikk **"Set up a custom domain"**
4. Skriv: `fyrk.eu`
5. Klikk **"Continue"**
6. Cloudflare vil automatisk konfigurere DNS (hvis domenet er i samme konto)

### Steg 6: Verifiser

1. Gå til **Deployments** tab
2. Du skal se en deployment med status **"Success"**
3. Klikk på deployment for å se URL
4. Test at `https://fyrk.eu` fungerer

## Automatisk Deployment

Cloudflare Pages vil automatisk deploye når:
- Du pusher til `main` branch
- GitHub Actions workflow committer til `docs/` mappen

## Hvis det fortsatt ikke fungerer

### Sjekk 1: Er Pages-prosjektet opprettet?

1. Gå til Pages → Se om `ai-news-agent` prosjektet eksisterer
2. Hvis ikke, følg Steg 1-4 over

### Sjekk 2: Er `docs/index.html` i GitHub?

1. Gå til: https://github.com/carlfrankalbert/ai-news-agent/tree/main/docs
2. Sjekk at `index.html` eksisterer
3. Hvis ikke, push den til GitHub

### Sjekk 3: Er custom domain konfigurert?

1. Gå til Pages → ai-news-agent → Custom domains
2. Sjekk at `fyrk.eu` er lagt til
3. Status skal være **Active** (ikke Pending)

### Sjekk 4: Trigger manuell deployment

1. Gå til Pages → ai-news-agent → Deployments
2. Klikk **"Retry deployment"** på siste deployment
3. Eller push en liten endring til `main` branch

## Quick Test

Etter setup, test:
```bash
curl -I https://fyrk.eu
```

Du skal få `200 OK` i stedet for `404 Not Found`.

