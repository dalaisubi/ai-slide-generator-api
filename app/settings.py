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