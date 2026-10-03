from openai import OpenAI
from app.config import get_settings

s = get_settings()
client = OpenAI(api_key=s.llm_api_key, base_url=s.llm_base_url)
r = client.chat.completions.create(
    model=s.llm_model,
    messages=[{"role": "user", "content": "Say hello in five words."}],
)
print(r.choices[0].message.content)