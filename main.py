from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.get("/")
def home():
    return {"message": "Groq LLM Middleware API running"}

@app.post("/generate")
def generate_text(request: PromptRequest):

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": request.prompt
            }
        ]
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=payload
    )

    data = response.json()

    ai_text = data["choices"][0]["message"]["content"]

    return {
        "prompt": request.prompt,
        "response": ai_text
    }