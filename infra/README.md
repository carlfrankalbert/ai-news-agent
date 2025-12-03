# Infrastructure Documentation

This directory contains all infrastructure code for the AI News Agent deployment pipeline.

## Structure

```
infra/
├── cloudflare/
│   └── slack_deploy_router.js    # Cloudflare Worker for Slack integration
├── seeds/
│   ├── fixed_seeds.json           # Fixed seed data for dev environment
│   └── seed_loader.py             # Loads seed data (prod cache or fixed)
└── scripts/
    ├── prepare_dev_data.py        # Prepares and uploads dev seed data
    ├── handle_deploy_dev.py       # Dev deployment handler
    ├── handle_deploy_prod.py      # Prod deployment handler
    └── healthcheck.py             # Health check script
```

## Setup

### 1. GitHub Secrets

Configure these secrets in your GitHub repository:

- `CLOUDFLARE_API_TOKEN` - Cloudflare API token with Pages/Workers permissions
- `CLOUDFLARE_ACCOUNT_ID` - Your Cloudflare account ID
- `ANTHROPIC_API_KEY` - Anthropic API key for Claude
- `SLACK_WEBHOOK_URL` - Slack webhook URL for notifications
- `SLACK_SIGNING_SECRET` - Slack signing secret for webhook verification
- `DEV_DOMAIN` (optional) - Custom dev domain
- `PROD_DOMAIN` (optional) - Custom production domain

### 2. Cloudflare Worker Setup

1. Create a Cloudflare Worker for the Slack router:
   ```bash
   wrangler deploy
   ```

2. Set secrets:
   ```bash
   wrangler secret put SLACK_SIGNING_SECRET
   wrangler secret put GITHUB_TOKEN
   wrangler secret put GITHUB_REPO_OWNER
   wrangler secret put GITHUB_REPO_NAME
   wrangler secret put DOMAIN
   ```

3. Configure Slack slash command:
   - Go to Slack App settings
   - Add slash command: `/deploy`
   - Set request URL to your Cloudflare Worker URL

### 3. Cloudflare Pages Setup

1. Create a Pages project named `ai-news-agent`
2. Connect to your GitHub repository
3. Set build settings:
   - Build command: (none, static site)
   - Output directory: `docs`
   - Root directory: `/`

### 4. KV Namespace Setup

1. Create a KV namespace for dev data:
   ```bash
   wrangler kv:namespace create "DEV_DATA"
   ```

2. Update `wrangler.toml` with the namespace ID

## Usage

### Deploy via Slack

- `/deploy dev` - Deploy to development
- `/deploy prod` - Deploy to production

### Deploy via Makefile

```bash
make deploy-dev
make deploy-prod
make preview
```

### Deploy via GitHub Actions

Go to Actions tab and manually trigger:
- `Deploy to Development`
- `Deploy to Production`

## Seed Data Strategy

**Development:**
1. If `output/prod_cache.json` exists → use it
2. Else → use `infra/seeds/fixed_seeds.json`

**Production:**
- Runs full pipeline
- Archives latest data to `output/prod_cache.json`

## Health Checks

Health check endpoint: `https://<domain>/health`

Returns:
```json
{
  "status": "ok",
  "time": "2025-12-15T10:00:00Z",
  "version": "abc1234",
  "environment": "dev"
}
```

## Rollback

If health check fails after deployment:
- Automatic rollback is triggered
- Previous deployment is restored
- Slack notification is sent

## Preview Deployments

Preview deployments are automatically created for pull requests:
- Deploys to Cloudflare Pages Preview
- Comments on PR with preview URL
- Includes health check status

