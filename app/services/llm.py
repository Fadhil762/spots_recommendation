import os
import httpx

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

SYSTEM = (
    "You are a short, decisive intent helper. "
    "Given a user's prompt, reply with exactly one of : FIND_PLACES or UNKNOWN."
)

async def classify(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM}\nUSER: {prompt}\nASSISTANT:",
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f"{OLLAMA_HOST}/api/generate", json=payload)
            r.raise_for_status()
            out = r.json().get("response", "").strip().upper()
            return "FIND_PLACES" if "FIND_PLACES" in out else "UNKNOWN"
    except Exception:
        #if LLM fails, be conservative
        return "UNKNOWN"