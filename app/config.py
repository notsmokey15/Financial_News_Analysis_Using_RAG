import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not NEWS_API_KEY or not GROQ_API_KEY:
    raise ValueError("API keys for NewsAPI or Groq are not set in the .env file.")
