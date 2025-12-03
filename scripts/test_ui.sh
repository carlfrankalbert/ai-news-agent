#!/bin/bash
# Quick UI test script using dummy data

echo "🎨 Testing UI with dummy data..."
echo ""

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Generate HTML with dummy data
python3 generate_html.py --dummy

# Open in browser
if [ -f "docs/index.html" ]; then
    open docs/index.html
    echo ""
    echo "✅ UI test complete! Browser opened."
    echo "💡 Edit generate_html.py and run again to see changes instantly"
else
    echo "❌ HTML generation failed"
    exit 1
fi

