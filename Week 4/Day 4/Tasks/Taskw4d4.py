import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Literal
from openai import OpenAI

# Load variables from the .env file
load_dotenv()

# Initialize the client 
client = OpenAI()

# ---------------------------------------------------------
# 1. Classification
# ---------------------------------------------------------
class SupportTicket(BaseModel):
    category: Literal["billing", "technical", "sales", "other"]
    urgency: Literal["low", "medium", "high"]

def classify_ticket(text: str) -> SupportTicket:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a routing agent. Classify the user's issue based strictly on the text provided."},
            {"role": "user", "content": text}
        ],
        response_format=SupportTicket
    )
    return completion.choices[0].message.parsed

# ---------------------------------------------------------
# 2. Extraction
# ---------------------------------------------------------
class EventDetails(BaseModel):
    event_name: str
    date: str
    participants: List[str]

def extract_event(text: str) -> EventDetails:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system", 
                "content": "Extract the event information. Return the date in ISO 8601 format if possible. If a participant's full name isn't given, use what is provided."
            },
            {"role": "user", "content": text}
        ],
        response_format=EventDetails
    )
    return completion.choices[0].message.parsed

# ---------------------------------------------------------
# 3. Summarization
# ---------------------------------------------------------
class ExecutiveSummary(BaseModel):
    key_takeaways: List[str]
    sentiment: Literal["positive", "neutral", "negative"]

def summarize_meeting(text: str) -> ExecutiveSummary:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system", 
                "content": "Summarize the provided transcript into exactly 3 key takeaways. Evaluate the overall sentiment."
            },
            {"role": "user", "content": text}
        ],
        response_format=ExecutiveSummary
    )
    return completion.choices[0].message.parsed

# ---------------------------------------------------------
# Execution Examples
# ---------------------------------------------------------
if __name__ == "__main__":
    
    # Classification Example
    ticket = classify_ticket("I was overcharged by $50 on my credit card this month and need a refund ASAP!")
    print("Classification:\n", ticket.model_dump_json(indent=2))
    
    # Extraction Example
    event = extract_event("Alice, Bob, and Charlie are meeting for the Q3 Roadmap Planning on October 15th, 2026.")
    print("\nExtraction:\n", event.model_dump_json(indent=2))
    
    # Summarization Example
    summary = summarize_meeting("The product launch was fantastic and users love the new UI. However, we need to fix the login bug quickly before it affects our retention rate.")
    print("\nSummarization:\n", summary.model_dump_json(indent=2))