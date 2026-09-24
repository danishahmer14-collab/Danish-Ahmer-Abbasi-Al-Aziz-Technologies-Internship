# Week 4 — Day 4

## Task(s) Assigned
Prompt structure 
System instructions 
Context injection 
Few-shot examples 
Output formatting 
JSON/structured output 
Prompt templates 
Prompt evaluation 
Hallucination reduction 
Grounding 
Context management 
Function/tool calling concepts 
AI application architecture 
Hands-on: 
Build an AI assistant with structured outputs. 
Create prompts for classification, extraction and summarization.

## What I Did
Firstly, I set up a virtual environment for my project using Python's built-in venv tool to manage my project dependencies. I then placed my API key into a .env file and added it to .gitignore so that it wouldn't be uploaded to GitHub. Once the setup was complete, I reviewed the theoretical concepts of prompt engineering and wrote the Python code to create a structured AI assistant in the file Taskw4d4.py, I cannot run the code due to low balance in my API.

## Key Learnings
I explored prompt structure, which is the skill of organizing prompts, context, and questions to maximize the AI's understanding. I learned about system instructions, the basic rules that dictate the AI's personality, limitations, and modes of operation without user input. I also covered context injection, which involves including relevant background information or real-time data into the prompt for the model to use. Additionally, I studied few-shot examples, which give the model concrete input-output pairs to learn a specific pattern, and output formatting to provide a specific structural layout for the response. A major focus was JSON and structured output, ensuring the model generates machine-readable data for consistent software integration. Furthermore, I looked into prompt templates, which are reusable, modular text strings with variable placeholders. I also explored prompt evaluation for testing prompts on edge cases prior to deployment, and hallucination reduction to minimize the risk of the AI making up information by using strict constraints. This connects to grounding, which ties the model's generation explicitly to a source of truth based on facts rather than pre-trained weights. Finally, I reviewed context management to programmatically manage, truncate, or summarize data to fit the model's token window, function and tool calling concepts to give the model access to external tools, and the overall AI application architecture, which includes the LLM, orchestrators, vector databases, execution environments, and security guardrails

## Files in this folder
 `Taskw4d4.py` — The main Python script demonstrating the use of OpenAI's structured outputs and Pydantic to perform classification, extraction, and summarization tasks.
