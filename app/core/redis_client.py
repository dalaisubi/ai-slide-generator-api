"""Redis client configuration and connection management."""

import redis.asyncio as aioredis
from typing import Optional
from app.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB


class RedisClient:
    """Singleton Redis client for the application."""

    _instance: Optional[aioredis.Redis] = None
    _connection_pool: Optional[aioredis.ConnectionPool] = None

    @classmethod
    async def get_client(cls) -> aioredis.Redis:
        """Get or create Redis client instance."""
        if cls._instance is None:
            cls._connection_pool = aioredis.ConnectionPool(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD if REDIS_PASSWORD else None,
                db=REDIS_DB,
                decode_responses=True,
                max_connections=50
            )
            cls._instance = aioredis.Redis(connection_pool=cls._connection_pool)
        else:
            # Check if connection is still alive
            try:
                await cls._instance.ping()
            except Exception:
                # Connection lost, recreate
                if cls._connection_pool:
                    await cls._connection_pool.disconnect()
                cls._connection_pool = aioredis.ConnectionPool(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    password=REDIS_PASSWORD if REDIS_PASSWORD else None,
                    db=REDIS_DB,
                    decode_responses=True,
                    max_connections=50
                )
                cls._instance = aioredis.Redis(connection_pool=cls._connection_pool)
        return cls._instance

    @classmethod
    async def close(cls):
        """Close Redis connection."""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
        if cls._connection_pool:
            await cls._connection_pool.disconnect()
            cls._connection_pool = None