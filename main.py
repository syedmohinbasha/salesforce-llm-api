from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

@app.get("/")
def home():
    return {"message": "Salesforce LLM API running"}

@app.post("/generate")
def generate_text(request: PromptRequest):

    url = "https://api.replicate.com/v1/predictions"

    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "version": "meta/llama-3-8b-instruct",
        "input": {
            "prompt": request.prompt
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        raise HTTPException(status_code=500, detail=response.text)

    prediction = response.json()

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": str(prediction)
                }
            }
        ]
    }