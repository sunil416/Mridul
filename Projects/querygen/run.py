import streamlit as st
import requests

# Streamlit page config
st.set_page_config(page_title="Query Generator", page_icon="✨", layout="centered")

# Custom CSS for dark theme
st.markdown(
    """
    <style>
    body {
        background-color: #111;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #1f1f1f;
        color: white;
        border-radius: 20px;
        padding: 12px;
    }
    .stButton button {
        background-color: #333;
        color: white;
        border-radius: 20px;
        padding: 8px 16px;
        border: none;
    }
    .stButton button:hover {
        background-color: #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
#st.markdown("<h2 style='text-align: center;'>Ready when you are.</h2>", unsafe_allow_html=True)

# Input box
query = st.text_input("Ask anything", placeholder="Ask anything", label_visibility="collapsed")

# Submit button
if st.button("➤ Generate"):
    if query.strip():
        # Display a loading message while waiting for the response
        with st.spinner('Generating query...'):
            try:
                # The correct endpoint URL
                api_url = "http://127.0.0.1:8000/generate-query/"  
                
                # Send the POST request with the query in the JSON body
                response = requests.post(api_url, json={"query": query})
                
                # Check if the request was successful
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("result", "No result found.")
                    st.success("Generated Query:")
                    st.code(result, language='sql') # Use st.code to display SQL queries

                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError as e:
                st.error(f"Failed to connect to the API. Make sure the server is running at {api_url}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a query.")