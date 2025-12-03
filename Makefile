.PHONY: deploy-dev deploy-prod preview help

help:
	@echo "Available commands:"
	@echo "  make deploy-dev   - Deploy to development environment"
	@echo "  make deploy-prod  - Deploy to production environment"
	@echo "  make preview      - Trigger preview deployment workflow"

deploy-dev:
	@echo "🚀 Triggering dev deployment..."
	gh workflow run deploy_dev.yml --ref main

deploy-prod:
	@echo "🚀 Triggering prod deployment..."
	gh workflow run deploy_prod.yml --ref main

preview:
	@echo "🚀 Triggering preview deployment..."
	gh workflow run preview.yml

# Local development helpers
local-healthcheck:
	@python infra/scripts/healthcheck.py

local-prepare-dev:
	@python infra/scripts/prepare_dev_data.py

# Cloudflare Workers
deploy-worker:
	@echo "📦 Deploying Cloudflare Worker..."
	wrangler deploy

# Setup helpers
setup-secrets:
	@echo "🔐 Setting up Cloudflare Worker secrets..."
	@echo "Run these commands:"
	@echo "  wrangler secret put SLACK_SIGNING_SECRET"
	@echo "  wrangler secret put GITHUB_TOKEN"
	@echo "  wrangler secret put GITHUB_REPO_OWNER"
	@echo "  wrangler secret put GITHUB_REPO_NAME"
	@echo "  wrangler secret put DOMAIN"

