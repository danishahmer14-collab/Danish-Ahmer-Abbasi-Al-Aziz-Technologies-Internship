import json
import os
from dotenv import load_dotenv
from groq import Groq
from tools import TOOL_SCHEMAS, run_tool

load_dotenv()

client = Groq()
MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
MAX_STEPS = 5

SYSTEM_PROMPT = (
    "You are a helpful assistant for a small store. "
    "Use the tools when you need live weather or product data. "
    "Never invent data - if a tool returns an error, tell the user honestly."
)

def run_agent(user_message: str) -> tuple[str, list[str]]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    tools_used: list[str] = []

    for _ in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            max_tokens=1024,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content or "", tools_used

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        })

        for tc in msg.tool_calls:
            tools_used.append(tc.function.name)
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            output = run_tool(tc.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(output),
            })

    return "Sorry, I couldn't finish within the step limit.", tools_used