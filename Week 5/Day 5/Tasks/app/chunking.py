import hashlib
from dataclasses import dataclass, field

from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)


def chunk_text(text: str, source: str, chunk_size: int = 800, overlap: int = 120) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for i, piece in enumerate(splitter.split_text(text)):
        digest = hashlib.sha1(f"{source}:{i}:{piece}".encode()).hexdigest()[:16]
        chunks.append(Chunk(id=digest, text=piece, metadata={"source": source, "chunk_index": i}))
    return chunks