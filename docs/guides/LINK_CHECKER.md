# Link Checker Agent

En automatisk agent som sjekker gyldigheten av alle lenker (logoer og nettsteder) i `PROVIDER_INFO` en gang per dag.

## Hva den gjør

Link checker agenten:
- ✅ Sjekker alle logo-URLer i `PROVIDER_INFO`
- ✅ Sjekker alle nettsteds-URLer i `PROVIDER_INFO`
- ✅ Genererer en detaljert rapport med resultater
- ✅ Oppretter GitHub Issues hvis døde lenker oppdages
- ✅ Kjører automatisk daglig via GitHub Actions

## Kjøre lokalt

```bash
# Installer avhengigheter
pip install -r requirements.txt

# Kjør link checker
python check_links.py
```

## Rapportformat

Rapporten lagres i `output/link_check_report.json` og inneholder:

```json
{
  "timestamp": "2025-12-02T12:00:00",
  "summary": {
    "total_providers": 50,
    "total_links": 100,
    "valid_links": 98,
    "invalid_links": 2,
    "all_valid": false
  },
  "invalid_links": [
    {
      "provider": "Example Provider",
      "type": "logo",
      "url": "https://example.com/favicon.ico",
      "status": 404,
      "error": "HTTP 404"
    }
  ],
  "detailed_results": [...]
}
```

## GitHub Actions

Workflowen kjører automatisk:
- **Schedule:** Daglig klokken 02:00 UTC
- **Manual trigger:** Kan også kjøres manuelt via `workflow_dispatch`

Hvis døde lenker oppdages:
1. Workflowen feiler (men fortsetter)
2. En rapport lastes opp som artifact
3. Et GitHub Issue opprettes automatisk med detaljer om døde lenker

## Feilsøking

### ImportError
Hvis du får import-feil lokalt, sørg for at du er i prosjektets rotmappe og at `src/` er i Python-path.

### Timeout-feil
Noen sider kan være trege eller blokkere automatiserte requests. Link checker bruker:
- 10 sekunder timeout per request
- User-Agent header for å unngå blokkering
- Følger redirects automatisk

### Rate limiting
Link checker begrenser til 10 samtidige requests for å unngå rate limiting.

