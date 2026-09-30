# Week 5 — Day 3

## Task(s) Assigned
What is LangChain? 
Models 
Prompt templates 
Output parsers 
Retrievers 
Document loaders 
Text splitters 
Chains 
Tools 
Tool calling 
Memory/conversation concepts 
RAG pipelines 
AI application architecture 
Hands-on: 
Build a RAG application using a modern AI framework. 
Connect LLM + embeddings + vector search. 

## What I Did
Firstly, I created my own virtual environment for the project, which isolates the LangChain packages and their dependencies from my other work. Then, I optimized my understanding of the fundamental concepts of LangChain, starting with models. I also had to navigate the distinction between embedding and chat models, where the former transforms text into vectors so that similar meanings can be compared, and the latter takes a list of messages and returns a response. Additionally, I explored how LangChain provides a uniform interface for all model providers, making it easy to replace one LLM with another without having to rewrite the application.

## Key Learnings
LangChain is a framework designed to enable a simple LLM to become a complete application by offering common building blocks like models, prompt templates, output parsers, retrievers, document loaders, text splitters, chains, and tools. I grasped the core idea that an LLM is inherently stateless and only knows the data it was trained on, while real-world applications require additional components built around it.

Both model types are required for a RAG (Retrieval-Augmented Generation) pipeline: chat models produce text from messages, while embedding models convert text into numbers. A RAG system involves loading documents, chunking them into small, overlapping sections, embedding them, and then storing them in a vector database. The process entails asking a question, embedding it, retrieving the most similar chunks, and putting them into a prompt template so that the LLM only uses that specific context to answer the question, thereby minimizing the risk of hallucination.

I also learned that these steps are chained with pipe syntax (prompt | llm | parser), that the model can call a function which I need to implement, and that "memory" simply involves re-sending relevant conversation history—the model doesn't actually remember anything on its own. Last but not least, I realized that a good AI application architecture should isolate the indexing task from serving, and return the sources containing the answers so they can be verified

## Files in this folder
- `rag_app.py` — RAG chatbot using LangChain that loads documents, splits and embeds them into Chromadb, and answers questions with a Groq/Grok LLM while keeping conversation memory.
- `requirements.txt` — list of Python packages needed to run the project.
