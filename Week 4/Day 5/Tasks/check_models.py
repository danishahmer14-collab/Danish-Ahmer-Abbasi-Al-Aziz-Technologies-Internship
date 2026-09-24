import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
models = response.json().get("data", [])

print("--- AVAILABLE MODELS FOR YOUR KEY ---")
for model in models:
    # Filter out whisper (audio) and guard (moderation) models
    if "whisper" not in model["id"] and "guard" not in model["id"]:
        print(model["id"])