from contextlib import asynccontextmanager
from io import BytesIO

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile

from app.config import get_settings
from app.embeddings import Embedder
from app.llm import LLM
from app.rag import RAGService
from app.schemas import (IngestRequest, IngestResponse, QueryRequest,
                         QueryResponse, SearchResponse)
from app.vectorstore import VectorStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    app.state.rag = RAGService(
        s, Embedder(s.embedding_model), VectorStore(s.chroma_dir), LLM(s)
    )
    yield


app = FastAPI(
    title="RAG Assistant API",
    version="1.0.0",
    description="Ingest documents, search them semantically, and ask grounded questions.",
    lifespan=lifespan,
)


def get_rag() -> RAGService:
    return app.state.rag


@app.get("/health", tags=["system"])
def health(rag: RAGService = Depends(get_rag)):
    return {"status": "ok", "chunks": rag.store.count(), "model": rag.llm.model}


@app.post("/documents", response_model=IngestResponse, tags=["documents"])
def ingest(req: IngestRequest, rag: RAGService = Depends(get_rag)):
    """Chunk, embed and store raw text."""
    n = rag.ingest_text(req.text, req.source)
    return IngestResponse(source=req.source, chunks_added=n, total_chunks=rag.store.count())


@app.post("/documents/upload", response_model=IngestResponse, tags=["documents"])
async def upload(file: UploadFile = File(...), rag: RAGService = Depends(get_rag)):
    """Upload a .txt, .md or .pdf file."""
    raw = await file.read()
    name = file.filename or "upload"
    if name.lower().endswith(".pdf"):
        from pypdf import PdfReader

        text = "\n\n".join(p.extract_text() or "" for p in PdfReader(BytesIO(raw)).pages)
    elif name.lower().endswith((".txt", ".md")):
        text = raw.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(415, "Supported types: .txt, .md, .pdf")
    if not text.strip():
        raise HTTPException(422, "No extractable text in file")
    n = rag.ingest_text(text, name)
    return IngestResponse(source=name, chunks_added=n, total_chunks=rag.store.count())


@app.get("/documents", tags=["documents"])
def list_documents(rag: RAGService = Depends(get_rag)):
    return {"sources": rag.store.sources(), "total_chunks": rag.store.count()}


@app.delete("/documents", tags=["documents"])
def clear_documents(rag: RAGService = Depends(get_rag)):
    rag.store.reset()
    return {"status": "cleared"}


@app.post("/search", response_model=SearchResponse, tags=["retrieval"])
def search(req: QueryRequest, rag: RAGService = Depends(get_rag)):
    """Vector search only. No LLM involved. Useful for debugging retrieval."""
    return SearchResponse(query=req.question, hits=rag.retrieve(req.question, req.top_k))


@app.post("/query", response_model=QueryResponse, tags=["rag"])
def query(req: QueryRequest, rag: RAGService = Depends(get_rag)):
    """Full RAG: answer grounded in retrieved chunks, with sources."""
    return rag.answer(req.question, req.top_k)