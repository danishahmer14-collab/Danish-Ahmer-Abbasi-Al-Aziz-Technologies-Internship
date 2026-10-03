from pathlib import Path

from app.chunking import chunk_text
from app.config import get_settings
from app.embeddings import Embedder
from app.vectorstore import VectorStore

s = get_settings()
embedder = Embedder(s.embedding_model)
store = VectorStore(s.chroma_dir)

text = Path("data/rag_notes.md").read_text(encoding="utf-8")
chunks = chunk_text(text, "rag_notes.md", 500, 80)
store.upsert(chunks, embedder.embed([c.text for c in chunks]))
print("chunks in database:", store.count())

for q in ["What is cosine similarity?", "How do I reduce hallucination?"]:
    print(f"\nQ: {q}")
    for h in store.search(embedder.embed([q])[0], k=2):
        print(f"  {h['score']:.3f} [{h['metadata']['source']}] {h['text'][:60]!r}")