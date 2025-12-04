"""Fetch latest capability information using Claude API with web search."""

import os
from anthropic import Anthropic
from typing import Dict, List
from .config import MODELS, SEARCH_QUERIES, BENCHMARK_SEARCHES, CAPABILITIES


class CapabilityFetcher:
    """Fetches latest AI model capabilities using Claude API."""

    def __init__(self, api_key: str = None):
        """Initialize fetcher with API key."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=self.api_key)

    def fetch_model_capabilities(self, model: str) -> Dict:
        """
        Fetch capabilities for a specific model.
        
        Args:
            model: Model name to fetch capabilities for
            
        Returns:
            Dictionary with capability information
        """
        queries = SEARCH_QUERIES.get(model, [f"{model} capabilities 2025"])
        
        search_query = " OR ".join([f'"{q}"' for q in queries])
        
        prompt = f"""Search the web for the latest capabilities of {model}.

Search queries to use: {search_query}

Check these sources:
- Official blogs (openai.com, anthropic.com, blog.google, ai.meta.com, x.ai)
- Wikipedia pages
- Benchmark leaderboards (artificialanalysis.ai, lmarena.ai, livebench.ai)

For each capability category, determine if {model} supports it:
- ✔︎ = Fully supported
- ✗ = Not supported
- ~ = Partial support

Return a JSON object with this structure:
{{
    "model": "{model}",
    "capabilities": {{
        "Cognitive abilities": {{
            "Reasoning": "✔︎|✗|~",
            "Coding": "✔︎|✗|~",
            "Memory (context)": "✔︎|✗|~",
            "Multilingual / Norwegian": "✔︎|✗|~"
        }},
        "Visual abilities": {{
            "Image generation": "✔︎|✗|~",
            "Image understanding": "✔︎|✗|~",
            "Video generation": "✔︎|✗|~",
            "Video understanding": "✔︎|✗|~"
        }},
        "Audio & speech": {{
            "Speech-to-text": "✔︎|✗|~",
            "Text-to-speech": "✔︎|✗|~",
            "Audio understanding": "✔︎|✗|~",
            "Audio generation": "✔︎|✗|~"
        }},
        "System abilities": {{
            "Web search / browsing": "✔︎|✗|~",
            "Document & PDF understanding": "✔︎|✗|~",
            "File handling": "✔︎|✗|~",
            "API calling": "✔︎|✗|~",
            "Computer use": "✔︎|✗|~"
        }},
        "Automation": {{
            "Agents / autonomous actions": "✔︎|✗|~",
            "Multi-step workflows": "✔︎|✗|~",
            "Scheduling": "✔︎|✗|~",
            "Tool use": "✔︎|✗|~"
        }}
    }},
    "sources": ["list of sources checked"],
    "last_updated": "YYYY-MM-DD"
}}

Be thorough and accurate. Only mark capabilities as supported if you find clear evidence."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            # Extract JSON from response (may be wrapped in markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            import json
            return json.loads(content)
        except Exception as e:
            print(f"Error fetching capabilities for {model}: {e}")
            return None

    def fetch_benchmark_results(self) -> Dict[str, str]:
        """
        Fetch benchmark results to determine best-in-category models.
        
        Returns:
            Dictionary mapping capability to best model
        """
        search_query = " OR ".join([f'"{q}"' for q in BENCHMARK_SEARCHES])
        
        prompt = f"""Search the web for latest AI model benchmark results and comparisons.

Search queries: {search_query}

Check these benchmark sources:
- artificialanalysis.ai
- lmarena.ai
- livebench.ai
- Official benchmark reports

For each capability, determine which model is BEST IN CATEGORY (only one ⭐ per capability):
- Reasoning
- Coding
- Memory (context)
- Image generation
- Image understanding
- Video generation
- Video understanding

Return a JSON object mapping each capability to the best model:
{{
    "Reasoning": "Model Name or null",
    "Coding": "Model Name or null",
    "Memory (context)": "Model Name or null",
    "Image generation": "Model Name or null",
    "Image understanding": "Model Name or null",
    "Video generation": "Model Name or null",
    "Video understanding": "Model Name or null"
}}

Only assign ⭐ where there's clear benchmark evidence of superiority. If unclear, use null."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            import json
            return json.loads(content)
        except Exception as e:
            print(f"Error fetching benchmark results: {e}")
            return {}

    def fetch_all_capabilities(self) -> Dict[str, Dict]:
        """
        Fetch capabilities for all models.
        
        Returns:
            Dictionary mapping model names to their capabilities
        """
        results = {}
        for model in MODELS:
            print(f"Fetching capabilities for {model}...")
            capabilities = self.fetch_model_capabilities(model)
            if capabilities:
                results[model] = capabilities
            else:
                print(f"Warning: Failed to fetch capabilities for {model}")
        return results

