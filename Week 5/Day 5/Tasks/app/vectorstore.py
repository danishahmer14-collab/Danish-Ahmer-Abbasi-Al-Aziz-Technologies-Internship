import chromadb

from app.chunking import Chunk


class VectorStore:
    def __init__(self, path: str, collection: str = "documents"):
        self.client = chromadb.PersistentClient(path=path)
        self.name = collection
        self.col = self.client.get_or_create_collection(
            self.name, metadata={"hnsw:space": "cosine"}
        )

    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self.col.upsert(
            ids=[c.id for c in chunks],
            documents=[c.text for c in chunks],
            embeddings=embeddings,
            metadatas=[c.metadata for c in chunks],
        )

    def search(self, embedding: list[float], k: int = 4) -> list[dict]:
        n = self.col.count()
        if n == 0:
            return []
        res = self.col.query(query_embeddings=[embedding], n_results=min(k, n))
        return [
            {"text": doc, "metadata": meta, "score": round(1 - dist, 4)}
            for doc, meta, dist in zip(
                res["documents"][0], res["metadatas"][0], res["distances"][0]
            )
        ]

    def count(self) -> int:
        return self.col.count()

    def delete_source(self, source: str) -> None:
        self.col.delete(where={"source": source})

    def sources(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for m in self.col.get(include=["metadatas"])["metadatas"]:
            counts[m["source"]] = counts.get(m["source"], 0) + 1
        return counts
    
    def reset(self) -> None:
        self.client.delete_collection(self.name)
        self.col = self.client.get_or_create_collection(
            self.name, metadata={"hnsw:space": "cosine"}
        )