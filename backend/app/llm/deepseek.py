import httpx
from .base import LLMProvider
from app.core.config import settings

class DeepSeekProvider(LLMProvider):
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        api_key = settings.DEEPSEEK_API_KEY
        if api_key:
            api_key = api_key.strip("'\"")
            
        print(f"DEBUG: API Key loaded, length: {len(api_key) if api_key else 0}")

        if not api_key or api_key == "your_key_here":
            # Cleaner mock response for testing
            return f"[MOCK] Kazi: I've processed your request. Based on the context provided, here is the answer to '{user_prompt}'."

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
