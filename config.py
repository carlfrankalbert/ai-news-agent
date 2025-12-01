"""
Configuration for AI News Agent MVP
"""
from datetime import datetime, timedelta

# Hacker News API
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
HN_ALGOLIA_API = "https://hn.algolia.com/api/v1"

# Tidsperiode (90 dager default)
LOOKBACK_DAYS = 90

# Søkeord for å fange AI/LLM-relaterte posts
AI_KEYWORDS = [
    # Modeller
    "gpt-4", "gpt-5", "gpt4", "gpt5", "chatgpt",
    "claude", "anthropic", "sonnet", "opus", "haiku",
    "gemini", "bard", "google ai",
    "llama", "mistral", "mixtral", "qwen", "deepseek",
    "phi-3", "phi-4", "cohere", "command-r",
    
    # Konsepter
    "llm", "large language model", "foundation model",
    "ai agent", "ai agents", "agentic",
    "rag", "retrieval augmented",
    "fine-tuning", "fine tuning", "finetuning",
    "prompt engineering", "chain of thought",
    "multimodal", "vision model",
    
    # Verktøy og plattformer
    "openai", "huggingface", "hugging face",
    "langchain", "langgraph", "llamaindex",
    "ollama", "localai", "vllm",
    "cursor", "copilot", "github copilot",
    "perplexity", "you.com",
    "midjourney", "dall-e", "stable diffusion", "flux",
    "suno", "elevenlabs", "runway",
    
    # Open source / lokalt
    "open source llm", "local llm", "self-hosted",
    "gguf", "ggml", "quantization",
]

# Kategorier for output
CATEGORIES = [
    {
        "name": "Kjerne-LLM-er (Chat & reasoning)",
        "slug": "core-llms",
        "description": "Hovedmodeller for chat, reasoning og generelt kunnskapsarbeid",
        "examples": ["GPT-4", "Claude", "Gemini", "Llama", "Mistral"]
    },
    {
        "name": "Kode-assistenter",
        "slug": "code-assistants",
        "description": "Verktøy spesifikt for koding og utvikling",
        "examples": ["Cursor", "GitHub Copilot", "Codeium", "Tabnine"]
    },
    {
        "name": "Byggeklosser & plattform (API + open source)",
        "slug": "builder-platform",
        "description": "APIer, rammeverk og open source-verktøy for å bygge AI-løsninger",
        "examples": ["LangChain", "LlamaIndex", "Ollama", "vLLM", "HuggingFace"]
    },
    {
        "name": "Bilde & video-generering",
        "slug": "image-video",
        "description": "Generative verktøy for visuelt innhold",
        "examples": ["Midjourney", "DALL-E", "Stable Diffusion", "Runway", "Flux"]
    },
    {
        "name": "Lyd & tale",
        "slug": "audio-voice",
        "description": "Tale-til-tekst, tekst-til-tale, musikk",
        "examples": ["ElevenLabs", "Suno", "Whisper", "Bark"]
    },
    {
        "name": "AI-agenter & automatisering",
        "slug": "agents-automation",
        "description": "Autonome agenter og workflow-automatisering",
        "examples": ["AutoGPT", "CrewAI", "n8n AI", "Zapier AI"]
    },
]

# Minimum score/points for å inkludere en HN-post
MIN_HN_POINTS = 10

# Minimum upvotes for Reddit
MIN_REDDIT_UPVOTES = 10

# Minimum upvotes for Product Hunt
MIN_PH_UPVOTES = 10

# Output-konfig
OUTPUT_DIR = "output"
