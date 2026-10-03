from pathlib import Path

from app.chunking import chunk_text
from app.config import get_settings
from app.embeddings import Embedder

e = Embedder(get_settings().embedding_model)


def cos(x, y):
    return sum(i * j for i, j in zip(x, y))


# Test 1: a standard sanity check with simple everyday sentences
a, b, c = e.embed([
    "A man is eating food.",
    "A man is eating a piece of bread.",
    "The girl is carrying a baby.",
])
print("Test 1 (similar):  ", round(cos(a, b), 3))
print("Test 1 (unrelated):", round(cos(a, c), 3))

# Test 2: the real job, retrieval over your own document
text = Path("data/rag_notes.md").read_text(encoding="utf-8")
chunks = chunk_text(text, "rag_notes.md", 500, 80)
cvecs = e.embed([ch.text for ch in chunks])

for q in ["How do I stop the model from making things up?", "What does chunk overlap do?"]:
    qv = e.embed([q])[0]
    ranked = sorted(zip(cvecs, chunks), key=lambda p: cos(qv, p[0]), reverse=True)
    print(f"\nQ: {q}")
    for v, ch in ranked[:3]:
        print(f"  {cos(qv, v):.3f}  {ch.text[:60]!r}")