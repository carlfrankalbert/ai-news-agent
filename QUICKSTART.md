# Quick Start Guide

## 🚀 Deploy in 3 Steps

### 1. Set Up Secrets

**GitHub Secrets** (Repository → Settings → Secrets):
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `ANTHROPIC_API_KEY`
- `SLACK_WEBHOOK_URL`
- `SLACK_SIGNING_SECRET`

**Cloudflare Worker Secrets**:
```bash
wrangler secret put SLACK_SIGNING_SECRET
wrangler secret put GITHUB_TOKEN
wrangler secret put GITHUB_REPO_OWNER
wrangler secret put GITHUB_REPO_NAME
wrangler secret put DOMAIN
```

### 2. Deploy Cloudflare Worker

```bash
cd infra/cloudflare
wrangler deploy
```

### 3. Configure Slack

1. Go to [Slack API](https://api.slack.com/apps)
2. Create slash command `/deploy`
3. Point to your Cloudflare Worker URL

## ✅ Done!

Now use `/deploy dev` or `/deploy prod` in Slack!

## Alternative: Deploy via Makefile

```bash
make deploy-dev   # Development
make deploy-prod  # Production
```

## Alternative: Deploy via GitHub Actions

1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"

---

For detailed setup, see [DEPLOYMENT.md](./DEPLOYMENT.md)


