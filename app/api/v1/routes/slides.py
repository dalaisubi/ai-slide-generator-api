from fastapi import APIRouter, HTTPException
from app.models.generate_request import GenerateRequest
from app.services.llm_service import generate_slide_content

router = APIRouter()

@router.post("/generate")
async def generate_slides(payload: GenerateRequest):
    """
    Generates slide content using LLM (mock or real).
    """
    try:
        slides = await generate_slide_content(payload.topic, payload.num_slides)
        return {
            "topic": payload.topic,
            "num_slides": payload.num_slides,
            "slides": slides
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))