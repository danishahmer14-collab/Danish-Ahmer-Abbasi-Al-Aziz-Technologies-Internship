from app.chunking import chunk_text
from app.config import Settings
from app.embeddings import Embedder
from app.llm import LLM
from app.vectorstore import VectorStore

SYSTEM_PROMPT = (
    "You are a careful assistant. Answer ONLY from the numbered context passages. "
    "Cite passages like [1] or [2]. If the context does not contain the answer, "
    "say you don't know. Never guess."
)


class RAGService:
    def __init__(self, settings: Settings, embedder: Embedder, store: VectorStore, llm: LLM):
        self.s = settings
        self.embedder = embedder
        self.store = store
        self.llm = llm

    def ingest_text(self, text: str, source: str) -> int:
        chunks = chunk_text(text, source, self.s.chunk_size, self.s.chunk_overlap)
        self.store.delete_source(source)
        self.store.upsert(chunks, self.embedder.embed([c.text for c in chunks]))
        return len(chunks)

    def retrieve(self, question: str, k: int | None = None) -> list[dict]:
        qvec = self.embedder.embed([question])[0]
        hits = self.store.search(qvec, k or self.s.top_k)
        return [h for h in hits if h["score"] >= self.s.min_score]

    def answer(self, question: str, k: int | None = None) -> dict:
        hits = self.retrieve(question, k)
        if not hits:
            return {"answer": "I don't know. No relevant documents were found.", "sources": []}
        context = "\n\n".join(
            f"[{i}] ({h['metadata']['source']}) {h['text']}" for i, h in enumerate(hits, 1)
        )
        user = f"Context:\n{context}\n\nQuestion: {question}"
        return {"answer": self.llm.generate(SYSTEM_PROMPT, user), "sources": hits}