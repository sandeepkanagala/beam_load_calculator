#!/bin/bash

# Automatic Deployment Script for Beam Load Calculator
# Supports: Heroku, Railway, Render

set -e

echo "🚀 Starting automatic deployment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example.txt .env
    echo "📝 Please update .env with your configuration before deploying."
    exit 1
fi

# Load environment variables
source .env

# Check required variables
if [ -z "$MONGO_URI" ] || [ -z "$GROQ_API_KEY" ]; then
    echo "❌ Error: MONGO_URI and GROQ_API_KEY must be set in .env"
    exit 1
fi

# Detect deployment platform
if command -v heroku &> /dev/null; then
    echo "📦 Detected Heroku CLI"
    DEPLOY_PLATFORM="heroku"
elif command -v railway &> /dev/null; then
    echo "📦 Detected Railway CLI"
    DEPLOY_PLATFORM="railway"
else
    echo "⚠️  No deployment platform detected. Please install Heroku or Railway CLI."
    echo "   Heroku: https://devcenter.heroku.com/articles/heroku-cli"
    echo "   Railway: npm i -g @railway/cli"
    exit 1
fi

# Deploy based on platform
case $DEPLOY_PLATFORM in
    heroku)
        echo "🚀 Deploying to Heroku..."
        
        # Check if app exists
        if ! heroku apps:info &> /dev/null; then
            echo "📱 Creating new Heroku app..."
            heroku create
        fi
        
        # Set environment variables
        echo "🔧 Setting environment variables..."
        heroku config:set MONGO_URI="$MONGO_URI"
        heroku config:set GROQ_API_KEY="$GROQ_API_KEY"
        heroku config:set SECRET_KEY="${SECRET_KEY:-$(openssl rand -hex 32)}"
        heroku config:set FLASK_DEBUG="False"
        
        # Deploy
        echo "📤 Pushing to Heroku..."
        git push heroku main || git push heroku master
        
        echo "✅ Deployment complete!"
        heroku open
        ;;
        
    railway)
        echo "🚀 Deploying to Railway..."
        
        # Set environment variables
        railway variables set MONGO_URI="$MONGO_URI"
        railway variables set GROQ_API_KEY="$GROQ_API_KEY"
        railway variables set SECRET_KEY="${SECRET_KEY:-$(openssl rand -hex 32)}"
        railway variables set FLASK_DEBUG="False"
        
        # Deploy
        railway up
        
        echo "✅ Deployment complete!"
        ;;
esac

echo "🎉 All done!"

