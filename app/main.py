from fastapi import FastAPI
from app.api.v1.routes.slides import router as slides_router

app = FastAPI(title="AI Slide Generator API")

app.include_router(slides_router, prefix="/api/v1/slides", tags=["Slides"])


@app.get("/")
async def root():
    return {"message": "Hello World"}