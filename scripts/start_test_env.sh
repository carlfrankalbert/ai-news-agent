#!/bin/bash
# Start test environment for AI News Agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "🚀 Starting test environment..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --quiet --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install --quiet -r requirements.txt

# Verify installation
echo ""
echo "✅ Test environment ready!"
echo ""
echo "Python version: $(python --version)"
echo "Python path: $(which python)"
echo ""
echo "Installed packages:"
pip list | grep -E "httpx|anthropic|dotenv" || true
echo ""
echo "📝 Available commands:"
echo "  python main.py --help              # Show help"
echo "  python main.py --collect-only       # Collect data only"
echo "  python generate_html.py --dummy    # Generate HTML with dummy data"
echo ""
echo "🧪 Test scripts:"
echo "  ./scripts/test_quick.sh             # Quick test"
echo "  ./scripts/test_full.sh              # Full test"
echo "  ./scripts/test_ui.sh                # UI test"
echo ""
echo "💡 To activate manually:"
echo "  source venv/bin/activate"
echo ""
echo "⚠️  Don't forget to set ANTHROPIC_API_KEY:"
echo "  export ANTHROPIC_API_KEY='sk-ant-...'"

