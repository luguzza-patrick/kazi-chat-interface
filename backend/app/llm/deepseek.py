import httpx
from .base import LLMProvider
from app.core.config import settings

class DeepSeekProvider(LLMProvider):
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        api_key = settings.DEEPSEEK_API_KEY
        if api_key:
            api_key = api_key.strip("'\"")
            
        # If no API key and not using the default DeepSeek URL, assume it's a local/unauthenticated endpoint
        is_custom_url = settings.DEEPSEEK_BASE_URL != "https://api.deepseek.com/v1"
        
        if not api_key and not is_custom_url:
            # Cleaner mock response for testing if no key and using default URL
            return f"[MOCK] Kazi: I've processed your request. Based on the context provided, here is the answer to '{user_prompt}'."

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                headers=headers,
                json={
                    "model": settings.LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
