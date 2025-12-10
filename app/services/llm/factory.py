"""Factory for creating LLM adapter instances."""

from typing import Optional
from app.services.llm.base import LLMAdapter
from app.services.llm.openai_adapter import OpenAIAdapter
from app.services.llm.gemini_adapter import GeminiAdapter
from app.services.llm.mock_adapter import MockAdapter
from app.settings import (
    LLM_PROVIDER, OPENAI_API_KEY, OPENAI_MODEL,
    GEMINI_API_KEY, GEMINI_MODEL
)


class LLMAdapterFactory:
    """Factory to create appropriate LLM adapter based on configuration."""
    
    @staticmethod
    def create_adapter(provider: Optional[str] = None) -> LLMAdapter:
        """
        Create an LLM adapter instance based on provider.
        
        Args:
            provider: Provider name (openai, gemini, mock). If None, uses settings.
            
        Returns:
            LLMAdapter instance
        """
        provider = provider or LLM_PROVIDER
        
        if provider == "openai":
            try:
                return OpenAIAdapter(api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
            except ValueError:
                print("OpenAI API key not found, falling back to mock")
                return MockAdapter()
        elif provider == "gemini":
            try:
                return GeminiAdapter(api_key=GEMINI_API_KEY, model=GEMINI_MODEL)
            except ValueError:
                print("Gemini API key not found, falling back to mock")
                return MockAdapter()
        elif provider == "mock":
            return MockAdapter()
        else:
            # Default to mock for unknown providers
            print(f"Unknown provider '{provider}', using mock adapter")
            return MockAdapter()
    
    @staticmethod
    def create_adapter_with_fallback() -> LLMAdapter:
        """
        Create adapter with automatic fallback to mock if primary fails.
        
        Returns:
            LLMAdapter instance (with fallback logic)
        """
        provider = LLM_PROVIDER
        
        if provider == "openai" and OPENAI_API_KEY:
            try:
                return OpenAIAdapter(api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
            except Exception as e:
                print(f"Failed to create OpenAI adapter: {e}, using mock")
                return MockAdapter()
        elif provider == "gemini" and GEMINI_API_KEY:
            try:
                return GeminiAdapter(api_key=GEMINI_API_KEY, model=GEMINI_MODEL)
            except Exception as e:
                print(f"Failed to create Gemini adapter: {e}, using mock")
                return MockAdapter()
        
        return MockAdapter()

