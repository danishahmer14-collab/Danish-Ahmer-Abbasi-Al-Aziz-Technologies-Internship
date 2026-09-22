import os
import sys
import time
import random
import json
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv
import anthropic
from anthropic import (
    APIStatusError,
    APIConnectionError,
    RateLimitError,
    InternalServerError,
)
from pydantic import BaseModel, ValidationError

load_dotenv()

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not API_KEY:
    sys.exit(
        "Missing ANTHROPIC_API_KEY.\n"
        "Set it in a .env file (ANTHROPIC_API_KEY=sk-ant-...) "
        "or export it in your shell before running this script."
    )

client = anthropic.Anthropic(api_key=API_KEY)

MODEL_FAST = "claude-haiku-4-5"
MODEL_DEFAULT = "claude-sonnet-4-6"

PRICING = {
    "claude-haiku-4-5":  {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
}

@dataclass
class UsageTracker:
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    calls: list = field(default_factory=list)

    def record(self, model: str, usage) -> None:
        input_tokens = usage.input_tokens
        output_tokens = usage.output_tokens
        price = PRICING.get(model, {"input": 0, "output": 0})
        cost = (input_tokens / 1_000_000) * price["input"] + \
               (output_tokens / 1_000_000) * price["output"]

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost_usd += cost
        self.calls.append(
            {"model": model, "input": input_tokens, "output": output_tokens, "cost": cost}
        )

    def summary(self) -> str:
        return (
            f"Calls: {len(self.calls)} | "
            f"Input tokens: {self.total_input_tokens} | "
            f"Output tokens: {self.total_output_tokens} | "
            f"Estimated cost: ${self.total_cost_usd:.6f}"
        )

usage_tracker = UsageTracker()

RETRYABLE_ERRORS = (RateLimitError, InternalServerError, APIConnectionError)

def call_with_retry(fn, max_retries: int = 5, base_delay: float = 1.0):
    for attempt in range(max_retries):
        try:
            return fn()
        except RETRYABLE_ERRORS as e:
            if attempt == max_retries - 1:
                raise
            wait = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"  [retry] {type(e).__name__} — waiting {wait:.1f}s "
                  f"(attempt {attempt + 1}/{max_retries})")
            time.sleep(wait)
        except APIStatusError as e:
            print(f"  [error] Non-retryable API error: {e.status_code} {e.message}")
            raise

def generate_text(prompt: str, model: str = MODEL_DEFAULT, system: Optional[str] = None) -> str:
    def _call():
        return client.messages.create(
            model=model,
            max_tokens=1024,
            system=system or "You are a helpful, concise assistant.",
            messages=[{"role": "user", "content": prompt}],
        )

    response = call_with_retry(_call)
    usage_tracker.record(model, response.usage)
    return response.content[0].text

def generate_text_streaming(prompt: str, model: str = MODEL_DEFAULT) -> str:
    full_text = ""
    try:
        with client.messages.stream(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for chunk in stream.text_stream:
                print(chunk, end="", flush=True)
                full_text += chunk
            print()
            final_message = stream.get_final_message()
            usage_tracker.record(model, final_message.usage)
    except RETRYABLE_ERRORS as e:
        print(f"\n[stream error] {type(e).__name__}: could not complete stream — {e}")
    return full_text

class ContactInfo(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

EXTRACT_CONTACT_TOOL = {
    "name": "extract_contact",
    "description": "Extract a person's contact information from the given text.",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Full name of the person"},
            "email": {"type": "string", "description": "Email address, if present"},
            "phone": {"type": "string", "description": "Phone number, if present"},
        },
        "required": ["name"],
    },
}

def extract_structured(text: str, model: str = MODEL_DEFAULT) -> Optional[ContactInfo]:
    def _call():
        return client.messages.create(
            model=model,
            max_tokens=500,
            tools=[EXTRACT_CONTACT_TOOL],
            tool_choice={"type": "tool", "name": "extract_contact"},
            messages=[{"role": "user", "content": text}],
        )

    response = call_with_retry(_call)
    usage_tracker.record(model, response.usage)

    for block in response.content:
        if block.type == "tool_use" and block.name == "extract_contact":
            try:
                return ContactInfo(**block.input)
            except ValidationError as e:
                print(f"[validation error] Model output didn't match schema: {e}")
                return None
    return None

class Conversation:
    def __init__(self, model: str = MODEL_DEFAULT, system: Optional[str] = None, max_history_messages: int = 20):
        self.model = model
        self.system = system or "You are a friendly, helpful assistant."
        self.max_history_messages = max_history_messages
        self.history: list = []

    def _trim_history(self):
        if len(self.history) > self.max_history_messages:
            self.history = self.history[-self.max_history_messages:]

    def send(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        self._trim_history()

        def _call():
            return client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system,
                messages=self.history,
            )

        response = call_with_retry(_call)
        usage_tracker.record(self.model, response.usage)

        reply = response.content[0].text
        self.history.append({"role": "assistant", "content": reply})
        return reply

def main():
    print("=" * 70)
    print("1) BASIC TEXT GENERATION")
    print("=" * 70)
    answer = generate_text("In one sentence, what is an API?", model=MODEL_FAST)
    print(answer, "\n")

    print("=" * 70)
    print("2) STREAMING RESPONSE")
    print("=" * 70)
    generate_text_streaming("Write a 3-line haiku about debugging code.")
    print()

    print("=" * 70)
    print("3) STRUCTURED RESPONSE (tool-based JSON extraction)")
    print("=" * 70)
    raw_text = "Hi, I'm Priya Shah — you can reach me at priya.shah@example.com."
    contact = extract_structured(raw_text)
    if contact:
        print(json.dumps(contact.model_dump(), indent=2))
    print()

    print("=" * 70)
    print("4) MULTI-TURN CONVERSATION (history managed for you)")
    print("=" * 70)
    convo = Conversation(model=MODEL_FAST, system="You are a terse assistant. One sentence replies.")
    print("User: My name is Alex and I'm learning about LLM APIs.")
    print("Assistant:", convo.send("My name is Alex and I'm learning about LLM APIs."))
    print("User: What's my name, and what am I learning about?")
    print("Assistant:", convo.send("What's my name, and what am I learning about?"))
    print()

    print("=" * 70)
    print("5) TOKEN USAGE + COST SUMMARY")
    print("=" * 70)
    print(usage_tracker.summary())

if __name__ == "__main__":
    main()