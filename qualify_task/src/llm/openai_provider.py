from openai import AsyncOpenAI
from src.auxiliary.config import OPENAI_API_KEY, DEFAULT_LLM_MODEL
from src.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate(self, prompt):
        resp = await self.client.responses.create(model=DEFAULT_LLM_MODEL, input=prompt)
        return resp.output_text
