"""Redis-based sliding window rate limiter using Sorted Sets."""

import time
import uuid
from typing import Tuple, Optional
import redis.asyncio as aioredis
from app.core.redis_client import RedisClient


class RateLimiter:
    """
    Sliding window rate limiter using Redis Sorted Sets.
    
    Uses Redis ZSET operations.
    """
    
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    async def is_allowed(
        self,
        identifier: str,
        endpoint: Optional[str] = None
    ) -> Tuple[bool, int, int]:
        """
        Check if request is allowed based on rate limit.
        
        Uses Redis Sorted Sets (ZSET) for sliding window:
        1. Remove old entries outside the window
        2. Count current entries
        3. Add new entry if under limit
        4. Set expiry for cleanup
        
        Args:
            identifier: Unique identifier (e.g., IP address, user ID, API key)
            endpoint: Optional endpoint name for endpoint-specific limits
            
        Returns:
            Tuple of (is_allowed: bool, remaining: int, reset_in: int)
            - is_allowed: True if request is allowed, False if rate limited
            - remaining: Number of requests remaining in current window
            - reset_in: Seconds until rate limit resets
        """
        redis_client = await RedisClient.get_client()

        # Create unique key for this identifier and endpoint
        if endpoint:
            key = f"rate_limit:{endpoint}:{identifier}"
        else:
            key = f"rate_limit:{identifier}"

        now = time.time()
        window_start = now - self.window_seconds
        request_id = str(uuid.uuid4())

        try:
            # Use pipeline for better performance (batches commands)
            pipe = redis_client.pipeline()

            # Step 1: Remove old entries outside the sliding window
            pipe.zremrangebyscore(key, 0, window_start)

            # Step 2: Count current entries in the window
            pipe.zcard(key)

            # Execute pipeline to get count
            results = await pipe.execute()
            count = results[1]  # zcard result

            # Step 3: Check if under limit
            if count < self.max_requests:
                # Add new request with current timestamp as score
                pipe = redis_client.pipeline()
                pipe.zadd(key, {request_id: now})
                # Set expiry for automatic cleanup (window + small buffer)
                pipe.expire(key, self.window_seconds + 10)
                await pipe.execute()

                remaining = self.max_requests - count - 1
                return True, remaining, self.window_seconds
            else:
                # Rate limit exceeded
                # Get oldest entry to calculate reset time
                oldest = await redis_client.zrange(key, 0, 0, withscores=True)
                reset_in = self.window_seconds

                if oldest and len(oldest) > 0:
                    oldest_timestamp = oldest[0][1]  # Score (timestamp)
                    reset_in = max(0, int((oldest_timestamp + self.window_seconds) - now))

                return False, 0, reset_in

        except Exception as e:
            # On Redis errors, allow request (fail open)
            # In production, you might want to log this and fail closed
            print(f"Rate limiter error: {e}, allowing request")
            return True, self.max_requests, self.window_seconds