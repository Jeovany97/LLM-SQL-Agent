# LLM-SQL-Agent
A lightweight RAG-inspired application that translates natural language questions into executable SQL queries. Features a real-time Streamlit interface and high-speed processing via Google Gemini 2.0 Flash.

## Features

Natural Language to SQL: Converts English questions into complex SQL queries.

Gemini 2.0 Integration: Uses the latest Google Flash models for high-speed, low-cost reasoning.

Read-Only Security: Forced SQLite read-only mode to prevent accidental data modification.

Smart Caching: Uses Streamlit's @st.cache_resource to minimize API calls and boost performance.

Chat History: Persistent session state to keep track of your data conversation

## Dependencies
Dependenices are listed in the requirements.txt, database must be named store_transaction.db, and file must be in root directorym and a google AI API key

## Running 
streamlit run main.py
