# AI News Agent Test Suite

Comprehensive test suite for the AI News Agent project.

## Structure

```
tests/
├── conftest.py                      # Shared pytest fixtures
├── unit/                            # Unit tests
│   ├── test_scoring.py              # Scoring calculation tests
│   ├── test_data_normalization.py   # Data normalization tests
│   └── test_claude_json_parsing.py  # Claude JSON parsing tests
└── README.md                        # This file
```

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Scoring tests only
pytest tests/unit/test_scoring.py

# Data normalization tests only
pytest tests/unit/test_data_normalization.py

# Claude JSON parsing tests only
pytest tests/unit/test_claude_json_parsing.py
```

### Run with Coverage

```bash
pytest --cov=src/ai_news_agent --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage.

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/unit/test_scoring.py::TestCalculatePercentile

# Run a specific test function
pytest tests/unit/test_scoring.py::TestCalculatePercentile::test_percentile_basic

# Run tests matching a pattern
pytest -k "percentile"
```

### Verbose Output

```bash
pytest -v
```

### Show Print Statements

```bash
pytest -s
```

## Test Coverage Areas

### 1. Scoring Calculations (`test_scoring.py`)

Tests all scoring functions:
- ✅ Percentile calculations with edge cases
- ✅ Buzz score calculations
- ✅ Sentiment score calculations
- ✅ Utility score calculations
- ✅ Price score calculations
- ✅ Final weighted score calculations

**Key test cases:**
- Empty data handling
- None value filtering
- Division by zero prevention
- Bounds enforcement (0-100)
- Percentile ranking accuracy

### 2. Data Normalization (`test_data_normalization.py`)

Tests data transformation from API responses:
- ✅ Hacker News post normalization
- ✅ GitHub repository normalization
- ✅ AI relevance filtering (keyword matching)
- ✅ Missing field handling
- ✅ Invalid timestamp handling
- ✅ URL construction and formatting

**Key test cases:**
- Complete vs incomplete data
- Missing/null fields
- Invalid timestamps
- Case-insensitive keyword matching
- Edge cases in relevance detection

### 3. Claude JSON Parsing (`test_claude_json_parsing.py`)

Tests Claude API integration and JSON error recovery:
- ✅ Valid JSON parsing
- ✅ Markdown-wrapped JSON extraction
- ✅ Truncated response handling
- ✅ Trailing comma removal
- ✅ Nested JSON extraction
- ✅ Escaped quotes handling
- ✅ Rankings validation

**Key test cases:**
- Multiple JSON extraction strategies
- Error structure fallbacks
- Validation logic
- Prompt generation

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Using Fixtures

Fixtures are defined in `conftest.py` and automatically available in all tests:

```python
def test_something(sample_hn_story):
    # sample_hn_story fixture is automatically injected
    result = normalize_post(sample_hn_story)
    assert result["source"] == "hackernews"
```

### Mocking External Dependencies

Use `pytest-mock` or `unittest.mock`:

```python
from unittest.mock import patch

@patch('module.external_api_call')
def test_with_mock(mock_api):
    mock_api.return_value = {"data": "test"}
    # Your test code here
```

### Async Tests

Use `pytest-asyncio`:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

## CI/CD Integration

Add to your CI pipeline (e.g., GitHub Actions):

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=src/ai_news_agent --cov-fail-under=80
```

## Current Coverage

Run `pytest --cov` to see current test coverage statistics.

Target: **80%+ coverage** for critical modules:
- `src/ai_news_agent/coding_assistants/analyzers/scoring.py`
- `src/ai_news_agent/collectors/hackernews.py`
- `src/ai_news_agent/collectors/github.py`
- `src/ai_news_agent/analyzer/analyzer.py`

## Troubleshooting

### Import Errors

If you see import errors, ensure you're running pytest from the project root:

```bash
cd /home/user/ai-news-agent
pytest
```

### Fixture Not Found

Make sure `conftest.py` is in the `tests/` directory and pytest can discover it.

### Async Test Issues

Ensure `pytest-asyncio` is installed and `asyncio_mode = auto` is in `pytest.ini`.
