# 🚀 DEPLOY NOW - Simple Instructions

## Easiest Method: Render (No CLI Needed!)

### Step 1: Push to GitHub
```bash
# If you haven't already
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Render (5 minutes)

1. Go to https://render.com
2. Sign up/Login (free)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: beam-calculator (or any name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add Environment Variables:
   - `MONGO_URI` = your MongoDB URI
   - `GROQ_API_KEY` = your Groq API key
   - `SECRET_KEY` = any random string (32+ chars)
   - `FLASK_DEBUG` = False
7. Click **"Create Web Service"**
8. **DONE!** Your app will be live in 2-3 minutes

## Alternative: Railway (Also Easy)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Add environment variables (same as above)
6. **DONE!** Auto-deploys on every push

## Quick Setup for .env (Local Testing)

If you want to test locally first:

1. Copy `env.example.txt` to `.env`
2. Edit `.env` and add your actual values:
   ```env
   MONGO_URI=mongodb://localhost:27017/beamdb
   GROQ_API_KEY=your-actual-groq-key
   SECRET_KEY=any-random-string-32-chars-minimum
   FLASK_DEBUG=False
   ```
3. Run: `python app.py`

## Need MongoDB?

### Option 1: MongoDB Atlas (Free Cloud)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create cluster (free tier)
4. Get connection string
5. Use it as `MONGO_URI`

### Option 2: Local MongoDB
- Windows: Download from mongodb.com
- Install and start service
- Use: `mongodb://localhost:27017/beamdb`

## Need Groq API Key?

1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy and use in environment variables

---

**That's it! Your app will be live in minutes! 🎉**

