"""Configuration for AI Capability Monitor."""

MODELS = [
    "Claude Opus 4.5",
    "ChatGPT (GPT-5)",
    "Gemini (2.5/3 Pro)",
    "Grok 3/4",
    "Llama 4",
    "DeepSeek (V3/R1)",
]

CAPABILITIES = {
    "Cognitive abilities": [
        "Reasoning",
        "Coding",
        "Memory (context)",
        "Multilingual / Norwegian",
    ],
    "Visual abilities": [
        "Image generation",
        "Image understanding",
        "Video generation",
        "Video understanding",
    ],
    "Audio & speech": [
        "Speech-to-text",
        "Text-to-speech",
        "Audio understanding",
        "Audio generation",
    ],
    "System abilities": [
        "Web search / browsing",
        "Document & PDF understanding",
        "File handling",
        "API calling",
        "Computer use",
    ],
    "Automation": [
        "Agents / autonomous actions",
        "Multi-step workflows",
        "Scheduling",
        "Tool use",
    ],
}

SEARCH_QUERIES = {
    "Claude Opus 4.5": [
        "Claude Opus 4.5 capabilities features 2025",
        "Anthropic Claude latest features",
    ],
    "ChatGPT (GPT-5)": [
        "ChatGPT GPT-5 capabilities 2025",
        "OpenAI GPT-5 features",
    ],
    "Gemini (2.5/3 Pro)": [
        "Gemini 2.5 Pro capabilities features 2025",
        "Google Gemini 3 Pro features",
    ],
    "Grok 3/4": [
        "Grok 3 xAI capabilities features 2025",
        "Grok 4 capabilities",
    ],
    "Llama 4": [
        "Llama 4 Meta capabilities features 2025",
        "Meta Llama 4 features",
    ],
    "DeepSeek (V3/R1)": [
        "DeepSeek V3 R1 capabilities features 2025",
        "DeepSeek latest model features",
    ],
}

BENCHMARK_SEARCHES = [
    "best AI model coding benchmark comparison 2025",
    "best AI image generation model 2025",
    "best AI video generation model 2025 Veo Sora",
    "AI model reasoning benchmark 2025",
    "AI model memory context window comparison 2025",
]

SYMBOLS = {
    "supported": "✔︎",
    "not_supported": "✗",
    "partial": "~",
    "best": "⭐",
}

