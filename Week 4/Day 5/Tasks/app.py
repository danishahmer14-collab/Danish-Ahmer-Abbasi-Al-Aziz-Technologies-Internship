import streamlit as st
from agent import app, AgentState

st.title("Enterprise SQL Agent")
st.markdown("Ask natural language questions about the business data. The agent will write, execute, and correct its own SQL.")

question = st.text_input("Ask a question:", "What were the total sales in the Networking category?")

if st.button("Query Database"):
    with st.spinner("Agent is working..."):
        # Initialize empty state with user question
        initial_state = {"question": question, "retry_count": 0, "error_message": ""}
        
        # Run the compiled LangGraph workflow
        result = app.invoke(initial_state)
        
        # Display Outputs
        st.subheader("Final Answer")
        st.write(result["final_answer"])
        
        with st.expander("View Agent Process & SQL"):
            st.code(result.get("generated_sql", "No SQL generated"), language="sql")
            st.write("**Raw Database Results:**")
            st.markdown(result.get("query_results", "No results"))
            if result.get("retry_count") > 0:
                st.warning(f"The agent had to self-correct {result['retry_count']} time(s) to fix SQL errors.")