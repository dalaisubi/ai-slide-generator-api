"""Mock LLM adapter for testing and fallback."""

from typing import List, Dict
from app.services.llm.base import LLMAdapter


class MockAdapter(LLMAdapter):
    """Mock adapter that generates placeholder content."""
    
    async def generate_slides(self, topic: str, num_slides: int) -> List[Dict[str, any]]:
        """Generate mock slide content."""
        slides = []
        for i in range(num_slides):
            slides.append(self._create_slide(topic, i + 1))
        return slides
    
    def _create_slide(self, topic: str, slide_num: int) -> Dict:
        """Creates a single mock slide with consistent structure."""
        return {
            "title": f"{topic} - Slide {slide_num}",
            "bullets": [
                f"Key idea {slide_num}.1 about {topic}",
                f"Key idea {slide_num}.2 about {topic}",
                f"Key idea {slide_num}.3 about {topic}",
            ],
            "citation": "Generated using LLM (Mock)"
        }

