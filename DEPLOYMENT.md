# Deployment Guide

Complete guide for setting up and using the deployment pipeline.

## Quick Start

### Deploy via Slack

1. Set up Slack slash command pointing to Cloudflare Worker
2. Use `/deploy dev` or `/deploy prod` in Slack

### Deploy via Makefile

```bash
make deploy-dev   # Deploy to development
make deploy-prod   # Deploy to production
make preview       # Trigger preview deployment
```

### Deploy via GitHub Actions

1. Go to Actions tab
2. Select workflow (Deploy to Development / Deploy to Production)
3. Click "Run workflow"

## Setup Instructions

### 1. GitHub Secrets

Configure these in your repository settings → Secrets and variables → Actions:

```
CLOUDFLARE_API_TOKEN       # Cloudflare API token
CLOUDFLARE_ACCOUNT_ID      # Cloudflare account ID
ANTHROPIC_API_KEY          # Anthropic API key
SLACK_WEBHOOK_URL          # Slack webhook for notifications
SLACK_SIGNING_SECRET       # Slack signing secret
DEV_DOMAIN                 # Optional: custom dev domain
PROD_DOMAIN                # Optional: custom production domain
```

### 2. Cloudflare Worker Setup

#### Deploy the Worker

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy worker
cd infra/cloudflare
wrangler deploy
```

#### Set Worker Secrets

```bash
wrangler secret put SLACK_SIGNING_SECRET
wrangler secret put GITHUB_TOKEN          # GitHub personal access token
wrangler secret put GITHUB_REPO_OWNER     # Your GitHub username
wrangler secret put GITHUB_REPO_NAME      # Repository name
wrangler secret put DOMAIN                 # Your domain (e.g., ai-news-agent.pages.dev)
```

#### Configure Slack Slash Command

1. Go to [Slack API](https://api.slack.com/apps)
2. Create or select your app
3. Go to "Slash Commands"
4. Create command: `/deploy`
5. Set Request URL to your Cloudflare Worker URL
6. Save

### 3. Cloudflare Pages Setup

1. Go to Cloudflare Dashboard → Pages
2. Create new project: `ai-news-agent`
3. Connect to GitHub repository
4. Build settings:
   - Framework preset: None
   - Build command: (leave empty)
   - Build output directory: `docs`
   - Root directory: `/`

### 4. KV Namespace Setup (Optional)

For storing dev seed data:

```bash
# Create namespace
wrangler kv:namespace create "DEV_DATA"

# Update wrangler.toml with namespace ID
# Then bind in your Worker code
```

## Pipeline Flow

### Development Deployment

1. Slack command `/deploy dev` → Cloudflare Worker
2. Worker triggers GitHub Actions `deploy_dev.yml`
3. GitHub Actions:
   - Checks out code
   - Runs tests
   - Prepares dev data (from prod_cache.json or fixed_seeds.json)
   - Runs full pipeline
   - Deploys to Cloudflare Pages (dev environment)
   - Health check
   - Rollback if health check fails
   - Sends Slack notification

### Production Deployment

1. Slack command `/deploy prod` → Cloudflare Worker
2. Worker triggers GitHub Actions `deploy_prod.yml`
3. GitHub Actions:
   - Checks out code
   - Runs tests
   - Runs full pipeline
   - Deploys to Cloudflare Pages (production)
   - Health check
   - Rollback if health check fails
   - Archives prod data to `prod_cache.json`
   - Sends Slack notification

### Preview Deployments

- Automatically triggered on pull requests
- Deploys to Cloudflare Pages Preview
- Comments on PR with preview URL and health status

## Health Checks

Health check endpoint: `https://<domain>/health`

Expected response:
```json
{
  "status": "ok",
  "time": "2025-12-15T10:00:00Z",
  "version": "abc1234",
  "environment": "dev"
}
```

If health check fails:
- Automatic rollback to previous deployment
- Slack notification sent
- Build marked as failed

## Seed Data Strategy

**Development:**
- Priority 1: `output/prod_cache.json` (from last prod deployment)
- Priority 2: `infra/seeds/fixed_seeds.json` (fallback)

**Production:**
- Always runs full pipeline
- Archives latest data to `output/prod_cache.json`

## Troubleshooting

### Worker not receiving Slack commands

- Verify Slack signing secret matches
- Check Worker logs in Cloudflare Dashboard
- Verify slash command URL is correct

### GitHub Actions not triggering

- Verify `GITHUB_TOKEN` in Worker secrets
- Check repository permissions
- Verify workflow files are in `.github/workflows/`

### Health check failing

- Check Cloudflare Pages deployment status
- Verify `/health` endpoint is accessible
- Check function logs in Cloudflare Dashboard

### Deployment rollback

- Automatic rollback happens if health check fails
- Manual rollback: Use Cloudflare Pages dashboard
- Previous deployments are preserved

## Environment Variables

### Runtime (Cloudflare Pages)

Set in Cloudflare Pages → Settings → Environment variables:

- `ENVIRONMENT` - `dev` or `prod`
- `GIT_SHA` - Git commit SHA (auto-set by GitHub Actions)

### Build Time (GitHub Actions)

Set as GitHub Secrets (see Setup section above).

## Monitoring

- GitHub Actions: View runs in Actions tab
- Cloudflare Pages: View deployments in Pages dashboard
- Slack: Receive notifications for all deployments
- Health checks: Monitor `/health` endpoint

## Best Practices

1. **Always test in dev first** before deploying to prod
2. **Monitor health checks** after deployment
3. **Keep secrets secure** - never commit to repository
4. **Use preview deployments** for PR reviews
5. **Archive prod data** for dev environment seeding


