import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/beamdb")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
