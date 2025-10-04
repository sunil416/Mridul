from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from weather import WeatherData
import json
import uvicorn

app = FastAPI()

# Enable CORS


@app.get("/")
def index():
    return {"message": "Web App with Python FastAPI!"}

@app.post("/webhook")
async def webhook(request: Request):
    req = await request.json()
    print("Request:")
    print(json.dumps(req))

    weather_obj = WeatherData()
    res = weather_obj.processRequest(req)

    print(res)
    return res  # FastAPI automatically converts dict → JSON

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    