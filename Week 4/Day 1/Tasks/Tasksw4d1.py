from dotenv import load_dotenv
load_dotenv()

import json
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-6"


def call_llm(messages, system=None, temperature=1.0, max_tokens=300):
    kwargs = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": messages,
        "extra_body": {"temperature": temperature},
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    text = "".join(block.text for block in response.content if block.type == "text")
    return text, response.usage


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


print_section("1. Zero-shot prompting")

zero_shot_prompt = "Classify the sentiment of this review as Positive, Negative, or Neutral: 'The battery life is decent but the screen feels outdated.'"

text, usage = call_llm(
    messages=[{"role": "user", "content": zero_shot_prompt}],
    temperature=0.2,
)
print(f"Prompt: {zero_shot_prompt}")
print(f"Response: {text}")
print(f"Tokens used: input={usage.input_tokens}, output={usage.output_tokens}")


print_section("2. Few-shot prompting (same task, with examples)")

few_shot_prompt = """Classify the sentiment as Positive, Negative, or Neutral.

Review: "Absolutely love this product, works perfectly!"
Sentiment: Positive

Review: "Broke after two days, total waste of money."
Sentiment: Negative

Review: "It's fine, does what it says, nothing special."
Sentiment: Neutral

Review: "The battery life is decent but the screen feels outdated."
Sentiment:"""

text, usage = call_llm(
    messages=[{"role": "user", "content": few_shot_prompt}],
    temperature=0.2,
    max_tokens=10,
)
print(f"Response: {text.strip()}")
print(f"Tokens used: input={usage.input_tokens}, output={usage.output_tokens}")
print("Notice: few-shot examples nudge the model toward a short, consistent format —")
print("compare this response's length/format to the zero-shot one above.")


print_section("3. Role-based prompting")

system_persona = "You are a terse senior code reviewer. Give feedback in at most 2 short sentences. No pleasantries."
user_code = "def add(a,b): return a+b"

text, usage = call_llm(
    messages=[{"role": "user", "content": f"Review this function:\n{user_code}"}],
    system=system_persona,
    temperature=0.3,
)
print(f"System role: {system_persona}")
print(f"Response: {text}")


print_section("4. Structured output (JSON)")

structured_prompt = """Extract the following from this text as JSON with keys
"name", "role", and "years_experience". Respond with ONLY the JSON, no other text.

Text: "Maria Chen has worked as a data scientist for 6 years."
"""

text, usage = call_llm(
    messages=[{"role": "user", "content": structured_prompt}],
    temperature=0.0,
)
print(f"Raw response: {text}")
try:
    parsed = json.loads(text.strip())
    print(f"Parsed successfully -> name={parsed['name']}, role={parsed['role']}, "
          f"years_experience={parsed['years_experience']}")
except json.JSONDecodeError:
    print("Could not parse as JSON — the model didn't follow the format instruction.")


print_section("5. Temperature comparison (same prompt, temp=0.0 vs temp=1.0)")

creative_prompt = "Write one creative opening line for a story about a lighthouse."

low_temp_text, _ = call_llm(
    messages=[{"role": "user", "content": creative_prompt}],
    temperature=0.0,
    max_tokens=60,
)
high_temp_text, _ = call_llm(
    messages=[{"role": "user", "content": creative_prompt}],
    temperature=1.0,
    max_tokens=60,
)
print(f"Temperature 0.0 (focused):  {low_temp_text.strip()}")
print(f"Temperature 1.0 (creative): {high_temp_text.strip()}")
print("Run this script again — temperature 0.0 should stay nearly identical each time,")
print("while temperature 1.0 will likely vary. (Note: on some newer models, sampling")
print("parameters may be ignored server-side, so this comparison may show little difference.)")


print_section("Done")
print("Try changing the prompts above, or add your own task to compare zero-shot vs few-shot.")