# 🚀 Quick Deployment Guide

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] MongoDB database set up (local or Atlas)
- [ ] Groq API key obtained
- [ ] Firebase project configured (optional)
- [ ] Dependencies installed and tested locally

## Environment Variables Required

```bash
MONGO_URI=mongodb://localhost:27017/beamdb  # or MongoDB Atlas URI
GROQ_API_KEY=your-groq-api-key
SECRET_KEY=your-secret-key-min-32-chars
FLASK_DEBUG=False
PORT=5000  # Usually auto-set by platform
```

## Quick Deploy Commands

### Heroku

```bash
# 1. Login
heroku login

# 2. Create app
heroku create your-app-name

# 3. Set config vars
heroku config:set MONGO_URI="your-mongodb-uri"
heroku config:set GROQ_API_KEY="your-key"
heroku config:set SECRET_KEY="your-secret-key"

# 4. Deploy
git push heroku main

# 5. Open
heroku open
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

### Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: beam-calculator
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add Environment Variables
6. Deploy

## Testing Deployment

After deployment, test these endpoints:

- `GET /` - Should load the main page
- `POST /calculate` - Should process calculations
- `POST /chat` - Should respond with AI chat
- `GET /get_projects` - Should return saved projects (if any)

## Common Issues

### Issue: Application crashes on startup

**Solution**: Check logs for missing environment variables or MongoDB connection errors.

### Issue: MongoDB connection fails

**Solution**: 
- Verify MONGO_URI is correct
- For Atlas: Check IP whitelist includes 0.0.0.0/0
- Verify database user credentials

### Issue: Groq API errors

**Solution**:
- Verify GROQ_API_KEY is set correctly
- Check API quota/limits in Groq dashboard

### Issue: Static files not loading

**Solution**: Ensure Flask is configured to serve static files (default behavior).

## Post-Deployment

1. Test all features
2. Monitor logs for errors
3. Set up monitoring/alerting (optional)
4. Configure custom domain (optional)
5. Enable HTTPS (usually automatic on platforms)

## Scaling

For high traffic:
- Use multiple Gunicorn workers: `gunicorn -w 4 app:app`
- Consider MongoDB Atlas for better performance
- Use CDN for static assets (optional)
- Enable caching (optional)

