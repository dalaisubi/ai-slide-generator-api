"""Base abstract class for LLM adapters."""

from abc import ABC, abstractmethod
from typing import List, Dict


class LLMAdapter(ABC):
    """Abstract base class for LLM provider adapters."""
    
    @abstractmethod
    async def generate_slides(self, topic: str, num_slides: int) -> List[Dict[str, any]]:
        """
        Generate slide content using the LLM provider.
        
        Args:
            topic: The topic/subject for the slides
            num_slides: Number of slides to generate
            
        Returns:
            List of slide dictionaries with structure:
            [
                {
                    "title": str,
                    "bullets": List[str],
                    "citation": str
                }
            ]
        """
        pass
    
    @staticmethod
    def normalize_slides(slides_data: List[Dict], topic: str, num_slides: int) -> List[Dict]:
        """
        Normalize slide data to ensure consistent structure.
        
        Args:
            slides_data: Raw slide data from LLM
            topic: Topic for fallback content
            num_slides: Expected number of slides
            
        Returns:
            Normalized list of slides
        """
        # Ensure we have exactly the right number of slides
        if len(slides_data) < num_slides:
            # Pad with placeholder content if we got fewer slides
            def _create_placeholder_slide(slide_num: int) -> Dict:
                return {
                    "title": f"{topic} - Slide {slide_num}",
                    "bullets": [f"Key point about {topic}"],
                    "citation": "Generated using LLM"
                }
            for i in range(len(slides_data), num_slides):
                slides_data.append(_create_placeholder_slide(i + 1))
        elif len(slides_data) > num_slides:
            # Trim if we got more slides
            slides_data = slides_data[:num_slides]
        
        # Normalize structure to ensure consistent output
        normalized_slides = []
        for slide in slides_data:
            normalized_slides.append({
                "title": str(slide.get("title", f"{topic} - Slide")).strip(),
                "bullets": [
                    str(bullet).strip() 
                    for bullet in slide.get("bullets", slide.get("points", []))
                    if bullet
                ] or [f"Key point about {topic}"],
                "citation": str(slide.get("citation", "Generated using LLM")).strip()
            })
        
        return normalized_slides
    
    @staticmethod
    def clean_json_content(content: str) -> str:
        """Extract JSON from markdown code blocks if present."""
        content = content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return content.strip()

