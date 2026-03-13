from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/generate")
def generate_text(request: PromptRequest, authorization: str = Header(None)):

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

    data = response.json()

    return {
        "response": data["choices"][0]["message"]["content"]
    }