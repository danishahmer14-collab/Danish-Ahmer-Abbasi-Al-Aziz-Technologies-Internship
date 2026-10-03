from pathlib import Path

from app.config import get_settings
from app.embeddings import Embedder
from app.llm import LLM
from app.rag import RAGService
from app.vectorstore import VectorStore

s = get_settings()
rag = RAGService(s, Embedder(s.embedding_model), VectorStore(s.chroma_dir), LLM(s))
rag.ingest_text(Path("data/rag_notes.md").read_text(encoding="utf-8"), "rag_notes.md")

questions = [
    "What is chunk overlap and why use it?",
    "How do I reduce hallucination?",
    "What is the capital of France?",  # not in the document
]
for q in questions:
    r = rag.answer(q)
    print(f"\nQ: {q}\nA: {r['answer']}")
    print("sources:", [(h["metadata"]["chunk_index"], h["score"]) for h in r["sources"]])