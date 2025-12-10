"""Google Gemini LLM adapter implementation."""

import asyncio
import json
from typing import List, Dict

import google.generativeai as genai

from app.services.llm.base import LLMAdapter
from app.settings import GEMINI_API_KEY, GEMINI_MODEL


class GeminiAdapter(LLMAdapter):
    """Adapter for Google Gemini API."""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model or GEMINI_MODEL
        
        if not self.api_key:
            raise ValueError("Gemini API key is required")
    
    async def generate_slides(self, topic: str, num_slides: int) -> List[Dict[str, any]]:
        """Generate slides using Google Gemini API."""
        try:
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Try to get the model, with fallback to available models
            try:
                model = genai.GenerativeModel(self.model)
            except Exception as model_error:
                # If model not found, try to list available models and use a fallback
                print(f"Model {self.model} not found: {model_error}")
                print("Attempting to use gemini-1.5-flash as fallback...")
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                except:
                    try:
                        model = genai.GenerativeModel("gemini-1.0-pro")
                    except:
                        # List available models for debugging
                        try:
                            available_models = [m.name for m in genai.list_models()]
                            print(f"Available models: {available_models}")
                        except:
                            pass
                        raise ValueError(f"Could not find a valid Gemini model. Tried: {self.model}, gemini-1.5-flash, gemini-1.0-pro")
            
            prompt = self._create_prompt(topic, num_slides)
            
            # Generate content (run sync method in executor for async compatibility)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(prompt)
            )
            
            content = response.text.strip()
            content = self.clean_json_content(content)
            
            slides_data = json.loads(content)
            
            return self.normalize_slides(slides_data, topic, num_slides)
            
        except json.JSONDecodeError as e:
            print(f"Gemini JSON parsing error: {str(e)}")
            raise
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            raise
    
    def _create_prompt(self, topic: str, num_slides: int) -> str:
        """Create the prompt for Gemini."""
        return f"""Generate exactly {num_slides} presentation slides about "{topic}".

For each slide, provide:
1. A clear, concise title
2. 3-5 bullet points with key information
3. A citation/source reference

Return ONLY a valid JSON array with this exact structure (no markdown, no explanations):
[
  {{
    "title": "Slide Title Here",
    "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3"],
    "citation": "Source citation here"
  }},
  {{
    "title": "Next Slide Title",
    "bullets": ["Point 1", "Point 2", "Point 3"],
    "citation": "Source citation"
  }}
]

Generate exactly {num_slides} slides. Make content informative and relevant."""

