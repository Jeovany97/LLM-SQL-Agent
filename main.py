import streamlit as st
import sqlite3
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

st.set_page_config(page_title="AI Data Analyst", page_icon="📊")
st.title("📊 Talk to your Sales Data")

# --- 1. Efficient API Key Handling ---
# Using a form prevents the app from rerunning for every single character typed
with st.sidebar:
    with st.form("config_form"):
        api_key = st.text_input("Google API Key", type="password")
        submit_config = st.form_submit_button("Connect Agent")

if not api_key:
    st.info("Please enter your API Key and click 'Connect Agent'.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

prompt = """
You are a expert Sales Data Analyst.
- When asked about 'growth', compare the current month's total to the previous month.
- If the user asks for 'Top' items, always limit to 5 unless specified.
- Use the 'Store_Name' column when users mention 'branch' or 'location'.
- Never execute INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE.
- If a user asks for modification, explain that the database is read-only
"""

# --- 2. Cache the Database and Agent ---
# @st.cache_resource ensures these are only created ONCE per session
@st.cache_resource
def get_sql_agent(key):
    db_uri = "sqlite:///file:store_transaction.db?mode=ro&uri=true"
    db = SQLDatabase.from_uri(db_uri)
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0) #Temperature set to zero for testing

    return create_sql_agent(
        llm,
        db=db,
        agent_type="tool-calling",
        verbose=True,
        max_iterations=5,  # Limits how many request ("thoughts") the agent has per query
        prefix = prompt
    )


agent_executor = get_sql_agent(api_key)

# --- 3. Persistent Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your sales..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Querying database..."):
            try:
                # The agent call is now the ONLY thing making an API request
                response = agent_executor.invoke({"input": prompt})
                full_response = response["output"]
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")