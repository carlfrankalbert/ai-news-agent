#!/bin/bash
# Full test script for AI News Agent (includes Claude analysis)

echo "🧪 Full Test - Collection + Analysis (uses Claude API)"
echo ""

source venv/bin/activate
python main.py --days 1

echo ""
echo "✅ Test complete! Check:"
echo "   - output/raw_posts_*.json (raw data)"
echo "   - output/rankings_*.json (Claude analysis)"
echo "   - docs/index.html (HTML report)"
