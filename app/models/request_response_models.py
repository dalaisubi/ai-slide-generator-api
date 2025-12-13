from pydantic import BaseModel, Field
from typing import List, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')

class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3)
    num_slides: int = Field(..., ge=1, le=20)

class Slide(BaseModel):
    title: str
    bullets: List[str] = []
    citation: str = ""

class BaseResponse(BaseModel, Generic[T]):
    """Reusable base response model"""
    request_id: str
    status: str
    message: str
    data: T
    timestamp: str

class PresentationData(BaseModel):
    title: str
    slides: List[Slide]

class PresentationResponse(BaseResponse[PresentationData]):
    """Response for generate endpoint"""
    num_slides: int

class ExportRequest(BaseModel):
    title: str
    slides: List[Slide]

class ExportData(BaseModel):
    """Data for export response"""
    file_name: str
    file_path: str
    download_url: str
    title: str
    num_slides: int

class ExportResponse(BaseResponse[ExportData]):
    """Response for export endpoint"""
    pass