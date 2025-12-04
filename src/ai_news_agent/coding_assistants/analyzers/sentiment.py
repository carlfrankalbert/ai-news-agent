"""
Sentiment Analysis using VADER
"""
from typing import List
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon if not already present
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    print("📥 Downloading VADER lexicon...")
    nltk.download('vader_lexicon', quiet=True)

_analyzer = None


def get_sentiment_analyzer() -> SentimentIntensityAnalyzer:
    """Get or create sentiment analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def analyze_sentiment(text: str) -> float:
    """
    Analyze sentiment of a single text.
    
    Returns:
        Compound score (-1 to 1, where 1 is most positive)
    """
    analyzer = get_sentiment_analyzer()
    scores = analyzer.polarity_scores(text)
    return scores['compound']


def analyze_sentiment_batch(texts: List[str]) -> float:
    """
    Analyze sentiment of multiple texts and return average.
    
    Returns:
        Average compound score (-1 to 1)
    """
    if not texts:
        return 0.0
    
    analyzer = get_sentiment_analyzer()
    scores = []
    
    for text in texts:
        if text and isinstance(text, str) and len(text.strip()) > 0:
            score = analyzer.polarity_scores(text)['compound']
            scores.append(score)
    
    if not scores:
        return 0.0
    
    return sum(scores) / len(scores)


def normalize_sentiment(score: float) -> float:
    """
    Normalize sentiment score from (-1, 1) to (0, 1).
    
    Args:
        score: Sentiment compound score (-1 to 1)
    
    Returns:
        Normalized score (0 to 1)
    """
    # Shift from (-1, 1) to (0, 2), then divide by 2 to get (0, 1)
    return (score + 1) / 2

