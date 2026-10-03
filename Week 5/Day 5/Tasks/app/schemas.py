from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    text: str = Field(..., min_length=1)
    source: str = Field("manual", description="Label shown in citations")


class IngestResponse(BaseModel):
    source: str
    chunks_added: int
    total_chunks: int


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int | None = Field(None, ge=1, le=20)


class Hit(BaseModel):
    text: str
    metadata: dict
    score: float


class SearchResponse(BaseModel):
    query: str
    hits: list[Hit]


class QueryResponse(BaseModel):
    answer: str
    sources: list[Hit]