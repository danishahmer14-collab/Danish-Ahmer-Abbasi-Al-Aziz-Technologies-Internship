# Week 6 — Day 1

## Task(s) Assigned
Understand AI project requirements and carry out requirement analysis and problem definition
Select the AI approach (traditional ML vs deep learning vs LLM), the model, and API vs local model
Plan the dataset, data pipeline, prompts, RAG, and agent/tools
Design the system architecture and API architecture
Plan the project folder structure, environment configuration, GitHub repository and README
Master Project: 
choose a project and prepare the problem statement, scope, feature list, user flow, AI architecture, technology stack, model selection, data requirements, API requirements, database/vector database requirements, project structure and development roadmap

## What I Did
I compared five candidate projects (policy docs assistant, resume screener, customer support agent, contract analyzer, study assistant) against the internship checklist and selected the Customer Support Agent with Tool Calling, since it covers RAG, tool calling, structured outputs, FastAPI, auth, a database and evaluation. I identified the problem: support teams spend time answering the same questions over and over again, and generic chatbots hallucinate policies and are unable to act on real order data. I wrote the project scope (in and out), a prioritized feature list (must / should / could) and the end-to-end user flow.
I then compared traditional ML, deep learning and LLM methods and selected LLM + RAG + tool calling. I chose the Claude API over a local model because of its tool-calling quality and because it does not require a GPU, and I chose the local all-MiniLM-L6-v2 model for embeddings. I designed the data: 8-12 knowledge base documents, a mock database of users, orders and refunds, and an evaluation set of question/answer pairs, tool scenarios and adversarial prompts. I also designed the ingestion pipeline (load, clean, chunk, embed, store, retrieve).
I planned four tools (order status, refund eligibility, request refund, escalate), the prompts (system prompt, RAG prompt, tool descriptions and JSON output schema), and the RAG settings (chunk size, top-k, similarity threshold, citations, "I don't know" fallback). I drew the system architecture and designed the API endpoints (auth, chat, orders, tickets, reindex, health) along with the SQL and vector DB schemas. I established the folder structure, .env configuration, GitHub setup and README outline, and created a 5-day roadmap along with a list of the most critical test cases for Day 4.
Tools used: Claude (for brainstorming and structuring the plan), Markdown, Git/GitHub.
## Key Learnings
Before coding, it is important to define the problem and scope of the work, so that only features that matter get built and the project can be demoed within a few days. An LLM alone is not enough for support: RAG grounds the answers in real documents, and tools allow the system to interact with real data.
Choosing an approach is a trade-off. An LLM with RAG can generate natural answers from documentation without labelling or training, whereas traditional ML and deep learning require labelled data and training. Security rules must be implemented in the backend: authorization and refund rules must be handled in code, not left to the model's judgment.
Planning evaluation early affects the design of the system and its fallbacks (hallucination, edge cases, prompt injection, wrong order IDs). Finally, a clear folder structure, .env configuration and README plan make the later days quicker and the project easier to present.
I made two accuracy fixes while keeping your wording. The "four system prompts, four RAG prompts" line was a mix-up (there are four tools and one prompt set), and all-MiniLM-L6-v2 is an embedding model, so it is not an alternative to the Claude API. I can update day1.md with this version if you want.

## Files in this folder
`project_plan.md` — full Master Project plan: problem statement, scope, features, user flow, architecture, tech stack, model selection, data, API, database, structure and roadmap
