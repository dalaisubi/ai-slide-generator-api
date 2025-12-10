"""OpenAI LLM adapter implementation."""

import json
from typing import List, Dict

from openai import AsyncOpenAI

from app.services.llm.base import LLMAdapter
from app.settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIAdapter(LLMAdapter):
    """Adapter for OpenAI API."""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    async def generate_slides(self, topic: str, num_slides: int) -> List[Dict[str, any]]:
        """Generate slides using OpenAI API."""
        try:
            client = AsyncOpenAI(api_key=self.api_key)
            
            prompt = self._create_prompt(topic, num_slides)
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional presentation content generator. Always return ONLY valid JSON arrays, no markdown formatting, no explanations."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content.strip()
            content = self.clean_json_content(content)
            
            slides_data = json.loads(content)
            
            return self.normalize_slides(slides_data, topic, num_slides)
            
        except json.JSONDecodeError as e:
            print(f"OpenAI JSON parsing error: {str(e)}")
            raise
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            raise
    
    def _create_prompt(self, topic: str, num_slides: int) -> str:
        """Create the prompt for OpenAI."""
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

