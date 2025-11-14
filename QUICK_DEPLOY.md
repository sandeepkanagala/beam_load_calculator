# 🚀 Quick Automatic Deployment Guide

## Option 1: Python Script (Recommended - Cross-Platform)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run deployment script
python setup_deploy.py
```

The script will:
- ✅ Check/create .env file
- ✅ Verify dependencies
- ✅ Detect deployment platform (Heroku/Railway)
- ✅ Set environment variables
- ✅ Deploy automatically

## Option 2: Shell Script (Linux/Mac)

```bash
# Make executable (if needed)
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

## Option 3: PowerShell Script (Windows)

```powershell
# Run deployment
.\deploy.ps1
```

## Option 4: GitHub Actions (Automatic on Push)

1. **Set up GitHub Secrets** (Settings → Secrets → Actions):
   - `HEROKU_API_KEY` - Your Heroku API key
   - `HEROKU_APP_NAME` - Your Heroku app name
   - `HEROKU_EMAIL` - Your Heroku email
   - OR
   - `RAILWAY_TOKEN` - Your Railway token
   - `RAILWAY_SERVICE_ID` - Your Railway service ID

2. **Push to main branch**:
   ```bash
   git push origin main
   ```

3. **Deployment happens automatically!** Check Actions tab in GitHub.

## Option 5: Manual Quick Deploy

### Heroku (Fastest)

```bash
# 1. Login
heroku login

# 2. Create app (first time only)
heroku create your-app-name

# 3. Set variables
heroku config:set MONGO_URI="your-mongodb-uri"
heroku config:set GROQ_API_KEY="your-groq-key"
heroku config:set SECRET_KEY="$(openssl rand -hex 32)"

# 4. Deploy
git push heroku main
```

### Railway

```bash
# 1. Install CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize
railway init

# 4. Set variables (via dashboard or CLI)
railway variables set MONGO_URI="your-uri"
railway variables set GROQ_API_KEY="your-key"

# 5. Deploy
railway up
```

## Pre-Deployment Checklist

- [ ] `.env` file created and configured
- [ ] MongoDB URI set (local or Atlas)
- [ ] Groq API key obtained
- [ ] Firebase config updated in `static/auth.js` (optional)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Tested locally: `python app.py`

## Environment Variables Needed

```env
MONGO_URI=mongodb://localhost:27017/beamdb
GROQ_API_KEY=your-groq-api-key
SECRET_KEY=your-secret-key-min-32-chars
FLASK_DEBUG=False
```

## After Deployment

1. **Test your app**: Visit the deployed URL
2. **Check logs**: 
   - Heroku: `heroku logs --tail`
   - Railway: `railway logs`
3. **Monitor**: Check for errors in logs
4. **Update Firebase**: Update `static/auth.js` with production Firebase config

## Troubleshooting

### "Command not found" errors
- Install the required CLI tool (Heroku or Railway)
- Make sure it's in your PATH

### Environment variable errors
- Double-check `.env` file exists
- Verify all required variables are set
- No quotes needed in `.env` file values

### Deployment fails
- Check logs: `heroku logs` or `railway logs`
- Verify MongoDB connection
- Check Groq API key is valid
- Ensure all dependencies are in `requirements.txt`

## Need Help?

- Check `README.md` for detailed instructions
- Check `DEPLOYMENT.md` for platform-specific guides
- Review error logs from your deployment platform

