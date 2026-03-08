import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

async def ask_openai(messages: list):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": messages,
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENAI_URL, json=payload, headers=headers) as resp:
            if resp.status != 200:
                return None

            data = await resp.json()
            return data["choices"][0]["message"]["content"]