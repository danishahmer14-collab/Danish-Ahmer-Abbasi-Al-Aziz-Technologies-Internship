import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # reads GROQ_API_KEY / XAI_API_KEY etc. from the .env file

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = Path("docs")
DB_DIR = "chroma_db_hf"

PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

if PROVIDER == "groq":
    from langchain_groq import ChatGroq  # needs GROQ_API_KEY

    llm = ChatGroq(model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"), temperature=0)
elif PROVIDER == "xai":
    from langchain_xai import ChatXAI  # needs XAI_API_KEY

    llm = ChatXAI(model=os.getenv("LLM_MODEL", "grok-4"), temperature=0)
else:
    raise SystemExit("LLM_PROVIDER must be 'groq' or 'xai' (check your .env file)")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_documents():
    docs = []
    for path in DOCS_DIR.rglob("*"):
        if path.suffix.lower() == ".pdf":
            docs += PyPDFLoader(str(path)).load()
        elif path.suffix.lower() in {".txt", ".md"}:
            docs += TextLoader(str(path), encoding="utf-8").load()
    return docs


def build_vectorstore():
    docs = load_documents()
    if not docs:
        raise SystemExit(f"No documents found. Add files to ./{DOCS_DIR}/ first.")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    print(f"Loaded {len(docs)} pages/files -> {len(chunks)} chunks")
    return Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)


def get_vectorstore():
    if Path(DB_DIR).exists():
        return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return build_vectorstore()


vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 4})


condense_prompt = ChatPromptTemplate.from_template(
    "Given the chat history and a follow-up question, rewrite the follow-up "
    "as a standalone question. Return ONLY the question.\n\n"
    "History:\n{history}\n\nFollow-up: {question}"
)
condense_chain = condense_prompt | llm | StrOutputParser()

answer_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant. Answer ONLY from the context below. "
     "If the answer is not in the context, say you don't know.\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])
answer_chain = answer_prompt | llm | StrOutputParser()


def format_docs(docs):
    return "\n\n".join(
        f"[{d.metadata.get('source', '?')} p.{d.metadata.get('page', '-')}]\n{d.page_content}"
        for d in docs
    )


history: list[tuple[str, str]] = []


def ask(question: str):
    if history:
        hist_text = "\n".join(f"User: {u}\nAssistant: {a}" for u, a in history[-4:])
        standalone = condense_chain.invoke({"history": hist_text, "question": question})
    else:
        standalone = question

    docs = retriever.invoke(standalone)
    answer = answer_chain.invoke({"context": format_docs(docs), "question": question})

    history.append((question, answer))
    sources = sorted({f"{d.metadata.get('source', '?')} (p.{d.metadata.get('page', '-')})" for d in docs})
    return answer, sources
    
if __name__ == "__main__":
    print(f"RAG chatbot ready (provider: {PROVIDER}). Type 'exit' to quit.\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        if not q:
            continue
        ans, srcs = ask(q)
        print(f"\nAssistant: {ans}\n\nSources: {', '.join(srcs)}\n")
