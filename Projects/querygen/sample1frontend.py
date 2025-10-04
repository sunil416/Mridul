from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import google.generativeai as genai
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

API_BASE = "http://127.0.0.1:8000"  # FastAPI base URL

# State definition
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], "List of messages in the chat history"]

# Configure Gemini
genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Tool functions ---
def call_generate_query(user_input: str) -> str:
    resp = requests.post(f"{API_BASE}/generate-query", json={"query": user_input})
    data = resp.json()
    return data.get("query")  # None if failed

def call_run_query(sql_query: str) -> str:
    resp = requests.post(
    f"{API_BASE}/run-query",
    data=json.dumps(sql_query),
    headers={"Content-Type": "application/json"}
)
    data = resp.json()
    if "error" in data:
        return f"Error: {data['error']}"
    return str(data.get("result", data))
'''
query="i want to check which employee worked less than 8hrs on 18th september 2025"
sql_query = call_generate_query(query)
print("Generated SQL Query:", sql_query)
if sql_query:
    result = call_run_query(sql_query)
    print("Query Result:", result)'''