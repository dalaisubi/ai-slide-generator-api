"""LLM service using adapter pattern for multiple AI providers."""

from app.services.llm.factory import LLMAdapterFactory


async def generate_slide_content(topic: str, num_slides: int):
    """
    Generates slide content using configured LLM provider.
    Returns list of slides with title, bullets, and citation - same structure always.

    Uses adapter pattern to support multiple AI providers (OpenAI, Mock, etc.)
    """
    adapter = LLMAdapterFactory.create_adapter_with_fallback()

    try:
        return await adapter.generate_slides(topic, num_slides)
    except Exception as e:
        print(f"LLM generation failed: {str(e)}, falling back to mock")
        # Fallback to mock adapter on any error
        mock_adapter = LLMAdapterFactory.create_adapter("mock")
        return await mock_adapter.generate_slides(topic, num_slides)