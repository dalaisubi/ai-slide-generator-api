"""Application settings and utility functions."""

import os
from datetime import datetime, timezone

def get_current_timestamp() -> str:
    """Returns current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # Options: openai, gemini, mock

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Auto-detect provider if API key is set
if LLM_PROVIDER == "mock":
    if GEMINI_API_KEY:
        LLM_PROVIDER = "gemini"
    elif OPENAI_API_KEY:
        LLM_PROVIDER = "openai"

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# Rate Limiting Configuration
RATE_LIMIT_GENERATE = int(os.getenv("RATE_LIMIT_GENERATE", "10"))  # requests per window
RATE_LIMIT_EXPORT = int(os.getenv("RATE_LIMIT_EXPORT", "30"))
RATE_LIMIT_DOWNLOAD = int(os.getenv("RATE_LIMIT_DOWNLOAD", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds