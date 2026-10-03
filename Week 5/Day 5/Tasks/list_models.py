from openai import OpenAI
from app.config import get_settings

s = get_settings()
print("Using:", s.llm_base_url)
client = OpenAI(api_key=s.llm_api_key, base_url=s.llm_base_url)
for m in client.models.list().data:
    print(m.id)