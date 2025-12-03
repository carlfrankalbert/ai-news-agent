#!/bin/bash
# Serve HTML locally for testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Check if HTML exists, if not generate it
if [ ! -f "docs/index.html" ]; then
    echo "📄 HTML not found, generating with dummy data..."
    source venv/bin/activate 2>/dev/null || true
    python generate_html.py --dummy
fi

# Find available port
PORT=8000
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
done

echo ""
echo "🚀 Starting local server..."
echo ""
echo "📍 URL: http://localhost:$PORT"
echo "📁 Serving: docs/index.html"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Try Python's built-in server first (most common)
if command -v python3 &> /dev/null; then
    cd docs
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    cd docs
    python -m SimpleHTTPServer $PORT 2>/dev/null || python -m http.server $PORT
else
    echo "❌ Python not found. Please install Python to use local server."
    echo ""
    echo "Alternative: Open docs/index.html directly in your browser:"
    echo "  open docs/index.html"
    exit 1
fi


