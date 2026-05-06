import httpx
from .base import LLMProvider
from app.core.config import settings

class DeepSeekProvider(LLMProvider):
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        api_key = settings.DEEPSEEK_API_KEY
        if api_key:
            api_key = api_key.strip("'\"")
            
        if not api_key or api_key == "your_key_here":
            # Mock response for development if no API key is provided
            return f"Mock Response: I am Kazi, your HR assistant. System Prompt: {system_prompt} User Prompt: {user_prompt}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
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
