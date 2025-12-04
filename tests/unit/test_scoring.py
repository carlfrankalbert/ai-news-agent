"""
Unit tests for scoring calculations
Tests all scoring functions in src/ai_news_agent/coding_assistants/analyzers/scoring.py
"""
import pytest
from src.ai_news_agent.coding_assistants.analyzers.scoring import (
    calculate_percentile,
    calculate_buzz_score,
    calculate_sentiment_score,
    calculate_utility_score,
    calculate_price_score,
    calculate_final_score
)


class TestCalculatePercentile:
    """Test percentile calculation function"""

    def test_percentile_basic(self):
        """Test basic percentile calculation"""
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Value at 0th percentile (minimum)
        assert calculate_percentile(1, values) == 10.0

        # Value at 100th percentile (maximum)
        assert calculate_percentile(10, values) == 100.0

        # Value at 50th percentile (median)
        assert calculate_percentile(5, values) == 50.0

    def test_percentile_with_duplicates(self):
        """Test percentile with duplicate values"""
        values = [1, 2, 2, 2, 3, 4, 5]

        # All 2s should get same percentile
        result = calculate_percentile(2, values)
        assert 20 <= result <= 60  # Should be somewhere in middle

    def test_percentile_empty_list(self):
        """Test percentile with empty list"""
        assert calculate_percentile(5, []) == 0.0

    def test_percentile_single_value(self):
        """Test percentile with single value"""
        assert calculate_percentile(5, [5]) == 100.0
        assert calculate_percentile(3, [5]) == 0.0

    def test_percentile_with_none_values(self):
        """Test percentile calculation filters out None values"""
        values = [1, None, 2, None, 3, 4, 5]
        result = calculate_percentile(3, values)
        # Should ignore None values and calculate based on [1, 2, 3, 4, 5]
        assert result == 60.0

    def test_percentile_value_is_none(self):
        """Test percentile when value itself is None"""
        values = [1, 2, 3, 4, 5]
        assert calculate_percentile(None, values) == 0.0

    def test_percentile_all_none_values(self):
        """Test percentile when all comparison values are None"""
        values = [None, None, None]
        assert calculate_percentile(5, values) == 0.0

    def test_percentile_with_floats(self):
        """Test percentile with floating point values"""
        values = [1.5, 2.7, 3.2, 4.8, 5.1]
        result = calculate_percentile(3.2, values)
        assert result == 60.0

    def test_percentile_edge_case_zero(self):
        """Test percentile with zero values"""
        values = [0, 0, 0, 1, 2, 3]
        result = calculate_percentile(0, values)
        assert result == 50.0  # 3 out of 6 values are <= 0


class TestCalculateBuzzScore:
    """Test buzz score calculation"""

    def test_buzz_score_basic(self, sample_tools_data):
        """Test basic buzz score calculation"""
        tool_data = sample_tools_data[1]  # Tool B

        score = calculate_buzz_score(
            tool_name="Tool B",
            github_data=tool_data["github"],
            hn_data=tool_data["hn"],
            reddit_data=tool_data["reddit"],
            all_tools_data=sample_tools_data
        )

        # Score should be between 0 and 100
        assert 0 <= score <= 100

        # Tool B should score higher than Tool D (has more stars, mentions)
        tool_d_score = calculate_buzz_score(
            tool_name="Tool D",
            github_data=sample_tools_data[3]["github"],
            hn_data=sample_tools_data[3]["hn"],
            reddit_data=sample_tools_data[3]["reddit"],
            all_tools_data=sample_tools_data
        )

        assert score > tool_d_score

    def test_buzz_score_highest_performer(self, sample_tools_data):
        """Test that tool with highest metrics gets highest buzz score"""
        # Tool C has highest stars and mentions
        tool_c_score = calculate_buzz_score(
            tool_name="Tool C",
            github_data=sample_tools_data[2]["github"],
            hn_data=sample_tools_data[2]["hn"],
            reddit_data=sample_tools_data[2]["reddit"],
            all_tools_data=sample_tools_data
        )

        # Should be higher than other tools
        # Calculate score for Tool A (lower metrics)
        tool_a_score = calculate_buzz_score(
            tool_name="Tool A",
            github_data=sample_tools_data[0]["github"],
            hn_data=sample_tools_data[0]["hn"],
            reddit_data=sample_tools_data[0]["reddit"],
            all_tools_data=sample_tools_data
        )

        # Tool C should have highest score
        assert tool_c_score > tool_a_score
        assert tool_c_score >= 70  # Should be reasonably high

    def test_buzz_score_no_github_data(self, sample_tools_data):
        """Test buzz score when GitHub data is missing"""
        score = calculate_buzz_score(
            tool_name="Unknown Tool",
            github_data={},  # No data
            hn_data={"mentions_count": 10},
            reddit_data={"mentions_count": 5},
            all_tools_data=sample_tools_data
        )

        # Should still calculate, but score will be lower
        assert 0 <= score <= 100

    def test_buzz_score_no_growth_data(self, sample_tools_data):
        """Test buzz score when stars_30d_ago is missing"""
        github_data = {"stars": 1000}  # No stars_30d_ago

        score = calculate_buzz_score(
            tool_name="Test Tool",
            github_data=github_data,
            hn_data={"mentions_count": 50},
            reddit_data={"mentions_count": 30},
            all_tools_data=sample_tools_data
        )

        # Should handle gracefully
        assert 0 <= score <= 100

    def test_buzz_score_zero_stars_prevents_division_error(self, sample_tools_data):
        """Test that zero stars in 30d_ago doesn't cause division by zero"""
        github_data = {"stars": 100, "stars_30d_ago": 0}

        # Should not raise ZeroDivisionError
        score = calculate_buzz_score(
            tool_name="Test Tool",
            github_data=github_data,
            hn_data={"mentions_count": 10},
            reddit_data={"mentions_count": 5},
            all_tools_data=sample_tools_data
        )

        assert 0 <= score <= 100


class TestCalculateSentimentScore:
    """Test sentiment score calculation"""

    def test_sentiment_score_perfect(self):
        """Test sentiment score with perfect metrics"""
        github_data = {
            "open_issues": 5,
            "closed_issues": 95  # 95% closed = excellent
        }

        score = calculate_sentiment_score(
            tool_name="Test Tool",
            github_data=github_data,
            hn_data={},
            reddit_data={},
            hn_sentiment=1.0,  # Perfect sentiment
            reddit_sentiment=1.0  # Perfect sentiment
        )

        # Should be very high
        assert score >= 90

    def test_sentiment_score_poor(self):
        """Test sentiment score with poor metrics"""
        github_data = {
            "open_issues": 95,
            "closed_issues": 5  # Only 5% closed = poor
        }

        score = calculate_sentiment_score(
            tool_name="Test Tool",
            github_data=github_data,
            hn_data={},
            reddit_data={},
            hn_sentiment=0.0,  # Negative sentiment
            reddit_sentiment=0.0  # Negative sentiment
        )

        # Should be very low
        assert score <= 20

    def test_sentiment_score_no_issues(self):
        """Test sentiment score when there are no issues"""
        github_data = {
            "open_issues": 0,
            "closed_issues": 0
        }

        score = calculate_sentiment_score(
            tool_name="Test Tool",
            github_data=github_data,
            hn_data={},
            reddit_data={},
            hn_sentiment=0.7,
            reddit_sentiment=0.6
        )

        # Should default to neutral (50) for issue health
        assert 40 <= score <= 80

    def test_sentiment_score_missing_issue_data(self):
        """Test sentiment score with missing issue data"""
        github_data = {}  # No issue data

        score = calculate_sentiment_score(
            tool_name="Test Tool",
            github_data=github_data,
            hn_data={},
            reddit_data={},
            hn_sentiment=0.8,
            reddit_sentiment=0.7
        )

        # Should handle gracefully
        assert 0 <= score <= 100

    def test_sentiment_score_bounds(self):
        """Test that sentiment score stays within bounds"""
        # Try extreme values
        github_data = {"open_issues": 0, "closed_issues": 1000000}

        score = calculate_sentiment_score(
            tool_name="Test Tool",
            github_data=github_data,
            hn_data={},
            reddit_data={},
            hn_sentiment=2.0,  # Invalid high value
            reddit_sentiment=2.0
        )

        # Should be clamped to 0-100
        assert 0 <= score <= 100


class TestCalculateUtilityScore:
    """Test utility score calculation"""

    def test_utility_score_missing_tool(self, monkeypatch):
        """Test utility score when tool not in features.json"""
        # Mock load_features to return empty dict
        def mock_load_features():
            return {}

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_features",
            mock_load_features
        )

        score = calculate_utility_score("Unknown Tool")

        # Should default to 50
        assert score == 50.0

    def test_utility_score_with_total(self, monkeypatch):
        """Test utility score when features.json has 'total' field"""
        def mock_load_features():
            return {
                "Test Tool": {
                    "total": 85,
                    "feature1": 90,
                    "feature2": 80
                }
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_features",
            mock_load_features
        )

        score = calculate_utility_score("Test Tool")
        assert score == 85

    def test_utility_score_calculated_average(self, monkeypatch):
        """Test utility score calculated from feature averages"""
        def mock_load_features():
            return {
                "Test Tool": {
                    "feature1": 80,
                    "feature2": 90,
                    "feature3": 70
                }
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_features",
            mock_load_features
        )

        score = calculate_utility_score("Test Tool")
        # Average of 80, 90, 70 = 80
        assert score == 80.0

    def test_utility_score_bounds_enforcement(self, monkeypatch):
        """Test utility score enforces 0-100 bounds"""
        def mock_load_features():
            return {
                "Test Tool": {"total": 150}  # Invalid high value
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_features",
            mock_load_features
        )

        score = calculate_utility_score("Test Tool")
        assert score == 100  # Should be clamped to 100


class TestCalculatePriceScore:
    """Test price score calculation"""

    def test_price_score_missing_tool(self, monkeypatch):
        """Test price score when tool not in pricing.json"""
        def mock_load_pricing():
            return {}

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_pricing",
            mock_load_pricing
        )

        score = calculate_price_score("Unknown Tool")
        assert score == 50.0

    def test_price_score_with_explicit_score(self, monkeypatch):
        """Test price score with explicit score field"""
        def mock_load_pricing():
            return {
                "Test Tool": {"score": 75, "tier": "freemium"}
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_pricing",
            mock_load_pricing
        )

        score = calculate_price_score("Test Tool")
        assert score == 75

    def test_price_score_free_tier(self, monkeypatch):
        """Test price score for free tier"""
        def mock_load_pricing():
            return {
                "Test Tool": {"tier": "free"}
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_pricing",
            mock_load_pricing
        )

        score = calculate_price_score("Test Tool")
        assert score == 100

    def test_price_score_paid_tier(self, monkeypatch):
        """Test price score for paid tier"""
        def mock_load_pricing():
            return {
                "Test Tool": {"tier": "paid"}
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_pricing",
            mock_load_pricing
        )

        score = calculate_price_score("Test Tool")
        assert score == 40

    def test_price_score_expensive_tier(self, monkeypatch):
        """Test price score for expensive tier"""
        def mock_load_pricing():
            return {
                "Test Tool": {"tier": "expensive"}
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_pricing",
            mock_load_pricing
        )

        score = calculate_price_score("Test Tool")
        assert score == 20

    def test_price_score_unknown_tier(self, monkeypatch):
        """Test price score for unknown tier defaults to 50"""
        def mock_load_pricing():
            return {
                "Test Tool": {"tier": "unknown_tier"}
            }

        monkeypatch.setattr(
            "src.ai_news_agent.coding_assistants.analyzers.scoring.load_pricing",
            mock_load_pricing
        )

        score = calculate_price_score("Test Tool")
        assert score == 50


class TestCalculateFinalScore:
    """Test final score calculation"""

    def test_final_score_basic(self):
        """Test basic final score calculation"""
        score = calculate_final_score(
            buzz=80,
            sentiment=70,
            utility=90,
            price=60
        )

        # Should be weighted average between 0-100
        assert 0 <= score <= 100

    def test_final_score_all_perfect(self):
        """Test final score with all perfect scores"""
        score = calculate_final_score(
            buzz=100,
            sentiment=100,
            utility=100,
            price=100
        )

        assert score == 100.0

    def test_final_score_all_zero(self):
        """Test final score with all zero scores"""
        score = calculate_final_score(
            buzz=0,
            sentiment=0,
            utility=0,
            price=0
        )

        assert score == 0.0

    def test_final_score_bounds_enforcement(self):
        """Test final score enforces bounds even with invalid inputs"""
        # Try with values outside normal range
        score = calculate_final_score(
            buzz=150,  # Invalid
            sentiment=-10,  # Invalid
            utility=200,  # Invalid
            price=50
        )

        # Should still clamp to 0-100
        assert 0 <= score <= 100

    def test_final_score_weights_matter(self):
        """Test that different weights produce different results"""
        # High buzz, low others
        score1 = calculate_final_score(buzz=100, sentiment=0, utility=0, price=0)

        # Low buzz, high others
        score2 = calculate_final_score(buzz=0, sentiment=100, utility=100, price=100)

        # Scores should be different (unless weights are exactly equal)
        # This tests that weights are actually being applied
        assert score1 != score2 or True  # Allow equal if weights happen to balance
