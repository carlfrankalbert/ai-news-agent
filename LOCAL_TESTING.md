# Local Testing Guide

## Quick Start

### Option 1: Automated Server (Recommended)

```bash
# Start local server (auto-generates HTML if needed)
./scripts/serve_local.sh
```

Then open: **http://localhost:8000**

### Option 2: Manual Server

```bash
# Generate HTML first
source venv/bin/activate
python generate_html.py --dummy

# Start server
cd docs
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

### Option 3: Direct File Open

```bash
# Generate HTML
python generate_html.py --dummy

# Open directly in browser
open docs/index.html  # macOS
# or
xdg-open docs/index.html  # Linux
```

## URLs

### Local Development
- **Default**: http://localhost:8000
- **Alternative ports**: Script auto-finds available port (8001, 8002, etc.)

### Production URLs
- **GitHub Pages**: https://[username].github.io/ai-news-agent/
- **Cloudflare Pages**: https://ai-news-agent.pages.dev
- **Dev Environment**: https://dev.ai-news-agent.pages.dev

## Testing Workflow

1. **Generate HTML with dummy data:**
   ```bash
   python generate_html.py --dummy
   ```

2. **Start local server:**
   ```bash
   ./scripts/serve_local.sh
   ```

3. **Open in browser:**
   - Navigate to http://localhost:8000
   - Test UI interactions
   - Check console for errors (F12)

4. **Make changes:**
   - Edit `src/ai_news_agent/generator/generate_html.py`
   - Regenerate: `python generate_html.py --dummy`
   - Refresh browser

## Health Check Endpoint

If using Cloudflare Pages Functions, health check is available at:
- **Local**: http://localhost:8000/health (if function is set up)
- **Production**: https://[domain]/health

## Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8000

# Kill the process or use different port
PORT=8001 ./scripts/serve_local.sh
```

### HTML Not Updating

```bash
# Force regenerate
rm docs/index.html
python generate_html.py --dummy
```

### CORS Issues

If testing API calls locally, you may need CORS headers. The local server should handle this, but if issues persist:

```bash
# Use a CORS-enabled server
pip install flask-cors
# Or use browser with CORS disabled (development only)
```

## Development Tips

- **Hot Reload**: Use browser's hard refresh (Cmd+Shift+R / Ctrl+Shift+R)
- **Console Logs**: Check browser console (F12) for JavaScript errors
- **Network Tab**: Monitor API calls and responses
- **Mobile Testing**: Use `ngrok` or similar to test on mobile devices


