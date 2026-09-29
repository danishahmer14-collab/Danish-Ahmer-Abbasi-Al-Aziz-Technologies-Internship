
import os
import uuid

import chromadb
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

load_dotenv()  # reads the key from the .env file in this folder


CHUNK_SIZE = 800      # characters per chunk
CHUNK_OVERLAP = 150   # characters shared between neighbouring chunks
TOP_K = 4             # how many chunks to retrieve
LLM_MODEL = "openai/gpt-oss-120b"  # see console.groq.com/docs/models for current names


@st.cache_resource
def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, local


# DOCUMENT LOADING
def load_document(uploaded_file):
    """Return a list of (text, page_number) for one uploaded file."""
    if uploaded_file.name.lower().endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return [(p.extract_text() or "", i + 1) for i, p in enumerate(reader.pages)]
    return [(uploaded_file.read().decode("utf-8", errors="ignore"), 1)]


# TEXT SPLITTING
def split_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Sliding window over the text, with overlap so ideas aren't cut off."""
    text = " ".join(text.split())  # normalise whitespace
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return [c for c in chunks if len(c.strip()) > 30]


#  3 + 4. EMBEDDING + VECTOR STORAGE 
def index_documents(files, collection):
    embedder = get_embedder()
    for f in files:
        texts, metas = [], []
        for page_text, page_no in load_document(f):
            for chunk in split_text(page_text):
                texts.append(chunk)
                metas.append({"source": f.name, "page": page_no})
        if not texts:
            continue
        vectors = embedder.encode(texts, normalize_embeddings=True).tolist()  # embeddings
        collection.add(                                                        # storage
            ids=[str(uuid.uuid4()) for _ in texts],
            documents=texts,
            embeddings=vectors,
            metadatas=metas,
        )


#  RETRIEVAL
def retrieve(question, collection, k=TOP_K):
    q_vec = get_embedder().encode([question], normalize_embeddings=True).tolist()
    res = collection.query(query_embeddings=q_vec, n_results=k)
    return [
        {"text": t, "source": m["source"], "page": m["page"], "distance": d}
        for t, m, d in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


# CONTEXT INJECTION
def build_prompt(question, chunks):
    context = "\n\n".join(
        f"[{i}] (source: {c['source']}, page {c['page']})\n{c['text']}"
        for i, c in enumerate(chunks, 1)
    )
    return (
        "Answer the question using ONLY the numbered context below. "
        "Cite the sources you used like [1] or [2]. "
        "If the context does not contain the answer, say you don't know "
        "based on the provided documents.\n\n"
        f"CONTEXT:\n{context}\n\nQUESTION: {question}"
    )


# ANSWER GENERATION
def generate_answer(prompt):

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("No API key found. Add GROQ_API_KEY=... to your .env file.")
        st.stop()
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


# UI
st.title("📄 Document Q&A (RAG)")

if "collection" not in st.session_state:
    client = chromadb.Client()  # in-memory
    st.session_state.collection = client.create_collection(
        f"docs_{uuid.uuid4().hex[:8]}", metadata={"hnsw:space": "cosine"}
    )
    st.session_state.indexed = set()

files = st.file_uploader("Upload PDF / TXT / MD files", type=["pdf", "txt", "md"],
                         accept_multiple_files=True)
new_files = [f for f in files if f.name not in st.session_state.indexed]
if new_files:
    with st.spinner("Loading, splitting, embedding, storing..."):
        index_documents(new_files, st.session_state.collection)
    st.session_state.indexed.update(f.name for f in new_files)
    st.success(f"Indexed {len(new_files)} file(s). "
               f"Total chunks: {st.session_state.collection.count()}")

question = st.text_input("Ask a question about your documents")
if question:
    if st.session_state.collection.count() == 0:
        st.warning("Upload a document first.")
    else:
        chunks = retrieve(question, st.session_state.collection)
        answer = generate_answer(build_prompt(question, chunks))
        st.markdown("### Answer")
        st.write(answer)
        st.markdown("### Sources retrieved")
        for i, c in enumerate(chunks, 1):
            with st.expander(f"[{i}] {c['source']} - page {c['page']} "
                             f"(distance {c['distance']:.3f})"):
                st.write(c["text"])