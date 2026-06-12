"""
Agent Render-ready.
Render injects `PORT` env var automatically — agent must read os.getenv("PORT").
"""
import os
import time
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from utils.mock_llm import ask

app = FastAPI(title="Agent on Render", version="1.0.0")
START_TIME = time.time()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AI Agent running on Render!",
        "docs": "/docs",
        "health": "/health",
    }


@app.post("/ask")
async def ask_agent(request: Request):
    body = await request.json()
    question = body.get("question", "")
    if not question:
        raise HTTPException(422, "question required")
    return {
        "question": question,
        "answer": ask(question),
        "platform": "Render",
    }


@app.get("/health")
def health():
    """
    Render will check this endpoint periodically.
    Return 200 = healthy. Non-200 = Render may restart the container.
    """
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "platform": "Render",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    # ✅ Render provides PORT env var — read from env
    port = int(os.getenv("PORT", 8000))
    print(f"Starting on port {port} (from PORT env var)")
    uvicorn.run(app, host="0.0.0.0", port=port)
