#!/bin/bash
# Quick test script for AI News Agent

echo "🧪 Quick Test - Collecting data only (no API costs)"
echo ""

source venv/bin/activate
python main.py --collect-only --days 1

echo ""
echo "✅ Test complete! Check output/raw_posts_*.json"
