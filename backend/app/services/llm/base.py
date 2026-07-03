from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def stream_chat(self, prompt: str):
        pass