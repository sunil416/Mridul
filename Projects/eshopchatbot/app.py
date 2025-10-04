from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import uvicorn
from pathlib import Path
from echatbot.components.model_trainer import generation
from echatbot.components.data_ingestion import ingestdata
import os

# Setup paths and FastAPI
#BASE_DIR = Path(__file__).resolve().parent
#templates = Jinja2Templates(directory=str(BASE_DIR / "eshopchatbot/templates"))
app = FastAPI()

# Load env
load_dotenv()

vstore, _ = ingestdata()
ask_bot = generation(vstore)   #  generation returns a callable function

HTML_FOLDER = "/Users/softsuave/Projects/eshopchatbot/templates"

@app.get("/", response_class=HTMLResponse)
def read_html_file():
    file_path = os.path.join(HTML_FOLDER, "chat.html")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)

@app.post("/get")
async def chat(msg: str = Form(...)):
    """
    This endpoint takes a message from an HTML form and uses our custom bot
    (Gemini + Astra vector store) to generate a response.
    """
    response = ask_bot(msg)   # directly call the function
    print("Response:", response)
    return response

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
