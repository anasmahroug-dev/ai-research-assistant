from groq import Groq
import os

from app.services.llm.base import BaseLLMProvider


client = Groq(api_key=os.getenv("API_KEY"))

class GroqProvider(BaseLLMProvider):
    def stream_chat(self, prompt: str):
        stream = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[{"role": "user", "content":prompt}],
            stream=True
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta