import os
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.llm_service import generate_slide_content
from app.models.request_response_models import (
    GenerateRequest, ExportRequest, ExportResponse, 
    ExportData, PresentationResponse, PresentationData, Slide
)
from app.services.pptx_service import PPTXService
from app.settings import get_current_timestamp


router = APIRouter()

OUTPUT_DIR = "app/generated_pptx"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/generate", response_model=PresentationResponse)
async def generate_slides(payload: GenerateRequest):
    """
    Generates slide content using LLM (mock or real).
    """
    request_id = str(uuid.uuid4())
    try:
        slides_data = await generate_slide_content(payload.topic, payload.num_slides)
        slides = [Slide(**slide) for slide in slides_data]

        return PresentationResponse(
            request_id=request_id,
            status="success",
            message=f"Successfully generated {len(slides)} slides for topic: {payload.topic}",
            data=PresentationData(
                title=payload.topic,
                slides=slides
            ),
            num_slides=len(slides),
            timestamp=get_current_timestamp()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "request_id": request_id,
                "status": "error",
                "message": f"Failed to generate slides: {str(e)}",
                "timestamp": get_current_timestamp()
            }
        )



@router.post("/export", response_model=ExportResponse)
async def export_slides(req: ExportRequest):
    """
    Exports slides to PowerPoint format and returns file information.
    """
    request_id = str(uuid.uuid4())
    try:
        file_name = f"{uuid.uuid4()}.pptx"
        safe_title = req.title.replace(' ', '_').replace('/', '_')
        path = f"{OUTPUT_DIR}/{file_name}"

        PPTXService.create_pptx(req.title, req.slides, path)

        return ExportResponse(
            request_id=request_id,
            status="success",
            message=f"Successfully exported {len(req.slides)} slides to PowerPoint format",
            data=ExportData(
                file_name=file_name,
                file_path=path,
                download_url=f"/api/v1/slides/download/{file_name}",
                title=req.title,
                num_slides=len(req.slides)
            ),
            timestamp=get_current_timestamp()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "request_id": request_id,
                "status": "error",
                "message": f"Failed to export slides: {str(e)}",
                "timestamp": get_current_timestamp()
            }
        )


@router.get("/download/{file_name}")
async def download_file(file_name: str):
    """
    Downloads the generated PowerPoint file.

    TODO: S3 storage for files
    """
    file_path = f"{OUTPUT_DIR}/{file_name}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Sanitize filename for download
    safe_filename = file_name.replace(' ', '_')

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=safe_filename,
        headers={
            "Content-Disposition": f"attachment; filename={safe_filename}"
        }
    )