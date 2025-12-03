# 🔒 Security - API Key Protection

## ✅ API Key er nå sikret

API-nøkkelen din er lagret i `.env` filen som er **ikke er commitet til Git**.

## Hvordan det fungerer

1. **`.env` fil** - Lagret lokalt, ikke i Git (`.gitignore`)
2. **`python-dotenv`** - Laster automatisk `.env` når du kjører `main.py`
3. **GitHub Secrets** - For CI/CD workflows (allerede konfigurert)

## Bruk

### Lokalt
API-nøkkelen lastes automatisk fra `.env`:
```bash
python main.py --days 30
```

### GitHub Actions
Bruker GitHub Secret (allerede satt opp i workflow).

## Viktig: Hvis du pusher til GitHub

1. **Sjekk at `.env` ikke er commitet:**
   ```bash
   git status .env
   # Skal vise: "nothing to commit" eller "untracked"
   ```

2. **Hvis `.env` er i Git (feil):**
   ```bash
   git rm --cached .env
   git commit -m "Remove .env from tracking"
   ```

3. **Legg til API key som GitHub Secret:**
   - Gå til: https://github.com/carlfrankalbert/ai-news-agent/settings/secrets/actions
   - Legg til `ANTHROPIC_API_KEY` hvis ikke allerede gjort

## Verifisering

```bash
# Sjekk at .env er ignorert
git check-ignore .env
# Skal outputte: .env

# Test at API key lastes
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Key loaded:', bool(os.getenv('ANTHROPIC_API_KEY')))"
```

## Hvis nøkkelen er eksponert

1. **Umiddelbart:** Gå til Anthropic Console og revoke nøkkelen
2. **Generer ny nøkkel**
3. **Oppdater `.env` filen**
4. **Oppdater GitHub Secret** (hvis nødvendig)

