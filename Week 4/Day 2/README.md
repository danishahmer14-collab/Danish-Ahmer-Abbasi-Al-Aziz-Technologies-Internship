# Week 4 — Day 2

## Task(s) Assigned
AI API concepts 
API authentication 
Environment variables 
Model selection 
Text generation 
Structured responses 
Streaming responses 
Conversation history 
Error handling 
Rate limits 
Token usage 
Cost awareness 
JSON responses 
Hands-on: 
Build a Python LLM application. 
Implement streaming and structured responses. 

## What I Did
First, I created my own virtual environment and a .env file to protect my API keys from being pushed to GitHub. I generated an Anthropic API key and successfully loaded it into my script via python-dotenv. I then created an extensive application (Tasksw4d2.py) with the Anthropic SDK. In this script, I implemented simple text generation with varying model sizes (Haiku vs. Sonnet), streaming responses to output text chunk-by-chunk for a better user experience, and structured JSON extraction via API "tool use" validated using pydantic. I also integrated a multi-turn conversation class that manually handles and truncates chat history to avoid context overflow, a custom retry function with exponential backoff for transient API errors, and a usage tracker to determine input and output tokens to estimate usage costs. In addition, during execution, I debugged SDK version changes by removing the deprecated temperature parameter, and I learned about the nature of API billing by resolving a 400 Bad Request error caused by an unfunded account balance.

## Key Learnings
Regarding security and environments, API keys are sensitive secrets that authenticate you with an LLM provider, meaning they should never be inserted into scripts or frontend code but rather set in environment variables like a .env file to ensure they are not accidentally leaked. Understanding statelessness and context taught me that LLM APIs are context-less; for multi-turn conversations, the entire chat history must be appended and sent again with each new message. Since providers charge by tokens for input and output, large conversations can quickly become expensive if the history isn't managed or shortened. When handling responses, basic text generation waits for the whole response to complete before returning, while streaming returns data in parts to reduce perceived latency. If an application must conform to a particular data structure, it is safer to use function calling to guarantee a specific format rather than simply prompting the model to return JSON. For resilience, production AI apps must accommodate network outages, rate limits, and overloaded servers; using retry logic, exponential backoff, and jitter prevents the app from crashing during intermittent provider problems, while immediately failing non-retryable errors like bad authentication. Finally, for cost optimization, the fastest and cheapest model should be used for simple tasks, employing more expensive models only for tasks requiring complex reasoning.

## Files in this folder
- `Tasksw4d2.py`  — Contains  Python application demonstrating text generation, streaming, structured tool use, conversation management, error handling, and usage tracking
- `.env` Contains Api keys for protection
- `requirement.txt` Contains list of Python dependencies required for the project
