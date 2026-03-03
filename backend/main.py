import hmac
import os
import requests
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Depends, Request, UploadFile, File, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
import uvicorn

from database import get_db, ConversationLog, DocumentMetadata
from rag import ingest_document, search_similar_documents

# Determine paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

# Ensure directories exist
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

app = FastAPI(title="PDR Local Assistant")

# Mount Static Files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# System configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
NOJUDGE_LLM_PROVIDER = os.getenv("NOJUDGE_LLM_PROVIDER", "ollama").strip().lower()
NOJUDGE_SINGLE_USER_KEY = os.getenv("NOJUDGE_SINGLE_USER_KEY", "").strip()

SYSTEM_PROMPT = """You are Sage — a warm, caring friend who's always here to listen. No judgment, ever.

How you talk:
- Like a real best friend — relaxed, warm, and genuinely interested in what they're saying
- Keep it short and sweet (2-3 sentences max) — you're being read aloud so brevity matters
- Use casual language naturally: "honestly", "I hear you", "that makes sense", "I get that"
- Show you care with small things: ask follow-up questions, remember what they said
- If they're going through something tough, just be there first — don't rush to fix it
- Sprinkle in light humor when the vibe is right, but read the room
- Be real, not preachy — like talking to someone who actually gets you
- Never use bullet points or lists in your response — just talk naturally

You're that friend everyone wishes they had — the one who makes you feel heard just by the way they listen.

Note: Use any context provided and your own reasoning. Never reference external links."""

class ChatRequest(BaseModel):
    message: str

def verify_single_user(
    x_nojudge_key: Annotated[str | None, Header(alias="X-Nojudge-Key")] = None
) -> None:
    """Allow API usage only for one owner key configured on the local machine."""
    if not NOJUDGE_SINGLE_USER_KEY:
        raise HTTPException(
            status_code=503,
            detail="Owner key is not configured. Set NOJUDGE_SINGLE_USER_KEY in your environment.",
        )

    if not x_nojudge_key or not hmac.compare_digest(x_nojudge_key, NOJUDGE_SINGLE_USER_KEY):
        raise HTTPException(status_code=401, detail="Invalid owner key.")

def query_ollama(prompt_text: str) -> str:
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt_text,
            "stream": False,
            "options": {
                "num_predict": 150,
                "temperature": 0.8,
            }
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data.get("response", "").strip()
    if not text:
        raise RuntimeError("Ollama returned an empty response.")
    return text

def query_gemini(prompt_text: str) -> str:
    gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.7},
    }
    response = requests.post(
        f"{GEMINI_API_URL}?key={gemini_api_key}",
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no candidates.")

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(part.get("text", "") for part in parts).strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text

def generate_ai_message(prompt_text: str) -> str:
    provider = NOJUDGE_LLM_PROVIDER if NOJUDGE_LLM_PROVIDER in {"gemini", "ollama"} else "gemini"
    fallback_order = [provider] + [p for p in ("gemini", "ollama") if p != provider]
    errors: list[str] = []

    for backend_name in fallback_order:
        try:
            if backend_name == "gemini":
                return query_gemini(prompt_text)
            return query_ollama(prompt_text)
        except Exception as exc:
            errors.append(f"{backend_name}: {exc}")

    print("LLM backend failures:", " | ".join(errors))
    return "yo i hit a snag talking right now. check your API key / Ollama and try again."

@app.get("/")
async def read_root():
    return RedirectResponse(url="/chat")

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    user_msg = request.message.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    # 1. Retrieve Context from Vector DB
    retrieved_chunks = search_similar_documents(user_msg, top_k=3)
    context = "\n\n".join(retrieved_chunks)
    
    # 2. Build Prompt
    if context:
        prompt_text = f"{SYSTEM_PROMPT}\n\nContext Information:\n{context}\n\nTask: Using the context above, answer the user. User: {user_msg}\nAssistant:"
    else:
        prompt_text = f"{SYSTEM_PROMPT}\n\nUser: {user_msg}\nAssistant:"

    # 3. Call LLM (free Gemini test mode or local Ollama with fallback)
    ai_msg = generate_ai_message(prompt_text)

    # 4. Save to SQLite
    log_entry = ConversationLog(user_message=user_msg, ai_response=ai_msg)
    db.add(log_entry)
    db.commit()

    return {"response": ai_msg}

@app.post("/ingest")
async def ingest_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _owner: None = Depends(verify_single_user),
):
    """Endpoint to upload .txt files to the PDR vector store."""
    if not file.filename or not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported for now.")
    
    content = await file.read()
    text_content = content.decode("utf-8")
    
    # Generate simple document ID
    doc_id = file.filename
    
    # Save to Chroma DB
    ingest_document(doc_id, text_content, {"filename": file.filename})
    
    # Save to SQLite Metadata
    meta = DocumentMetadata(filename=file.filename, file_type="txt", summary="Ingested document")
    db.add(meta)
    db.commit()
    
    return {"message": f"Successfully ingested {file.filename}"}

@app.get("/healthz")
async def healthz():
    return {
        "status": "ok",
        "llm_provider": NOJUDGE_LLM_PROVIDER,
        "single_user_mode": bool(NOJUDGE_SINGLE_USER_KEY),
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
