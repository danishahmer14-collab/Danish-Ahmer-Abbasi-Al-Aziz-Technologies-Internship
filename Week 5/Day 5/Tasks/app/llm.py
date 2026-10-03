from openai import OpenAI

from app.config import Settings


class LLM:
    def __init__(self, s: Settings):
        self.client = OpenAI(api_key=s.llm_api_key, base_url=s.llm_base_url)
        self.model = s.llm_model

    def generate(self, system: str, user: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return r.choices[0].message.content or ""