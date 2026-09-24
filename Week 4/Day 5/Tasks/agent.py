from typing import TypedDict
from pydantic import BaseModel
import sqlite3
import pandas as pd
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

# Load environment variables (GROQ_API_KEY)
load_dotenv()

# Initialize Groq LLM with the specified model
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# --- 1. Define State and Pydantic Schema ---

class AgentState(TypedDict):
    question: str
    schema: str
    generated_sql: str
    error_message: str
    query_results: str
    retry_count: int
    final_answer: str

class SQLOutput(BaseModel):
    sql_query: str

def get_database_schema() -> str:
    # Connects to DB and extracts table structures
    conn = sqlite3.connect('company_data.db')
    schema_query = "SELECT sql FROM sqlite_master WHERE type='table';"
    schema = pd.read_sql(schema_query, conn)
    conn.close()
    return "\n".join(schema['sql'].dropna().tolist())

# --- 2. Define Graph Nodes ---

def generate_sql(state: AgentState):
    schema = get_database_schema()
    prompt = f"""
    You are a SQL expert. Write a valid SQLite query to answer the following question: "{state['question']}"
    Use the following schema:
    {schema}
    
    If there was an error previously, fix the SQL based on this error: {state.get('error_message', '')}
    
    You must return your answer in valid JSON format with a single key called "sql_query".
    """
    
    # Use json_mode to bypass the tool-calling restriction
    structured_llm = llm.with_structured_output(SQLOutput, method="json_mode")
    response = structured_llm.invoke(prompt)
    
    return {"generated_sql": response.sql_query, "schema": schema}

def execute_sql(state: AgentState):
    query = state['generated_sql']
    
    # Security Guardrail: Block modifying commands
    if any(keyword in query.upper() for keyword in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        return {"error_message": "Blocked: Destructive commands are not allowed.", "retry_count": state.get('retry_count', 0) + 1}
    
    try:
        conn = sqlite3.connect('company_data.db')
        df = pd.read_sql(query, conn)
        conn.close()
        return {"query_results": df.to_markdown(), "error_message": ""}
    except Exception as e:
        # Catch SQL syntax errors so the graph can loop back and fix them
        return {"error_message": str(e), "retry_count": state.get('retry_count', 0) + 1}

def synthesize_answer(state: AgentState):
    results = state.get('query_results', 'No results found.')
    error = state.get('error_message', '')
    
    # If there is an actual SQL error, force the error message
    if error:
        prompt = f"""
        The user asked: {state['question']}
        The database query failed.
        
        Tell the user exactly this: "I could not retrieve the data due to a query error."
        """
    # If the SQL was successful, pass ONLY the results
    else:
        prompt = f"""
        The user asked: {state['question']}
        Database Results: {results}
        
        Based ONLY on the Database Results above, answer the user's question concisely. 
        Do not mention databases or queries in your answer.
        """
        
    response = llm.invoke(prompt)
    return {"final_answer": response.content}

# --- 3. Wire the LangGraph Routing Logic ---

def routing_logic(state: AgentState):
    if state.get("retry_count", 0) >= 3:
        return "synthesize_answer" # Give up on SQL fixing and output what we have
    if state.get("error_message"):
        return "generate_sql" # Loop back to fix the syntax error
    return "synthesize_answer" # Success, move to synthesis

workflow = StateGraph(AgentState)
workflow.add_node("generate_sql", generate_sql)
workflow.add_node("execute_sql", execute_sql)
workflow.add_node("synthesize_answer", synthesize_answer)

workflow.set_entry_point("generate_sql")
workflow.add_edge("generate_sql", "execute_sql")

workflow.add_conditional_edges(
    "execute_sql",
    routing_logic,
    {
        "generate_sql": "generate_sql",
        "synthesize_answer": "synthesize_answer"
    }
)
workflow.add_edge("synthesize_answer", END)

# Compile the final agent application
app = workflow.compile()