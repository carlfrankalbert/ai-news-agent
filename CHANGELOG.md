# Changelog

## [Unreleased]

### Added
- **Reddit Collector**: Ny collector som samler AI-relaterte posts fra flere subreddits:
  - r/MachineLearning
  - r/LocalLLaMA
  - r/artificial
  - r/ChatGPT
  - r/OpenAI
  - r/singularity
  - r/agi
  - r/learnmachinelearning
- **Product Hunt Collector**: Grunnleggende struktur for å samle AI-verktøy fra Product Hunt
- **Multi-source collection**: `main.py` samler nå fra alle kilder parallelt
- **Deduplication**: Automatisk deduplicering basert på URL/title
- **Source tracking**: Hver post har nå `source`-felt som viser hvor den kom fra

### Changed
- `main.py` oppdatert til å bruke alle collectors
- `collectors/__init__.py` eksporterer nå alle collectors
- `config.py` har nye konfigurasjonsvalg for Reddit og Product Hunt

### Notes
- Product Hunt collector krever enten API key eller web scraping for full funksjonalitet
- Reddit collector bruker public API (ingen auth nødvendig)
- Alle collectors følger samme interface for enkel utvidelse

