# Week 4 — Day 5

## Task(s) Assigned
Review:
Generative AI 
LLMs 
Tokens 
Prompt engineering 
LLM APIs 
Structured outputs 
Streaming 
Hugging Face 
Transformers 
Pre-trained models 
AI application patterns 
Friday Deliverables: 
Working AI application 
GitHub repository 
README.md 
Prompt documentation 
API configuration 
Project demonstration 
## What I Did
The first step in this project was to create a new Python virtual environment, investigate which modules were needed for an autonomous agent, and compile them into a requirements.txt file for installation. Then, I wrote a script that sets up a local relational SQLite database to emulate an import/export company's operations spanning a number of related tables. I then integrated the Groq API, created a utility script to ensure the model was actually available, and set up my backend to use the high-parameter openai/gpt-oss-120b reasoning model. The main logic was implemented in LangGraph, where I created a state machine to generate SQL queries, execute them, and use a conditional self-correction loop to rewrite the queries if there were database syntax errors. To ensure stability, I added Pydantic and JSON mode to the LLM to only return structured output, and I added strict prompt guardrails to prevent data hallucination in case of query failure. Lastly, I integrated this backend with a Streamlit app to create a complete and interactive UI for the final project demonstration.

## Key Learnings
Building this autonomous agent proved the complexity of production-level AI, showing it requires much more than just simple API calls. I learned how to create a workflow that works with an LLM, allowing it to execute logic, read system tracebacks, and dynamically self-correct. Troubleshooting 404 and 400 API errors taught me how to adapt to model configurations and switch between LLM providers while maintaining the core application code. I also learned how absolutely critical structured outputs are for integrating generative text into deterministic software loops, and how important it is to enforce strict JSON generation. Additionally, handling complex JOIN statement failures exposed how easily a model will hallucinate fake entities to satisfy a prompt, proving the need for clear prompt engineering and strict fallback instructions to ensure enterprise reliability.

## Files in this folder
- `requirements.txt`  —  Lists the Python dependencies required to run the Project.
- `setup_db.py` — Script that builds and populates the local company_data.db relational SQLite database with business data.
- `company_data.db` — The generated local database file used by the agent for SQL execution.
- `check_models.py` — Utility script to query the Groq API and list all active, permitted model IDs for the current API key.
- `agent.py` — The core backend logic containing the LangGraph state machine, database schema extraction, LLM node definitions, and self-correction routing.
- `app.py` — The Streamlit frontend application that provides the interactive user interface and visualizes the agent's database results and process.
- `Week4 Presentation.ppy`  — Is the Presentation for Project Demonstration.
