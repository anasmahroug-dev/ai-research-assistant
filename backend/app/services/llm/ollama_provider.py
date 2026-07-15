"""
import ollama
import os

from app.services.llm.base import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    def stream_chat(self, prompt: str):
        
        stream = ollama.chat(model=os.getenv("OLLAMA_MODEL"), 
                             messages=[{"role": "user",
                                        "content": prompt}],
                             stream=True)
        for chunk in stream:
            yield chunk["message"]["content"]
"""

