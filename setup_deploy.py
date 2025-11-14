#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic Deployment Setup Script
Helps configure and deploy the Beam Load Calculator
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_file_exists(filepath):
    return Path(filepath).exists()

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if check_file_exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if check_file_exists('env.example.txt'):
        print("📝 Creating .env file from template...")
        with open('env.example.txt', 'r') as f:
            content = f.read()
        with open('.env', 'w') as f:
            f.write(content)
        print("✅ .env file created. Please update it with your values.")
        return False
    else:
        print("❌ env.example.txt not found")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("🔍 Checking dependencies...")
    try:
        import flask
        import flask_pymongo
        import groq
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_env_vars():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    from dotenv import load_dotenv
    load_dotenv()
    
    required = ['MONGO_URI', 'GROQ_API_KEY']
    missing = []
    
    for var in required:
        value = os.getenv(var)
        if not value or value.startswith('your-') or value.startswith('YOUR_'):
            missing.append(var)
    
    if missing:
        print(f"⚠️  Missing or placeholder values for: {', '.join(missing)}")
        print("   Please update .env file")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def detect_platform():
    """Detect which deployment platform CLI is available"""
    platforms = {
        'heroku': 'heroku',
        'railway': 'railway',
    }
    
    available = []
    for name, cmd in platforms.items():
        try:
            subprocess.run([cmd, '--version'], 
                         capture_output=True, 
                         check=True)
            available.append(name)
            print(f"✅ {name.capitalize()} CLI detected")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {name.capitalize()} CLI not found")
    
    return available

def deploy_heroku():
    """Deploy to Heroku"""
    print_header("Deploying to Heroku")
    
    # Check if logged in
    try:
        subprocess.run(['heroku', 'apps'], 
                      capture_output=True, 
                      check=True)
    except subprocess.CalledProcessError:
        print("❌ Not logged in to Heroku. Run: heroku login")
        return False
    
    # Get app name or create new
    result = subprocess.run(['heroku', 'apps:info'], 
                           capture_output=True, 
                           text=True)
    
    if result.returncode != 0:
        print("📱 Creating new Heroku app...")
        app_name = input("Enter app name (or press Enter for auto-generated): ").strip()
        if app_name:
            subprocess.run(['heroku', 'create', app_name], check=True)
        else:
            subprocess.run(['heroku', 'create'], check=True)
    
    # Set environment variables
    print("🔧 Setting environment variables...")
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = {
        'MONGO_URI': os.getenv('MONGO_URI'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'SECRET_KEY': os.getenv('SECRET_KEY') or os.urandom(32).hex(),
        'FLASK_DEBUG': 'False'
    }
    
    for key, value in env_vars.items():
        if value:
            subprocess.run(['heroku', 'config:set', f'{key}={value}'], check=True)
    
    # Deploy
    print("📤 Deploying to Heroku...")
    try:
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['git', 'push', 'heroku', 'master'], check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to push to Heroku")
            return False
    
    print("✅ Deployment complete!")
    subprocess.run(['heroku', 'open'])
    return True

def deploy_railway():
    """Deploy to Railway"""
    print_header("Deploying to Railway")
    
    # Check if logged in
    try:
        subprocess.run(['railway', 'whoami'], 
                      capture_output=True, 
                      check=True)
    except subprocess.CalledProcessError:
        print("❌ Not logged in to Railway. Run: railway login")
        return False
    
    # Set environment variables
    print("🔧 Setting environment variables...")
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = {
        'MONGO_URI': os.getenv('MONGO_URI'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'SECRET_KEY': os.getenv('SECRET_KEY') or os.urandom(32).hex(),
        'FLASK_DEBUG': 'False'
    }
    
    for key, value in env_vars.items():
        if value:
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
    
    # Deploy
    print("📤 Deploying to Railway...")
    subprocess.run(['railway', 'up'], check=True)
    
    print("✅ Deployment complete!")
    return True

def main():
    print_header("Beam Load Calculator - Deployment Setup")
    
    # Step 1: Create .env file
    env_created = create_env_file()
    if env_created:
        if not check_env_vars():
            print("\n⚠️  Please update .env file with your actual values")
            print("   Then run this script again.")
            return
    else:
        print("\n⚠️  Please update .env file with your actual values")
        print("   Then run this script again.")
        return
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install dependencies first: pip install -r requirements.txt")
        return
    
    # Step 3: Detect platform
    platforms = detect_platform()
    
    if not platforms:
        print("\n❌ No deployment platform detected.")
        print("   Please install Heroku CLI or Railway CLI")
        print("   Heroku: https://devcenter.heroku.com/articles/heroku-cli")
        print("   Railway: npm i -g @railway/cli")
        return
    
    # Step 4: Choose platform
    if len(platforms) == 1:
        platform = platforms[0]
    else:
        print("\n📦 Multiple platforms detected. Choose one:")
        for i, p in enumerate(platforms, 1):
            print(f"   {i}. {p.capitalize()}")
        choice = input("\nEnter choice (1-{}): ".format(len(platforms))).strip()
        try:
            platform = platforms[int(choice) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid choice")
            return
    
    # Step 5: Deploy
    if platform == 'heroku':
        deploy_heroku()
    elif platform == 'railway':
        deploy_railway()
    else:
        print(f"❌ Unknown platform: {platform}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

