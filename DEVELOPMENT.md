# Development Workflow

This document describes the development workflow for the AI News Agent project.

## Initial Setup

If you're setting this up for the first time, you need to create the `dev` branch:

```bash
git checkout main
git pull origin main
git checkout -b dev
git push -u origin dev
```

After this one-time setup, the dev branch will exist in your repository and you can follow the workflow below.

## Branch Strategy

The project uses a simple two-branch strategy:

- **`main`** - Production branch
  - Auto-deploys to https://ai-radar.fyrk.no
  - Scheduled workflows run daily/monthly
  - Only stable, tested code

- **`dev`** - Development/staging branch
  - Auto-deploys to Cloudflare Pages preview URL
  - For testing changes before production
  - Workflows can be triggered manually or on push

## Local Development

### 1. Clone and Setup

```bash
git clone https://github.com/carlfrankalbert/ai-news-agent.git
cd ai-news-agent
pip install -r requirements.txt
```

### 2. Create .env File

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."  # Optional
```

### 3. Test Locally

```bash
# Run full pipeline
python main.py --days 30

# Generate HTML
python generate_html.py

# Check links
python check_links.py

# Run tests
pytest
```

## Making Changes

### Option A: Feature Branch Workflow (Recommended)

```bash
# 1. Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/my-change

# 2. Make changes and test locally
python main.py --days 30
python generate_html.py

# 3. Commit changes
git add .
git commit -m "Add feature: my change"

# 4. Merge to dev for staging test
git checkout dev
git merge feature/my-change
git push origin dev

# 5. Check Cloudflare Pages preview deployment
# Wait for GitHub Actions to complete
# Test on preview URL

# 6. If everything works, merge to main
git checkout main
git merge dev
git push origin main

# 7. Verify production deployment
# Check https://ai-radar.fyrk.no
```

### Option B: Direct Dev Branch (Simpler)

```bash
# 1. Work directly on dev branch
git checkout dev
git pull origin dev

# 2. Make changes and test locally
python main.py --days 30

# 3. Push to dev
git add .
git commit -m "Update feature"
git push origin dev

# 4. Test on preview deployment

# 5. When ready, merge to main
git checkout main
git merge dev
git push origin main
```

## GitHub Actions Workflows

### Daily AI News Scan (daily.yml)

**Triggers:**
- **Scheduled:** 06:00 UTC daily (only on `main`)
- **Manual:** Via workflow_dispatch
- **Push:** On push to `main` or `dev`

**What it does:**
1. Collects data from Hacker News, GitHub, Reddit
2. Analyzes with Claude
3. Generates HTML
4. Commits results to the current branch

### Monthly Capability Update (monthly-capability-update.yml)

**Triggers:**
- **Scheduled:** 09:00 UTC on 1st of month (only on `main`)
- **Manual:** Via workflow_dispatch
- **Push:** On push to `main` or `dev`

**What it does:**
1. Updates AI capability tracking data
2. Generates capability report
3. Commits results to the current branch

### Check Provider Links (check_links.yml)

**Triggers:**
- **Scheduled:** 02:00 UTC daily (only on `main`)
- **Manual:** Via workflow_dispatch
- **Push:** On push to `main` or `dev`

**What it does:**
1. Validates all provider links in tool_links.json
2. Uploads report as artifact
3. Creates GitHub issue if broken links found (only on `main`)

## Manual Workflow Triggers

You can manually trigger workflows from GitHub Actions tab:

1. Go to **Actions** tab
2. Select workflow (e.g., "Daily AI News Scan")
3. Click **Run workflow**
4. Select branch (`main` or `dev`)
5. Click **Run workflow**

## Cloudflare Pages Deployment

### Automatic Deployment

- **Main branch** → Production (ai-radar.fyrk.no)
- **Dev branch** → Preview URL (automatically generated)

### Finding Preview URL

1. Go to Cloudflare Pages dashboard
2. Select your project
3. Find the latest deployment for `dev` branch
4. Copy the preview URL (e.g., `dev-abc123.ai-radar.pages.dev`)

Alternatively, check the GitHub Actions "Pages" deployment logs.

## Testing Strategy

### Before Pushing to Dev

```bash
# Run local tests
pytest

# Test data collection (free, no API calls)
python main.py --collect-only

# Test with dummy data
python generate_html.py --dummy

# Test full pipeline with limited data
python main.py --days 7
```

### Before Merging to Main

1. ✅ All tests pass locally
2. ✅ Code pushed to `dev` branch
3. ✅ GitHub Actions workflows completed successfully on `dev`
4. ✅ Preview deployment tested and working
5. ✅ No errors in workflow logs

## Rollback Strategy

If something breaks in production:

```bash
# Quick rollback to previous commit
git checkout main
git revert HEAD
git push origin main
```

Or revert to specific commit:

```bash
git checkout main
git revert <commit-hash>
git push origin main
```

## Environment Variables

Required in GitHub Secrets:

- `ANTHROPIC_API_KEY` - Required for Claude API
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

Optional:

- `TWITTER_BEARER_TOKEN` - For Twitter data collection

## Troubleshooting

### Workflow Fails on Dev

1. Check workflow logs in GitHub Actions
2. Fix the issue locally
3. Push again to `dev`
4. No impact on production

### Preview Deployment Not Working

1. Check Cloudflare Pages dashboard
2. Verify `docs/index.html` is being generated
3. Check GitHub Actions logs for errors

### Merge Conflicts

```bash
# If dev is behind main
git checkout dev
git merge main
# Resolve conflicts
git push origin dev
```

## Best Practices

1. **Always test on `dev` first** - Never push untested code to `main`
2. **Keep commits atomic** - One logical change per commit
3. **Write clear commit messages** - Explain what and why
4. **Review workflow logs** - Even if they pass, check for warnings
5. **Test preview deployments** - Don't just assume they work
6. **Keep dev and main in sync** - Regularly merge main into dev if needed

## Quick Reference

```bash
# Switch between branches
git checkout main
git checkout dev

# Update branches
git pull origin main
git pull origin dev

# Merge dev to main
git checkout main
git merge dev
git push origin main

# Check current branch
git branch

# View recent commits
git log --oneline -10
```
