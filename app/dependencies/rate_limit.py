"""Rate limiting dependencies for FastAPI routes."""

from fastapi import Request, HTTPException, Depends
from typing import Optional
from app.core.rate_limiter import RateLimiter
from app.settings import (
    RATE_LIMIT_GENERATE,
    RATE_LIMIT_EXPORT,
    RATE_LIMIT_DOWNLOAD,
    RATE_LIMIT_WINDOW
)


# Create rate limiter instances for each endpoint
generate_limiter = RateLimiter(RATE_LIMIT_GENERATE, RATE_LIMIT_WINDOW)
export_limiter = RateLimiter(RATE_LIMIT_EXPORT, RATE_LIMIT_WINDOW)
download_limiter = RateLimiter(RATE_LIMIT_DOWNLOAD, RATE_LIMIT_WINDOW)


def get_client_identifier(request: Request) -> str:
    """
    Get client identifier for rate limiting.
    Currently uses IP address. Can be extended to use API keys, user IDs, etc.

    Args:
        request: FastAPI request object

    Returns:
        Client identifier string
    """
    # Get client IP address
    client_ip = request.client.host if request.client else "unknown"

    # If behind proxy, check X-Forwarded-For header
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP (original client)
        client_ip = forwarded_for.split(",")[0].strip()
    print(f"Client IP: {client_ip}")
    print(f"Forwarded For: {forwarded_for}")
    return client_ip


async def rate_limit_dependency(
    request: Request,
    limiter: RateLimiter,
    endpoint: str
):
    """
    FastAPI dependency for rate limiting.
    
    Args:
        request: FastAPI request object
        limiter: RateLimiter instance
        endpoint: Endpoint name for logging/identification
        
    Raises:
        HTTPException: 429 if rate limit exceeded
    """
    identifier = get_client_identifier(request)
    
    is_allowed, remaining, reset_in = await limiter.is_allowed(identifier, endpoint)
    
    if not is_allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Please try again later.",
                "retry_after": reset_in,
                "limit": limiter.max_requests,
                "window": limiter.window_seconds
            },
            headers={
                "X-RateLimit-Limit": str(limiter.max_requests),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_in),
                "Retry-After": str(reset_in)
            }
        )
    
    # Add rate limit headers to successful responses
    # Note: FastAPI doesn't easily allow modifying response headers in dependencies
    # This would need to be done in the route handler or via middleware
    return {
        "remaining": remaining,
        "reset_in": reset_in
    }


# Convenience dependencies for each endpoint
async def rate_limit_generate(request: Request):
    """Rate limit dependency for /generate endpoint."""
    return await rate_limit_dependency(request, generate_limiter, "generate")


async def rate_limit_export(request: Request):
    """Rate limit dependency for /export endpoint."""
    return await rate_limit_dependency(request, export_limiter, "export")


async def rate_limit_download(request: Request):
    """Rate limit dependency for /download endpoint."""
    return await rate_limit_dependency(request, download_limiter, "download")

