from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.routes.slides import router as slides_router
from app.core.redis_client import RedisClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan: startup and shutdown."""
    # Startup: Initialize Redis connection
    try:
        await RedisClient.get_client()
        print("Redis connected successfully")
    except Exception as e:
        print(f"Redis connection failed: {e}. Rate limiting may not work.")

    yield

    # Shutdown: Close Redis connection
    try:
        await RedisClient.close()
        print("Redis connection closed")
    except Exception as e:
        print(f"Error closing Redis: {e}")


app = FastAPI(
    title="AI Slide Generator API",
    lifespan=lifespan
)

app.include_router(slides_router, prefix="/api/v1/slides", tags=["Slides"])


@app.get("/")
async def root():
    return {"message": "Hello World"}