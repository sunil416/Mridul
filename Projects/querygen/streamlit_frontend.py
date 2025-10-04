import streamlit as st
import pandas as pd
import json
from geminisample import llm
# Dummy LLM function (replace with your actual one)
class ChatCompletionMessage:
    def __init__(self, content, role="assistant"):
        self.content = content
        self.role = role



# --- Streamlit App ---
st.set_page_config(page_title="Chat with LLM", page_icon="💬", layout="centered")
st.title("💬 LLM Chat Interface")

# Initialize chat history if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting from LLM
    greeting = llm("")
    if isinstance(greeting, ChatCompletionMessage):
        st.session_state.messages.append({"role": greeting.role, "content": greeting.content})
    else:
        st.session_state.messages.append({"role": "assistant", "content": greeting})

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        try:
            parsed = json.loads(msg["content"].replace("'", '"'))
            if isinstance(parsed, dict) and parsed.get("type") == "table":
                df = pd.DataFrame(parsed["data"])
                st.dataframe(df, use_container_width=True)
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])
        except Exception:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
    else:
        with st.chat_message("user"):
            st.markdown(msg["content"])

# Input box
if user_input := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from LLM
    response = llm(user_input)

    if isinstance(response, ChatCompletionMessage):
        content = response.content
    else:
        content = response  # raw string (possibly JSON-like)

    st.session_state.messages.append({"role": "assistant", "content": content})

    # Display assistant response
    try:
        parsed = json.loads(content.replace("'", '"'))
        if isinstance(parsed, dict) and parsed.get("type") == "table":
            df = pd.DataFrame(parsed["data"])
            st.dataframe(df, use_container_width=True)
        else:
            with st.chat_message("assistant"):
                st.markdown(content)
    except Exception:
        with st.chat_message("assistant"):
            st.markdown(content)
