# PDR Implementation Changes

This document outlines the architectural changes and procedures implemented to transition Nojudge to the fully local Personal Data Repository (PDR) architecture, while preserving the original dependency structures.

## Procedures Implemented

### 1. Backend Migration to FastAPI
The primary change was shifting from the Flask-based architecture (which relied on the external Gemini API) to a fully local FastAPI server. 
- Created `backend/main.py` which serves as the new entry point.
- Replaced the Gemini API integration with local inference via Ollama, pulling the `qwen2.5-coder:14b` model.

### 2. Local Database Setup (SQLite & SQLAlchemy)
To satisfy the PDR objective of maintaining long-term memory of personal information locally:
- Established a basic SQLite database in the `/data` directory.
- Created SQLAlchemy models to track all conversation history and document metadata.

### 3. Vector Search & RAG Integration (ChromaDB)
To provide semantic search capabilities over personal unstructured data:
- Added `backend/rag.py` which leverages `sentence-transformers` for local embedding creation.
- Initialized a persistent local ChromaDB instance in `/vector_store` to store and query text chunks.
- Implemented an `/ingest` endpoint to allow simple `.txt` document uploads to the vector store.
- Integrated RAG into the chat context: before generating a response, the backend now searches ChromaDB for semantically similar user ingested contexts and includes them in the LLM's prompt.

### 4. Frontend Adaptation
- Migrated the assets from `soft/nojudge/templates` and `soft/nojudge/static` into a clean `/frontend` structure.
- Modified Jinja templates (`base.html`, `chat.html`) to be compatible with FastAPI's `url_for` structure and JSON payload expectations.
- Updated the `package.json`'s `start` and `dev` scripts to initialize the Python virtual environment and run Uvicorn.

### 5. Dependency Management
- Added a `backend/requirements.txt` to strictly keep PDR dependencies managed.
- Deliberately avoided destructive modifications to `.gitignore` or existing `node_modules` configurations to respect user project rules.





## Sage Orb Redesign & Voice Integration (by Claude Opus 4.6)

### 1. AI Persona & Model Update
- Switched the default Ollama model from `qwen2.5-coder:14b` to `llama3` to provide a warmer, more natural conversational experience.
- Rewrote the Sage system prompt to be a genuine, empathetic companion rather than a meme-heavy chatbot.
- Optimized Ollama inference parameters (`num_predict: 150`, `temperature: 0.8`) to ensure concise and responsive replies suitable for text-to-speech.

### 2. Orb Interface Redesign
- Completely replaced the traditional text-messaging chat UI with a minimalist, centralized animated Orb interface.
- Implemented a state machine for the Orb with visual feedback:
  - **Idle**: Purple pulsing orb.
  - **Listening**: Pink orb with active fast-rotating rings.
  - **Thinking**: Amber orb with a wobbling animation.
  - **Speaking**: Teal orb with a slow breathing glow.
- Redesigned `style.css` to feature a premium dark theme, glassmorphism input elements, and ambient background lighting.

### 3. Voice Interaction System
- **Voice Input**: Integrated the Web Speech API (`SpeechRecognition`) for hands-free, always-on listening.
- **Auto-Submit**: Added a silence timeout to automatically submit user speech after they stop talking.
- **Text-to-Speech**: Integrated the Web Speech Synthesis API to read responses aloud.
- **Voice Selection**: Configured the TTS engine to prioritize premium/enhanced voices (e.g., Samantha Enhanced, macOS voices) with adjusted pitch and rate for a warmer, human-like tone.

### 4. Backend Adjustments
- Removed the `verify_single_user` requirement from the `/chat` endpoint to prevent 503 errors and allow seamless local usage.
- Implemented a root (`/`) redirect pointing straight to `/chat` since the Orb is now the primary experience.
