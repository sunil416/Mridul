import streamlit as st
from src.helper import voice_input, llm_model, text_to_speech

def main():
    st.title("Voice-Activated AI Assistant")
    
    if st.button("Start Talking"):
        with st.spinner("Listening..."):
            text = voice_input()
            response=llm_model(text)
            text_to_speech(response)
            
            audio_file = open("output.mp3", "rb")
            audio_bytes = audio_file.read()
            st.text_area("AI Response", value=response, height=200)
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("Download Response", data=audio_bytes, file_name="response.mp3", mime="audio/mp3")
            
if __name__ == "__main__":
    main()         
        