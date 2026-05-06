from abc import ABC, abstractmethod
from typing import List, Dict

class LLMProvider(ABC):
    @abstractmethod
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        pass
