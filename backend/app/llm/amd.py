from .base import LLMProvider

class AMDProvider(LLMProvider):
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        # Placeholder for AMD-hosted Qwen via Hugging Face Transformers
        return "AMD Provider: Qwen model execution on AMD hardware is not yet implemented."
