"""Application settings and utility functions."""

from datetime import datetime, timezone

def get_current_timestamp() -> str:
    """Returns current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()

