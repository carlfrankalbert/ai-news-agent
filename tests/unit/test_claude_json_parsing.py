"""
Unit tests for Claude JSON parsing and error recovery
Tests the analyze_with_claude function and its JSON parsing strategies
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from src.ai_news_agent.analyzer.analyzer import (
    analyze_with_claude,
    validate_rankings,
    create_analysis_prompt
)


class TestAnalyzeWithClaude:
    """Test Claude API integration and JSON parsing"""

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_valid_json(self, mock_anthropic, sample_claude_response_valid):
        """Test successful parsing of valid JSON response"""
        # Mock the Anthropic client
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Mock the API response
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=json.dumps(sample_claude_response_valid))]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        # Test data
        posts = [
            {"title": "GPT-4 released", "points": 500, "num_comments": 200, "source": "hackernews"}
        ]

        result = analyze_with_claude(posts, "2025-01")

        # Should parse successfully
        assert "categories" in result
        assert len(result["categories"]) > 0
        assert result["period"] == "2025-01"

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_markdown_wrapped_json(
        self,
        mock_anthropic,
        sample_claude_response_with_markdown
    ):
        """Test parsing JSON wrapped in markdown code blocks"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=sample_claude_response_with_markdown)]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should successfully extract JSON from markdown
        assert "categories" in result
        assert result["period"] == "2025-01"

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_truncated_response(self, mock_anthropic):
        """Test handling of truncated response (max_tokens reached)"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Incomplete JSON
        truncated_json = '{"period": "2025-01", "categories": ['

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=truncated_json)]
        mock_message.stop_reason = "max_tokens"  # Indicates truncation
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should return error structure
        assert "error" in result or "categories" in result
        # If it has categories, they should be empty due to parse failure
        if "categories" in result:
            assert isinstance(result["categories"], list)

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_json_with_trailing_commas(self, mock_anthropic):
        """Test parsing JSON with trailing commas (common error)"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # JSON with trailing commas (invalid JSON but common)
        json_with_trailing_commas = '''{
  "period": "2025-01",
  "generated_at": "2025-01-15T12:00:00",
  "data_source": "hackernews,github",
  "total_posts_analyzed": 100,
  "categories": [
    {
      "name": "Test",
      "slug": "test",
      "top3": [],
    },
  ],
  "new_and_noteworthy": [],
  "summary": "Test summary",
}'''

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=json_with_trailing_commas)]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should use Strategy 3 to fix trailing commas
        assert "categories" in result
        assert result["period"] == "2025-01"

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_nested_json_in_text(self, mock_anthropic):
        """Test extracting JSON from surrounded by other text"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        response_with_extra_text = '''Here is my analysis of the AI tools:

{
  "period": "2025-01",
  "generated_at": "2025-01-15T12:00:00",
  "data_source": "hackernews,github",
  "total_posts_analyzed": 50,
  "categories": [],
  "new_and_noteworthy": [],
  "summary": "Test"
}

Hope this helps!'''

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=response_with_extra_text)]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should extract JSON using brace counting (Strategy 2)
        assert "categories" in result
        assert result["period"] == "2025-01"

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_completely_invalid_response(self, mock_anthropic):
        """Test handling completely invalid response"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="This is not JSON at all!")]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should return error structure
        assert "error" in result
        assert "categories" in result
        assert result["categories"] == []  # Empty categories as fallback

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_empty_response(self, mock_anthropic):
        """Test handling empty response"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="")]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should return error structure
        assert "error" in result or "categories" in result

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_multiple_json_objects(self, mock_anthropic):
        """Test extracting first complete JSON object from multiple objects"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        # Two JSON objects - should extract first complete one
        response = '''{
  "period": "2025-01",
  "generated_at": "2025-01-15T12:00:00",
  "data_source": "hackernews",
  "total_posts_analyzed": 50,
  "categories": [],
  "new_and_noteworthy": [],
  "summary": "First object"
}
{
  "period": "2025-02",
  "summary": "Second object"
}'''

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=response)]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should extract the first complete JSON object
        assert result["period"] == "2025-01"
        assert result["summary"] == "First object"

    @patch('src.ai_news_agent.analyzer.analyzer.Anthropic')
    def test_analyze_with_claude_json_with_escaped_quotes(self, mock_anthropic):
        """Test parsing JSON with escaped quotes in strings"""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        json_with_escapes = '''{
  "period": "2025-01",
  "generated_at": "2025-01-15T12:00:00",
  "data_source": "hackernews,github",
  "total_posts_analyzed": 10,
  "categories": [],
  "new_and_noteworthy": [],
  "summary": "Claude said \\"this is great\\""
}'''

        mock_message = MagicMock()
        mock_message.content = [MagicMock(text=json_with_escapes)]
        mock_message.stop_reason = "end_turn"
        mock_client.messages.create.return_value = mock_message

        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        result = analyze_with_claude(posts, "2025-01")

        # Should parse correctly
        assert result["period"] == "2025-01"
        assert "this is great" in result["summary"]


class TestValidateRankings:
    """Test rankings validation logic"""

    def test_validate_rankings_valid(self, sample_claude_response_valid):
        """Test validation of valid rankings"""
        is_valid, issues = validate_rankings(sample_claude_response_valid)

        assert is_valid is True
        assert len(issues) == 0

    def test_validate_rankings_missing_categories(self):
        """Test validation catches missing categories"""
        invalid_rankings = {
            "period": "2025-01",
            "summary": "Test"
            # Missing categories
        }

        is_valid, issues = validate_rankings(invalid_rankings)

        assert is_valid is False
        assert len(issues) > 0
        assert any("categories" in issue.lower() for issue in issues)

    def test_validate_rankings_missing_top3(self):
        """Test validation catches missing top3 in category"""
        invalid_rankings = {
            "categories": [
                {
                    "name": "Test Category",
                    "slug": "test"
                    # Missing top3
                }
            ]
        }

        is_valid, issues = validate_rankings(invalid_rankings)

        assert is_valid is False
        assert len(issues) > 0

    def test_validate_rankings_insufficient_top3(self):
        """Test validation catches fewer than 3 items in top3"""
        invalid_rankings = {
            "categories": [
                {
                    "name": "Test Category",
                    "slug": "test",
                    "top3": [
                        {"name": "Tool 1", "short_reason": "Good"},
                        {"name": "Tool 2", "short_reason": "Better"}
                        # Only 2 items, should have 3
                    ]
                }
            ]
        }

        is_valid, issues = validate_rankings(invalid_rankings)

        assert is_valid is False
        assert len(issues) > 0
        assert any("færre enn 3" in issue.lower() or "fewer than 3" in issue.lower() for issue in issues)

    def test_validate_rankings_missing_name(self):
        """Test validation catches missing name in ranking"""
        invalid_rankings = {
            "categories": [
                {
                    "name": "Test Category",
                    "slug": "test",
                    "top3": [
                        {"short_reason": "Good"},  # Missing name
                        {"name": "Tool 2", "short_reason": "Better"},
                        {"name": "Tool 3", "short_reason": "Best"}
                    ]
                }
            ]
        }

        is_valid, issues = validate_rankings(invalid_rankings)

        assert is_valid is False
        assert len(issues) > 0

    def test_validate_rankings_missing_reason(self):
        """Test validation catches missing short_reason"""
        invalid_rankings = {
            "categories": [
                {
                    "name": "Test Category",
                    "slug": "test",
                    "top3": [
                        {"name": "Tool 1"},  # Missing short_reason
                        {"name": "Tool 2", "short_reason": "Better"},
                        {"name": "Tool 3", "short_reason": "Best"}
                    ]
                }
            ]
        }

        is_valid, issues = validate_rankings(invalid_rankings)

        assert is_valid is False
        assert len(issues) > 0

    def test_validate_rankings_empty_categories(self):
        """Test validation of empty categories array"""
        rankings = {
            "categories": []
        }

        # Empty categories is technically valid structure-wise
        is_valid, issues = validate_rankings(rankings)

        # Should be valid (no structural issues)
        assert is_valid is True

    def test_validate_rankings_multiple_categories(self):
        """Test validation with multiple valid categories"""
        rankings = {
            "categories": [
                {
                    "name": "Category 1",
                    "slug": "cat1",
                    "top3": [
                        {"name": "Tool 1", "short_reason": "Good"},
                        {"name": "Tool 2", "short_reason": "Better"},
                        {"name": "Tool 3", "short_reason": "Best"}
                    ]
                },
                {
                    "name": "Category 2",
                    "slug": "cat2",
                    "top3": [
                        {"name": "Tool A", "short_reason": "Good"},
                        {"name": "Tool B", "short_reason": "Better"},
                        {"name": "Tool C", "short_reason": "Best"}
                    ]
                }
            ]
        }

        is_valid, issues = validate_rankings(rankings)

        assert is_valid is True
        assert len(issues) == 0


class TestCreateAnalysisPrompt:
    """Test prompt creation for Claude"""

    def test_create_analysis_prompt_basic(self):
        """Test basic prompt creation"""
        posts = [
            {
                "title": "GPT-4 released",
                "points": 500,
                "num_comments": 200,
                "source": "hackernews"
            }
        ]

        prompt = create_analysis_prompt(posts, "2025-01")

        # Should include key elements
        assert "2025-01" in prompt
        assert "GPT-4 released" in prompt
        assert "500 pts" in prompt
        assert "200 comments" in prompt

    def test_create_analysis_prompt_source_counts(self):
        """Test that prompt includes source counts"""
        posts = [
            {"title": "Test 1", "points": 100, "num_comments": 10, "source": "hackernews"},
            {"title": "Test 2", "points": 200, "num_comments": 20, "source": "hackernews"},
            {"title": "Test 3", "points": 300, "num_comments": 0, "source": "github"}
        ]

        prompt = create_analysis_prompt(posts, "2025-01")

        # Should show counts: 2 HN, 1 GitHub
        assert "Hacker News: 2" in prompt or "2 posts" in prompt
        assert "GitHub" in prompt

    def test_create_analysis_prompt_limits_posts(self):
        """Test that prompt limits number of posts to avoid context overflow"""
        # Create 300 posts
        posts = [
            {
                "title": f"Test post {i}",
                "points": i,
                "num_comments": i,
                "source": "hackernews"
            }
            for i in range(300)
        ]

        prompt = create_analysis_prompt(posts, "2025-01")

        # Should only include first 200 posts
        assert "Test post 199" in prompt or "Test post 150" in prompt
        assert "Test post 250" not in prompt  # Should not include posts beyond limit

    def test_create_analysis_prompt_includes_categories(self):
        """Test that prompt includes category descriptions"""
        posts = [{"title": "Test", "points": 100, "num_comments": 10, "source": "hackernews"}]

        prompt = create_analysis_prompt(posts, "2025-01")

        # Should include category information
        assert "Kategorier" in prompt or "Categories" in prompt
        # Should mention some categories from config
        assert "core-llms" in prompt.lower() or "code-assistants" in prompt.lower()

    def test_create_analysis_prompt_empty_posts(self):
        """Test prompt creation with no posts"""
        posts = []

        prompt = create_analysis_prompt(posts, "2025-01")

        # Should still create valid prompt
        assert "2025-01" in prompt
        assert isinstance(prompt, str)
        assert len(prompt) > 0
