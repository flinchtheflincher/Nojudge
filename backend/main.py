import os
import requests
from fastapi import FastAPI, Depends, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import shutil

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
OLLAMA_MODEL = "qwen2.5-coder:14b"

SYSTEM_PROMPT = """Hey! I'm your bestie and we're just hanging out! Let's keep it real and fun:

- Talk like we're texting at 3am (super casual and honest)
- Use lots of "haha", "omg", "tbh", "fr fr"
- Share your thoughts like "ngl, I feel you" or "same tho!"
- Keep it medium length (3-4 sentences)
- Be that friend who's always got your back
- Give actual advice from your perspective
- If something's super serious, be gentle but real about it

Remember: We're besties who tell each other everything - just keep it friendly and appropriate! 😊
Note: Answer purely using the context provided (if any) and your own reasoning. Do not reference external links."""

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    user_msg = request.message
    
    # 1. Retrieve Context from Vector DB
    retrieved_chunks = search_similar_documents(user_msg, top_k=3)
    context = "\n\n".join(retrieved_chunks)
    
    # 2. Build Prompt
    if context:
        prompt_text = f"{SYSTEM_PROMPT}\n\nContext Information:\n{context}\n\nTask: Using the context above, answer the user. User: {user_msg}\nAssistant:"
    else:
        prompt_text = f"{SYSTEM_PROMPT}\n\nUser: {user_msg}\nAssistant:"
        
    print(f"Generated prompt: {prompt_text}")

    # 3. Call Local LLM via Ollama
    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt_text,
            "stream": False
        }, timeout=120)  # Larger models may take time
        response.raise_for_status()
        
        data = response.json()
        ai_msg = data.get("response", "oof my bad! brain froze for a sec there 😅 wanna try again?")
    except requests.exceptions.RequestException as e:
        print(f"Ollama error: {e}")
        ai_msg = "yo having a moment here, my local brain isn't fully spinning up!"

    # 4. Save to SQLite
    log_entry = ConversationLog(user_message=user_msg, ai_response=ai_msg)
    db.add(log_entry)
    db.commit()

    return {"response": ai_msg}

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Endpoint to upload .txt files to the PDR vector store."""
    if not file.filename.endswith(".txt"):
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
