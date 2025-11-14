# 🏗️ Structural Beam Load Calculator

A comprehensive web application for structural engineering calculations including Shear Force Diagrams (SFD), Bending Moment Diagrams (BMD), deflection analysis, stress checks, and AI-powered suggestions.

## Features

- **Load Analysis**: Supports multiple load types (Point Load, UDL, UVL, Moment)
- **Visualizations**: Interactive SFD, BMD, and Deflection diagrams
- **Stress & Deflection Checks**: Automatic validation against design limits
- **Cost Estimation**: Material cost calculations (concrete, steel, binding wire)
- **AI-Powered Suggestions**: Groq-powered chatbot and engineering recommendations
- **Firebase Authentication**: Secure user authentication
- **Data Persistence**: MongoDB integration for saving projects

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **AI**: Groq API (LangChain)
- **Authentication**: Firebase
- **Deployment**: Gunicorn

## 🚀 Quick Automatic Deployment

**Fastest way to deploy:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automatic deployment script
python setup_deploy.py
```

The script will guide you through the entire deployment process automatically!

**Or use platform-specific scripts:**
- Linux/Mac: `./deploy.sh`
- Windows: `.\deploy.ps1`

**For GitHub Actions (automatic on push):** See `QUICK_DEPLOY.md`

## Prerequisites

- Python 3.11+
- MongoDB (local or Atlas)
- Groq API Key
- Firebase Project (optional, for authentication)
- Heroku CLI or Railway CLI (for automatic deployment)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd beam_load_calculator_final
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/beamdb
# Or for MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/beamdb

# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
FLASK_DEBUG=False
PORT=5000

# Groq API Configuration
GROQ_API_KEY=your-groq-api-key

# Firebase Configuration (Optional)
# FIREBASE_CREDENTIALS=path/to/firebase-service-account.json
```

### 5. Configure Firebase (Frontend)

Update `static/auth.js` with your Firebase configuration:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Deployment

### Option 1: Heroku Deployment

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create Heroku App**:
```bash
heroku create your-app-name
```

3. **Set Environment Variables**:
```bash
heroku config:set MONGO_URI="your-mongodb-atlas-uri"
heroku config:set GROQ_API_KEY="your-groq-api-key"
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set FLASK_DEBUG="False"
```

4. **Add MongoDB Atlas Addon** (if not using external MongoDB):
```bash
heroku addons:create mongolab:sandbox
```

5. **Deploy**:
```bash
git push heroku main
```

6. **Open your app**:
```bash
heroku open
```

### Option 2: Railway Deployment

1. **Install Railway CLI**:
```bash
npm i -g @railway/cli
railway login
```

2. **Initialize Project**:
```bash
railway init
```

3. **Set Environment Variables** in Railway dashboard:
   - `MONGO_URI`
   - `GROQ_API_KEY`
   - `SECRET_KEY`
   - `PORT` (auto-set by Railway)

4. **Deploy**:
```bash
railway up
```

### Option 3: Render Deployment

1. **Create a new Web Service** on Render
2. **Connect your GitHub repository**
3. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. **Set Environment Variables** in Render dashboard
5. **Deploy**

### Option 4: DigitalOcean App Platform

1. **Create a new App** on DigitalOcean
2. **Connect GitHub repository**
3. **Configure**:
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `gunicorn app:app`
4. **Set Environment Variables**
5. **Deploy**

### Option 5: Local Production Setup

1. **Install Gunicorn** (already in requirements.txt)

2. **Run with Gunicorn**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **For production with Nginx** (optional):
   - Configure Nginx as reverse proxy
   - Use systemd to manage Gunicorn service

## MongoDB Setup

### Local MongoDB

1. **Install MongoDB**:
   - Windows: Download from [MongoDB website](https://www.mongodb.com/try/download/community)
   - Linux: `sudo apt-get install mongodb`
   - Mac: `brew install mongodb-community`

2. **Start MongoDB**:
```bash
# Windows
net start MongoDB

# Linux/Mac
sudo systemctl start mongod
# or
mongod
```

### MongoDB Atlas (Cloud)

1. **Create Account** at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. **Create Cluster** (Free tier available)
3. **Create Database User**
4. **Whitelist IP** (0.0.0.0/0 for all IPs)
5. **Get Connection String**:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/beamdb
   ```
6. **Update MONGO_URI** in `.env`

## API Keys Setup

### Groq API Key

1. **Sign up** at [Groq](https://console.groq.com/)
2. **Create API Key**
3. **Add to `.env`**: `GROQ_API_KEY=your-key`

### Firebase Setup (Optional)

1. **Create Firebase Project** at [Firebase Console](https://console.firebase.google.com/)
2. **Enable Authentication** (Email/Password and Google)
3. **Get Web App Config** and update `static/auth.js`
4. **For Backend Verification**:
   - Generate Service Account Key
   - Download JSON file
   - Set `FIREBASE_CREDENTIALS` environment variable to file path

## Project Structure

```
beam_load_calculator_final/
├── app.py                 # Main Flask application
├── beam_logic.py          # Beam calculation logic
├── chatbot.py             # AI chatbot implementation
├── suggestions.py         # AI suggestions using LangChain
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── Procfile               # Heroku deployment config
├── runtime.txt            # Python version
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── static/
│   ├── auth.js           # Firebase authentication
│   ├── app.js            # Main application logic
│   ├── script.js         # Form handling
│   ├── chart-script.js   # Chart visualizations
│   └── style.css         # Styles
└── templates/
    └── index.html        # Main HTML template
```

## API Endpoints

- `GET /` - Main application page
- `POST /calculate` - Calculate beam loads and analysis
- `POST /chat` - AI chatbot endpoint
- `POST /verify_token` - Firebase token verification
- `GET /get_projects` - Retrieve saved projects

## Troubleshooting

### MongoDB Connection Issues

- **Local**: Ensure MongoDB service is running
- **Atlas**: Check IP whitelist and credentials
- **Connection String**: Verify format is correct

### Groq API Errors

- Check API key is set correctly
- Verify API quota/limits
- Check internet connection

### Firebase Authentication

- Verify Firebase config in `static/auth.js`
- Check Firebase project settings
- Ensure authentication methods are enabled

### Port Already in Use

```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Kill process or change PORT in .env
```

## Development

### Running in Debug Mode

Set in `.env`:
```env
FLASK_DEBUG=True
```

### Testing Locally

1. Start MongoDB
2. Set environment variables
3. Run `python app.py`
4. Access at `http://localhost:5000`

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review deployment platform documentation

## Acknowledgments

- Groq for AI capabilities
- Firebase for authentication
- Chart.js for visualizations
- Flask community

---

**Made with ❤️ for Structural Engineers**

