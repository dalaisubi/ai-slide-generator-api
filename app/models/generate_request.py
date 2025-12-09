from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3)
    num_slides: int = Field(..., ge=1, le=20)