class LLMProvider:
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError

    async def embed(self, text: str):
        raise NotImplementedError
