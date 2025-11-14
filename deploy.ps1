# Automatic Deployment Script for Beam Load Calculator (PowerShell)
# Supports: Heroku, Railway

Write-Host "🚀 Starting automatic deployment..." -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item env.example.txt .env
    Write-Host "📝 Please update .env with your configuration before deploying." -ForegroundColor Yellow
    exit 1
}

# Load environment variables from .env
$envVars = @{}
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

# Check required variables
if (-not $envVars.MONGO_URI -or -not $envVars.GROQ_API_KEY) {
    Write-Host "❌ Error: MONGO_URI and GROQ_API_KEY must be set in .env" -ForegroundColor Red
    exit 1
}

# Detect deployment platform
$deployPlatform = $null

if (Get-Command heroku -ErrorAction SilentlyContinue) {
    Write-Host "📦 Detected Heroku CLI" -ForegroundColor Cyan
    $deployPlatform = "heroku"
}
elseif (Get-Command railway -ErrorAction SilentlyContinue) {
    Write-Host "📦 Detected Railway CLI" -ForegroundColor Cyan
    $deployPlatform = "railway"
}
else {
    Write-Host "⚠️  No deployment platform detected. Please install Heroku or Railway CLI." -ForegroundColor Yellow
    Write-Host "   Heroku: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    Write-Host "   Railway: npm i -g @railway/cli" -ForegroundColor Yellow
    exit 1
}

# Deploy based on platform
switch ($deployPlatform) {
    "heroku" {
        Write-Host "🚀 Deploying to Heroku..." -ForegroundColor Green
        
        # Check if logged in
        try {
            heroku apps:info 2>&1 | Out-Null
        }
        catch {
            Write-Host "📱 Please login to Heroku first: heroku login" -ForegroundColor Yellow
            exit 1
        }
        
        # Check if app exists
        $appExists = $false
        try {
            heroku apps:info 2>&1 | Out-Null
            $appExists = $true
        }
        catch {
            Write-Host "📱 Creating new Heroku app..." -ForegroundColor Cyan
            heroku create
        }
        
        # Set environment variables
        Write-Host "🔧 Setting environment variables..." -ForegroundColor Cyan
        heroku config:set "MONGO_URI=$($envVars.MONGO_URI)"
        heroku config:set "GROQ_API_KEY=$($envVars.GROQ_API_KEY)"
        
        if ($envVars.SECRET_KEY) {
            heroku config:set "SECRET_KEY=$($envVars.SECRET_KEY)"
        } else {
            $secretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
            heroku config:set "SECRET_KEY=$secretKey"
        }
        
        heroku config:set "FLASK_DEBUG=False"
        
        # Deploy
        Write-Host "📤 Pushing to Heroku..." -ForegroundColor Cyan
        git push heroku main
        if ($LASTEXITCODE -ne 0) {
            git push heroku master
        }
        
        Write-Host "✅ Deployment complete!" -ForegroundColor Green
        heroku open
    }
    
    "railway" {
        Write-Host "🚀 Deploying to Railway..." -ForegroundColor Green
        
        # Set environment variables
        railway variables set "MONGO_URI=$($envVars.MONGO_URI)"
        railway variables set "GROQ_API_KEY=$($envVars.GROQ_API_KEY)"
        
        if ($envVars.SECRET_KEY) {
            railway variables set "SECRET_KEY=$($envVars.SECRET_KEY)"
        }
        
        railway variables set "FLASK_DEBUG=False"
        
        # Deploy
        railway up
        
        Write-Host "✅ Deployment complete!" -ForegroundColor Green
    }
}

Write-Host "🎉 All done!" -ForegroundColor Green

