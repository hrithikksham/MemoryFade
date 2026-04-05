import os
from dotenv import load_dotenv

load_dotenv()

def required(key: str):
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing environment variable: {key}")
    return value

GROQ_API_KEY = required("GROQ_API_KEY")

SUPABASE_URL = required("SUPABASE_URL")
SUPABASE_KEY = required("SUPABASE_KEY")

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

SIMILARITY_THRESHOLD = 0.4
TOP_K = 10
TOP_N = 3