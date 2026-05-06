import httpx
from .base import LLMProvider
from app.core.config import settings

class DeepSeekProvider(LLMProvider):
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        if not settings.DEEPSEEK_API_KEY:
            # Mock response for development if no API key is provided
            return f"Mock Response: I am Kazi, your HR assistant. System Prompt: {system_prompt} User Prompt: {user_prompt}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
