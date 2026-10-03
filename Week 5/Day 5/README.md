# Week 5 — Day 5

## Task(s) Assigned
Review: 
Embeddings 
Vector search 
Chunking 
Vector databases 
RAG 
Retrieval 
LangChain 
Tools 
Function calling 
AI agents 
FastAPI 
AI API development 
Working RAG application 
GitHub repository 
README.md 
Architecture diagram 
API documentation 
Project demonstration 

## What I Did
I first set up my own virtual environment in VS Code and installed all the project requirements, and then reviewed the theory of the week: embeddings, vector search, chunking, vector databases, RAG, retrieval, LangChain, tools, function calling, AI agents, and FastAPI. After revising, I tried them in practice, constructing a "working RAG assistant" step-by-step. I added an OpenAI-compatible client with my Groq API key and stored the key in a .env file where it will never be exposed in the code. I then wrote a module for chunking the text with LangChain's recursive text splitter, then tried different chunk sizes and overlaps. I then created embeddings using the all-MiniLM-L6-v2 model and confirmed that similar sentences have a higher embedding similarity score than dissimilar ones. I added the vectors to a persistent collection in ChromaDB and performed similarity searches. Finally, I created the RAG pipeline, which retrieves the top chunks, filters weak matches according to the score threshold, and will then ask the LLM to answer based on the retrieved context with citations. I exposed the entire pipeline via a FastAPI application containing endpoints to ingest documents, perform searches, and answer questions, and tested it in the automatic Swagger documentation at /docs. I fixed a few things along the way: a wrong model name that returned a 404, a misleading embedding test that I was able to diagnose by comparing a few tests, and duplicate chunks that I solved by removing the old chunks from a document when it was re-ingested. I also made a project presentation that included the architecture diagram, API documentation, and demo results.

## Key Learnings
The most important thing I learned is that a RAG system isn't as effective as its retrieval, so I had to test search first before evaluating answers from the language model. I noticed that there is a real trade-off in what chunks of text to show: chunks that are too large have multiple topics in them, chunks that are too small lose some context that makes sense of sentences, and overlap helps when a sentence is cut between two topics. I learned that embeddings map text into vectors, such that when two things are similar, their vectors will be similar, and so a question such as "stop the model making things up" can find a passage about "hallucination" that has nothing in common but the words. A vector database will always provide the closest results, regardless of whether they are relevant or not; they must have a minimum similarity score before the system can provide the "I don't know" answer, otherwise it will provide the best guess that it has in its knowledge base. Numbers in the prompt provide context, and when the prompt asks for citations, the answers will be more credible and verifiable. From the API perspective, I gained insights into the use of typed Pydantic models and dependency injection to create clean endpoints and automatically generate API documentation with FastAPI. I also looked at function calling so a model could ask code to run a tool, and how an agent would then loop it with a step limit, which will be the next feature I add. Lastly, I got to know some practical bits: secrets in .env, pinning package versions with the same syntax as PHP, and checking things out with small experiments—rather than assuming they will work.

## Files in this folder
- `requirements.txt` — Python dependencies for the project
- `.gitignore` — keeps the virtual environment, `.env`, database and caches out of GitHub
- `app/config.py` — settings loaded from environment variables
- `app/chunking.py` — splits documents into overlapping chunks (LangChain splitter)
- `app/embeddings.py` — turns text into embedding vectors
- `app/vectorstore.py` — ChromaDB wrapper for storing and searching vectors
- `app/llm.py` — Groq LLM client (OpenAI-compatible)
- `app/rag.py` — RAG pipeline: ingest, retrieve and generate answers with citations
- `app/schemas.py` — Pydantic request and response models
- `app/main.py` — FastAPI application and endpoints
- `data/rag_notes.md` — sample document used for testing
- `test_llm.py`, `list_models.py` — scripts to test the API key and list available models
- `try_chunking.py`, `try_embeddings.py`, `try_vectorstore.py`, `try_rag.py` — experiment scripts for each stage
- `RAG_Assistant_Project.pptx` — project presentation (architecture, API docs, demo)
