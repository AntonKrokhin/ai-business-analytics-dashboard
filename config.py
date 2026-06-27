import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

REQUIRED_COLUMNS = ["price"]
OPTIONAL_COLUMNS = [
    "date",
    "session_id",
    "ga_session_id",
    "continent",
    "country",
    "device",
    "browser",
    "operating_system",
    "traffic_channel",
    "traffic_source",
    "product_category",
    "registered_user_id",
    "is_verified",
    "is_unsubscribed",
]
