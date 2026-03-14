from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Health check endpoint
@app.get("/")
def home():
    return {"message": "Salesforce LLM API running"}

@app.post("/chat/completions")
def generate_text(request: PromptRequest, authorization: str = Header(None)):

    # Authentication check
    if authorization != "Bearer salesforce-secret":
        raise HTTPException(status_code=401, detail="Unauthorized")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": request.prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Groq API Error")

    data = response.json()

    return {
        "response": data["choices"][0]["message"]["content"]
    }