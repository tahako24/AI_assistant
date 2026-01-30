import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_llm(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not found")

    print("⏳ Sending request to LLM...")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.3
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    print("✅ Response received")

    return response.json()["choices"][0]["message"]["content"]
