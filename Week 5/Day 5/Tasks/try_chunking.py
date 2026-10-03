from pathlib import Path
from app.chunking import chunk_text

text = Path("data/rag_notes.md").read_text(encoding="utf-8")

for size, overlap in [(800, 120), (300, 50)]:
    chunks = chunk_text(text, "rag_notes.md", size, overlap)
    print(f"\n=== chunk_size={size}, overlap={overlap} -> {len(chunks)} chunks")
    for c in chunks:
        print(f"[{c.metadata['chunk_index']}] ({len(c.text)} chars) {c.text[:70]!r}...")