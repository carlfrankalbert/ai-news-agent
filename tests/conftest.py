"""Pytest configuration and shared fixtures"""
import pytest
from datetime import datetime, timedelta
from pathlib import Path
import json


@pytest.fixture
def sample_hn_story():
    """Sample Hacker News story data (raw API format)"""
    return {
        "id": 123456,
        "title": "GPT-4 Released by OpenAI",
        "url": "https://openai.com/gpt4",
        "score": 500,
        "descendants": 200,
        "by": "testuser",
        "time": 1234567890
    }


@pytest.fixture
def sample_github_repo():
    """Sample GitHub repository data (raw API format)"""
    return {
        "id": 789012,
        "name": "llama-cpp",
        "html_url": "https://github.com/ggerganov/llama.cpp",
        "description": "Port of LLaMA model in C/C++",
        "stargazers_count": 50000,
        "language": "C++",
        "topics": ["llm", "ai", "machine-learning"],
        "owner": {
            "login": "ggerganov"
        },
        "created_at": "2023-03-10T12:00:00Z",
        "updated_at": "2024-01-15T14:30:00Z",
        "open_issues": 50,
        "closed_issues": 200
    }


@pytest.fixture
def sample_tools_data():
    """Sample data for multiple tools (for percentile calculations)"""
    return [
        {
            "name": "Tool A",
            "github": {"stars": 1000, "stars_30d_ago": 900, "open_issues": 10, "closed_issues": 90},
            "hn": {"mentions_count": 50},
            "reddit": {"mentions_count": 30}
        },
        {
            "name": "Tool B",
            "github": {"stars": 5000, "stars_30d_ago": 4500, "open_issues": 20, "closed_issues": 80},
            "hn": {"mentions_count": 100},
            "reddit": {"mentions_count": 60}
        },
        {
            "name": "Tool C",
            "github": {"stars": 10000, "stars_30d_ago": 9500, "open_issues": 5, "closed_issues": 95},
            "hn": {"mentions_count": 200},
            "reddit": {"mentions_count": 150}
        },
        {
            "name": "Tool D",
            "github": {"stars": 500, "stars_30d_ago": 450, "open_issues": 30, "closed_issues": 70},
            "hn": {"mentions_count": 10},
            "reddit": {"mentions_count": 5}
        }
    ]


@pytest.fixture
def sample_claude_response_valid():
    """Valid Claude response JSON"""
    return {
        "period": "2025-01",
        "generated_at": "2025-01-15T12:00:00",
        "data_source": "hackernews,github",
        "total_posts_analyzed": 100,
        "categories": [
            {
                "name": "Core LLMs",
                "slug": "core-llms",
                "top3": [
                    {
                        "rank": 1,
                        "medal": "gold",
                        "name": "GPT-4",
                        "provider": "OpenAI",
                        "short_reason": "Most discussed model",
                        "tags": ["chat", "reasoning"],
                        "scores": {
                            "buzz_momentum": 5,
                            "sentiment": 4,
                            "utility_for_knowledge_work": 5,
                            "price_performance": 3
                        },
                        "evidence": ["GPT-4 release announcement"]
                    },
                    {
                        "rank": 2,
                        "medal": "silver",
                        "name": "Claude",
                        "provider": "Anthropic",
                        "short_reason": "Strong performance",
                        "tags": ["chat", "coding"],
                        "scores": {
                            "buzz_momentum": 4,
                            "sentiment": 5,
                            "utility_for_knowledge_work": 5,
                            "price_performance": 4
                        },
                        "evidence": ["Claude Sonnet release"]
                    },
                    {
                        "rank": 3,
                        "medal": "bronze",
                        "name": "Gemini",
                        "provider": "Google",
                        "short_reason": "Good integration",
                        "tags": ["multimodal"],
                        "scores": {
                            "buzz_momentum": 3,
                            "sentiment": 3,
                            "utility_for_knowledge_work": 4,
                            "price_performance": 4
                        },
                        "evidence": ["Gemini Pro launch"]
                    }
                ]
            }
        ],
        "new_and_noteworthy": [
            {
                "name": "Mixtral",
                "provider": "Mistral AI",
                "category_hint": "core-llms",
                "short_reason": "Impressive open source model",
                "tags": ["open-source", "moe"]
            }
        ],
        "summary": "GPT-4 maintains dominance while open source alternatives gain traction"
    }


@pytest.fixture
def sample_claude_response_malformed():
    """Malformed Claude response (truncated JSON)"""
    return '''{
  "period": "2025-01",
  "generated_at": "2025-01-15T12:00:00",
  "data_source": "hackernews,github",
  "total_posts_analyzed": 100,
  "categories": [
    {
      "name": "Core LLMs",
      "slug": "core-llms",
      "top3": [
        {
          "rank": 1,
          "medal": "gold",
          "name": "GPT-4",
          "provider": "OpenAI",
          "short_reason": "Most discussed'''


@pytest.fixture
def sample_claude_response_with_markdown():
    """Claude response wrapped in markdown code blocks"""
    return '''Here's the analysis:

```json
{
  "period": "2025-01",
  "generated_at": "2025-01-15T12:00:00",
  "data_source": "hackernews,github",
  "total_posts_analyzed": 100,
  "categories": [
    {
      "name": "Core LLMs",
      "slug": "core-llms",
      "top3": [
        {
          "rank": 1,
          "medal": "gold",
          "name": "GPT-4",
          "provider": "OpenAI",
          "short_reason": "Most discussed model",
          "tags": ["chat"],
          "scores": {"buzz_momentum": 5, "sentiment": 4, "utility_for_knowledge_work": 5, "price_performance": 3},
          "evidence": ["GPT-4 release"]
        }
      ]
    }
  ],
  "new_and_noteworthy": [],
  "summary": "GPT-4 dominates"
}
```

That's the analysis.'''


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for tests"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
