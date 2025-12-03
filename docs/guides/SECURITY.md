# Security Guide - API Keys

## Important: Never commit API keys to Git

API keys are sensitive credentials and must be kept secret.

## Setup

### 1. Create `.env` file (local development)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your actual API key
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

### 2. Load environment variables

The code automatically loads from environment variables. Make sure `.env` is in `.gitignore` (it already is).

### 3. For GitHub Actions (CI/CD)

Add the API key as a GitHub Secret:

1. Go to: https://github.com/carlfrankalbert/ai-news-agent/settings/secrets/actions
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your API key
5. Click "Add secret"

The workflow (`.github/workflows/daily.yml`) will automatically use this secret.

## Verification

Check that `.env` is ignored:
```bash
git check-ignore .env
# Should output: .env
```

## If you accidentally committed a key

1. **Immediately revoke the key** in Anthropic console
2. **Generate a new key**
3. **Remove from Git history** (if needed):
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

## Best Practices

- ✅ Use `.env` file for local development
- ✅ Use GitHub Secrets for CI/CD
- ✅ Never commit `.env` or any file with keys
- ✅ Rotate keys periodically
- ✅ Use different keys for dev/prod if possible

