# Week 5 — Day 2

## Task(s) Assigned
What is RAG? 
Why RAG is needed 
RAG architecture 
Document ingestion 
Document loading 
Text splitting 
Embedding generation 
Vector storage 
Retrieval 
Context injection 
Answer generation 
Citations/source references 
RAG limitations 
Basic RAG evaluation 
Hands-on: 
Build a document-question-answering system. 
Upload documents and ask questions based on their content.

## What I Did
I began by learning the theory behind Retrieval-Augmented Generation (RAG): why it is needed, what it is, and how each aspect of the pipeline works. Then I created a Python virtual environment, listed the libraries I needed in the requirements.txt file, and installed them. I put my Groq API key in a .env file and added the .env file to .gitignore so that it never gets uploaded to GitHub.

Next, I created a document question-answering application in Streamlit called Tasksw5d2.py. The application allows a user to upload a PDF, TXT, or MD file and ask questions related to it. Under the hood, it runs a full RAG pipeline: it loads the documents using pypdf, splits the text into overlapping chunks, embeds those chunks using the all-MiniLM-L6-v2 sentence-transformers model, and stores them in a Chroma vector database. If I submit a query, the app embeds the question, fetches the top four most similar chunks, and places them into a prompt as numbered context. Using the Groq API, an LLM then provides an answer based solely on that context. The app displays the final answer with citations (like [1] and [2]), along with the source file, page number, and similarity distance of each retrieved chunk.

## Key Learnings
Instead of being limited to the material it learned during training, RAG allows an LLM to respond based on content outside of its training set. This can be used to address issues such as out-of-date information, lack of access to private data, hallucinations, and unverifiable answers. There are two main stages to the pipeline: indexing (load, split, embed, store) and querying (embed the question, retrieve, inject context, generate). I learned that the quality of the answer depends heavily on retrieval quality, since without the correct chunk, the LLM cannot provide the right answer. Chunk size and overlap are also important: small chunks lose context, while large chunks add noise. Embeddings convert text into vectors so that related concepts sit near each other in the vector space, enabling a search-by-meaning approach. Users can verify answers through citations because the model is only allowed to answer based on the provided context; otherwise, it is instructed to say "I don't know."

I also understand the drawbacks of RAG: if parsing or chunking is ineffective, the results will suffer. Furthermore, when a question is too vague and can be answered by multiple documents, it is difficult to get a good result using semantic search. Hallucinations can also still occur with RAG. Finally, I learned the basics of measuring retrieval (hit rate, MRR) and generation (faithfulness, correctness) separately using a small sample of test questions. From a practical perspective, I discovered how to securely store API keys using .env and .gitignore files, and I learned the difference between Groq and Grok.
## Files in this folder
- `Tasksw5d2.py` — Streamlit app that implements the document Q&A system with the full RAG pipeline (load, split, embed, store, retrieve, generate, cite).
- `requirements.txt` — list of Python libraries needed to run the project (streamlit, chromadb, pypdf, sentence-transformers, openai, python-dotenv).
- `.gitignore` — tells git to ignore `.env` (and the virtual environment) so secrets and large folders are not uploaded.
- `.env` — stores my Groq API key locally (not uploaded to GitHub; other people must create their own with `GROQ_API_KEY=...`).
