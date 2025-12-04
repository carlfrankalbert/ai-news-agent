# Datakilder - AI News Agent

Dette dokumentet beskriver alle datakilder som brukes for å samle inn AI-relaterte verktøy og diskusjoner.

## Aktive datakilder

### 1. Hacker News
- **API**: Firebase API (gratis, ingen autentisering)
- **URL**: `https://hacker-news.firebaseio.com/v0`
- **Hva vi samler**: AI-relaterte posts fra topstories, beststories og newstories
- **Filtrering**: Minimum 10 poeng, AI-keywords i tittel/URL
- **Rate limit**: Ingen offisiell limit, men vi respekterer API-et

### 2. GitHub Trending
- **API**: GitHub Search API (gratis med token, begrenset uten)
- **URL**: `https://api.github.com/search/repositories`
- **Hva vi samler**: AI-relaterte repositories som er oppdatert nylig
- **Filtrering**: Minimum 10 stars, AI-keywords i navn/beskrivelse/topics
- **Rate limit**: 60 req/time uten token, 5000 req/time med token
- **Miljøvariabel**: `GITHUB_TOKEN` (valgfri, men anbefalt)

### 3. Reddit
- **API**: Public JSON API (gratis, ingen autentisering)
- **URL**: `https://www.reddit.com`
- **Hva vi samler**: AI-relaterte posts fra relevante subreddits
- **Subreddits**: MachineLearning, artificial, LocalLLaMA, OpenAI, singularity, ChatGPT, StableDiffusion, comfyui, programming, technology, Futurology, og flere
- **Filtrering**: Minimum 5 poeng, AI-keywords i tittel/tekst
- **Rate limit**: 60 requests per minutt (respekteres automatisk)

### 4. X/Twitter
- **API**: Twitter API v2 (krever autentisering)
- **URL**: `https://api.twitter.com/2`
- **Hva vi samler**: AI-relaterte tweets med høy engagement
- **Filtrering**: Minimum 10 engagement (likes + retweets + replies), AI-keywords
- **Rate limit**: 300 requests per 15 minutter
- **Miljøvariabel**: `TWITTER_BEARER_TOKEN` (påkrevd for å aktivere)

## Konfigurasjon

### Miljøvariabler

Opprett en `.env` fil i prosjektroten:

```bash
# GitHub (valgfri, men anbefalt for høyere rate limit)
GITHUB_TOKEN=your_github_token_here

# Twitter (påkrevd for Twitter-innsamling)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Anthropic (påkrevd for analyse)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Hvordan få API-nøkler

#### GitHub Token
1. Gå til https://github.com/settings/tokens
2. Klikk "Generate new token (classic)"
3. Velg scope: `public_repo` (eller ingen scopes for read-only)
4. Kopier tokenet til `.env` filen

#### Twitter Bearer Token
1. Gå til https://developer.twitter.com/en/portal/dashboard
2. Opprett en ny app eller bruk eksisterende
3. Gå til "Keys and tokens"
4. Generer en "Bearer Token"
5. Kopier tokenet til `.env` filen

**Merk**: Twitter API v2 Basic (gratis tier) har begrensninger:
- 10,000 tweets per måned
- 300 requests per 15 minutter
- Kun "recent search" (siste 7 dager)

## Bruk

### Aktivere alle datakilder

Alle datakilder aktiveres automatisk når du kjører:

```bash
python main.py
```

Hvis `TWITTER_BEARER_TOKEN` ikke er satt, hopper systemet over Twitter-innsamling og fortsetter med de andre kildene.

### Teste enkelte datakilder

Du kan teste hver datakilde individuelt:

```bash
# Test Reddit
python -m src.ai_news_agent.collectors.reddit

# Test Twitter (krever TWITTER_BEARER_TOKEN)
python -m src.ai_news_agent.collectors.twitter
```

## Dataformat

Alle datakilder returnerer data i samme format:

```json
{
  "id": "source-unique-id",
  "title": "Post title or tweet text",
  "url": "Original URL",
  "points": 100,
  "num_comments": 50,
  "author": "username",
  "created_at": "2025-12-01T10:00:00",
  "source": "hackernews|github|reddit|twitter"
}
```

## Feilhåndtering

Systemet håndterer feil gracefully:
- Hvis en datakilde feiler, fortsetter systemet med de andre
- Rate limits respekteres automatisk
- Manglende API-nøkler gir advarsler, men stopper ikke kjøringen

## Ytelse

Typisk kjøretid for full innsamling:
- Hacker News: ~30-60 sekunder
- GitHub: ~1-2 minutter
- Reddit: ~2-5 minutter (avhengig av antall subreddits)
- Twitter: ~3-5 minutter (avhengig av rate limits)

**Totalt**: ~5-10 minutter for full innsamling fra alle kilder.

