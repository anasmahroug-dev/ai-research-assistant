import os 

from app.services.llm.ollama_provider import OllamaProvider
from app.services.llm.groq_provider import GroqProvider

def get_llm_provider():
    provider = os.getenv("LLM_PROVIDER", "ollama")
    
    if provider == "groq":
        return GroqProvider()
    
    return OllamaProvider()
    