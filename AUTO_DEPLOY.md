# 🤖 Fully Automatic Deployment

This guide shows you how to set up **completely automatic** deployment that happens on every push to GitHub.

## Setup GitHub Actions (One-Time)

### Step 1: Get Your Deployment Platform Credentials

#### For Heroku:
1. Go to [Heroku Account Settings](https://dashboard.heroku.com/account)
2. Scroll to "API Key" section
3. Click "Reveal" to get your API key
4. Note your Heroku email

#### For Railway:
1. Go to [Railway Dashboard](https://railway.app)
2. Click your profile → Settings → Tokens
3. Create a new token
4. Get your Service ID from your project

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

**For Heroku:**
- `HEROKU_API_KEY` - Your Heroku API key
- `HEROKU_APP_NAME` - Your app name (e.g., `my-beam-calculator`)
- `HEROKU_EMAIL` - Your Heroku email

**For Railway:**
- `RAILWAY_TOKEN` - Your Railway token
- `RAILWAY_SERVICE_ID` - Your service ID

**For Both:**
- `MONGO_URI` - Your MongoDB connection string
- `GROQ_API_KEY` - Your Groq API key
- `SECRET_KEY` - A random secret key (generate with: `openssl rand -hex 32`)

### Step 3: Update GitHub Actions Workflow

The workflow file (`.github/workflows/deploy.yml`) is already configured! Just make sure your secrets are set.

### Step 4: Push to GitHub

```bash
git add .
git commit -m "Setup automatic deployment"
git push origin main
```

**That's it!** Every time you push to `main` branch, your app will automatically deploy.

## How It Works

1. **On Push**: GitHub Actions triggers the workflow
2. **Tests Run**: Basic import and syntax checks
3. **Deploy**: Automatically deploys to your chosen platform
4. **Status**: Check the Actions tab to see deployment status

## Viewing Deployment Status

1. Go to your GitHub repository
2. Click the **Actions** tab
3. Click on the latest workflow run
4. See real-time deployment logs

## Manual Trigger

You can also trigger deployment manually:

1. Go to **Actions** tab
2. Select **Deploy to Production** workflow
3. Click **Run workflow**
4. Select branch and click **Run workflow**

## Troubleshooting

### Deployment Fails

1. **Check Secrets**: Make sure all required secrets are set
2. **Check Logs**: View the Actions log for error messages
3. **Verify Credentials**: Ensure API keys are valid
4. **Check Platform Status**: Verify Heroku/Railway services are up

### Common Errors

**"HEROKU_API_KEY not found"**
- Add the secret in GitHub Settings → Secrets

**"App not found"**
- Create the Heroku app first: `heroku create your-app-name`
- Or update `HEROKU_APP_NAME` secret

**"MongoDB connection failed"**
- Verify `MONGO_URI` secret is correct
- Check MongoDB Atlas IP whitelist includes GitHub Actions IPs

## Advanced: Multiple Environments

You can deploy to different environments:

- **Staging**: Deploy on push to `develop` branch
- **Production**: Deploy on push to `main` branch

Update `.github/workflows/deploy.yml`:

```yaml
on:
  push:
    branches:
      - main    # Production
      - develop # Staging
```

Then use different app names/secrets for each environment.

## Benefits of Automatic Deployment

✅ **Zero Manual Steps** - Push code, deployment happens automatically  
✅ **Consistent** - Same process every time  
✅ **Fast** - Deploys in minutes  
✅ **Safe** - Tests run before deployment  
✅ **Visible** - See deployment status in GitHub  

## Next Steps

1. Set up your secrets (one-time)
2. Push your code
3. Watch it deploy automatically! 🎉

For manual deployment options, see `QUICK_DEPLOY.md` or `README.md`.

