# Push til GitHub

## Steg 1: Opprett repo på GitHub

1. Gå til: https://github.com/new
2. Repository name: `ai-news-agent`
3. Description: `AI verktøy-radar basert på Hacker News, Reddit og Product Hunt`
4. Velg Public eller Private
5. **IKKE** huk av for README, .gitignore eller license
6. Klikk "Create repository"

## Steg 2: Push koden

Etter at repoet er opprettet, kjør:

```bash
cd /Users/carl/Desktop/FYRK/ai-news-agent

# Koble til GitHub (erstatt DITT_BRUKERNAVN)
git remote add origin https://github.com/DITT_BRUKERNAVN/ai-news-agent.git

# Push til GitHub
git push -u origin main
```

## Alternativ: Hvis du bruker SSH

```bash
git remote add origin git@github.com:DITT_BRUKERNAVN/ai-news-agent.git
git push -u origin main
```

## Verifisering

Etter push, sjekk at repoet er synlig på:
https://github.com/DITT_BRUKERNAVN/ai-news-agent

