import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-small-latest"
API_URL = "https://api.mistral.ai/v1/chat/completions"


def call_mistral(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    res = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
