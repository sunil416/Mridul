import os
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def voice_input():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Now")
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except Exception as e:
            print("Sorry could not recognize your voice")
            return "Sorry could not recognize your voice"
def llm_model(user_prompt):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model=genai.GenerativeModel("gemma-3-4b-it")
    response=model.generate_content(user_prompt)
    result=response.text
    return result
def text_to_speech(text_response):
    tts=gTTS(text=text_response)
    tts.save("output.mp3")
