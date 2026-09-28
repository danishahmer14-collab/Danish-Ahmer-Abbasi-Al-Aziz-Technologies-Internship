import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("\n=== PART 1: Generate embeddings ===")

sentences = [
    "The cat sits on the sofa.",
    "A kitten is resting on the couch.",
    "The stock market crashed yesterday.",
]

embeddings = model.encode(sentences)

print("Shape:", embeddings.shape)
print("Dimension of each vector:", embeddings.shape[1])
print("First 8 numbers of sentence 1:", np.round(embeddings[0][:8], 4))

print("\n=== PART 2: Cosine similarity ===")


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


print(f"'{sentences[0]}'\n  vs '{sentences[1]}'  -> {cosine_similarity(embeddings[0], embeddings[1]):.3f}")
print(f"'{sentences[0]}'\n  vs '{sentences[2]}'  -> {cosine_similarity(embeddings[0], embeddings[2]):.3f}")
print("=> Cat/kitten sentences share almost no words but score HIGH (semantic similarity).")

print("\n=== PART 3: Chunking ===")


def chunk_text(text, chunk_size=40, overlap=10):
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]
        chunks.append(" ".join(chunk_words))
        if start + chunk_size >= len(words):
            break
    return chunks


documents = [
    {
        "source": "python_intro.txt",
        "category": "programming",
        "text": (
            "Python is a high-level programming language known for its readable syntax. "
            "It is widely used in web development, automation, data science, and artificial intelligence. "
            "Python has a huge ecosystem of libraries such as NumPy, Pandas, and PyTorch. "
            "Beginners like Python because the code looks close to plain English. "
            "It supports multiple paradigms including object-oriented and functional programming."
        ),
    },
    {
        "source": "health_guide.txt",
        "category": "health",
        "text": (
            "Regular exercise improves heart health and boosts mood. "
            "Adults should aim for at least 150 minutes of moderate activity every week. "
            "A balanced diet with vegetables, fruits, whole grains, and lean protein supports long-term health. "
            "Sleeping seven to eight hours each night helps the body recover and improves concentration. "
            "Drinking enough water is also important for energy and digestion."
        ),
    },
    {
        "source": "space_facts.txt",
        "category": "science",
        "text": (
            "The Sun is a star at the center of our solar system. "
            "Jupiter is the largest planet and has a strong magnetic field and many moons. "
            "Mars is called the red planet because of iron oxide on its surface. "
            "Light from the Sun takes about eight minutes to reach the Earth. "
            "Astronomers use telescopes to study distant galaxies and stars."
        ),
    },
    {
        "source": "ai_basics.txt",
        "category": "programming",
        "text": (
            "Machine learning lets computers learn patterns from data instead of following fixed rules. "
            "Neural networks are inspired by the human brain and power modern AI systems. "
            "Large language models are trained on huge amounts of text to predict the next word. "
            "Embeddings convert text into numbers so that similar meanings are close together. "
            "Retrieval augmented generation combines search with language models to answer questions from your own data."
        ),
    },
]

all_chunks = []
for doc in documents:
    pieces = chunk_text(doc["text"], chunk_size=30, overlap=8)
    for i, piece in enumerate(pieces):
        all_chunks.append(
            {
                "id": f"{doc['source']}_chunk{i}",
                "text": piece,
                "metadata": {
                    "source": doc["source"],
                    "category": doc["category"],
                    "chunk_index": i,
                },
            }
        )

print(f"Created {len(all_chunks)} chunks from {len(documents)} documents.")
print("Example chunk:")
print("  id      :", all_chunks[0]["id"])
print("  text    :", all_chunks[0]["text"])
print("  metadata:", all_chunks[0]["metadata"])

print("\n=== PART 4: Store in vector database ===")

client = chromadb.PersistentClient(path="./chroma_db")

try:
    client.delete_collection("day1_docs")
except Exception:
    pass

collection = client.create_collection(
    name="day1_docs",
    metadata={"hnsw:space": "cosine"},
)

texts = [c["text"] for c in all_chunks]
chunk_embeddings = model.encode(texts).tolist()

collection.add(
    ids=[c["id"] for c in all_chunks],
    documents=texts,
    embeddings=chunk_embeddings,
    metadatas=[c["metadata"] for c in all_chunks],
)

print(f"Stored {collection.count()} vectors in ChromaDB.")


def search(query, k=3, where=None):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        where=where,
    )

    print(f"\nQuery: '{query}'  (top {k}" + (f", filter={where}" if where else "") + ")")
    for rank in range(len(results["ids"][0])):
        distance = results["distances"][0][rank]
        similarity = 1 - distance
        meta = results["metadatas"][0][rank]
        text = results["documents"][0][rank]
        print(f"  #{rank + 1}  similarity={similarity:.3f}  [{meta['source']}, chunk {meta['chunk_index']}]")
        print(f"       {text}")


print("\n=== PART 5: Similarity search & Top-K ===")

search("How can I stay fit and healthy?", k=3)
search("Which planet is the biggest?", k=2)
search("How do computers understand the meaning of text?", k=3)

search("What is a good language for beginners?", k=2, where={"category": "programming"})

print("\nDone! Now experiment: change chunk_size, overlap, k, and the queries.")