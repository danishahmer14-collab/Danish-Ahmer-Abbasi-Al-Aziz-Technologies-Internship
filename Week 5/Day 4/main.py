import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is missing. Copy .env.example to .env and set it.")

from agent import run_agent

app = FastAPI(
    title="AI Agent API",
    description="An AI agent that can check live weather and search a product database.",
    version="1.0.0",
)

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, examples=["What's the weather in Lahore?"])

class ChatResponse(BaseModel):
    answer: str
    tools_used: list[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        answer, tools_used = run_agent(req.message)
        return ChatResponse(answer=answer, tools_used=tools_used)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")