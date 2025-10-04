# Install dependencies first if not done already:
# pip install langgraph langchain openai
from langgraph.graph import StateGraph, START , END
from typing import TypedDict,Literal
from google import genai
from dotenv import load_dotenv
import os
from pydantic import BaseModel,Field
from openai import OpenAI
from sample1frontend import call_generate_query, call_run_query

#from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from google import genai
from google.genai.types import Content, Part

# --- 1. Define the State ---
class ConversationState(BaseModel):
    user_message: str = Field(
        ...,
        description="The natural language input from the user."
    )
    sql_query: Optional[str] = Field(
        None,
        description="The SQL query generated from the user_message."
    )
    response: str = Field(
        "",
        description="The natural language response from the AI."
    )


# --- 2. Define the LLM Node ---
client = OpenAI(
    api_key="<API_KEY>",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def llm_node(state: ConversationState) -> ConversationState:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": state.user_message}
    ]
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "call_generate_query",
                    "description": "This function generates a SQL query based on the user request",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_input": {
                                "type": "string",
                                "description": "It is user request what they want to do regarding database"
                            }
                        },
                        "required": ["user_input"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "call_run_query",
                    "description": "This function executes a SQL query against the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {
                                "type": "string",
                                "description": "It is the SQL query to be executed"
                            }
                        },
                        "required": ["sql_query"]
                    }
                }
            }
        ],
        function_call="auto"
    )

    message = response.choices[0].message
    if message.get("function_call"):
        fn_name = message["function_call"]["name"]
        fn_args = message["function_call"].get("arguments", {})
        if fn_name == "call_generate_query":
            # Step 1: Call generate_query tool
            sql_query = call_generate_query(fn_args["user_input"])
            state.sql_query = sql_query
            if sql_query:
                # Step 2: Feed SQL into run_query tool
                run_result = call_run_query(sql_query)
                state.response = run_result
            else:
                state.response = "Failed to generate SQL query."
        elif fn_name == "call_run_query":
            # Step 2: Feed SQL into run_query tool
            run_result = call_run_query(fn_args["sql_query"])
            state.response = run_result
    else:
        state.response = message["content"]
    return state


graph=StateGraph(ConversationState)
graph.add_node("llm", llm_node)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)
chatbot=graph.compile()
if __name__ == "__main__":
    query="Hey" 
    initial_state = ConversationState(user_message=query)
    final_state = chatbot(initial_state)
    print("Final State:", final_state)
    print("Query Result:", final_state.response)