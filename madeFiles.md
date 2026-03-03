# PDR Implementation Files

Overview of the files created or modified for the Personal Data Repository (PDR) architecture:

## Backend (`/backend`)
- **`main.py`**: The core FastAPI application. Sets up routes for serving the frontend templates, handling the `/chat` endpoint using the local Ollama LLM (`qwen2.5-coder:14b`), and handling document ingestion via `/ingest`.
- **`database.py`**: SQLAlchemy configuration for the local SQLite database (`pdr.db`). Contains models for `ConversationLog` and `DocumentMetadata` to maintain history and record ingested files locally.
- **`rag.py`**: Contains the retrieval-augmented generation logic using ChromaDB and `sentence-transformers` (`all-MiniLM-L6-v2`). Exposes functions to split text, embed it, store it in the vector store, and search for similar documents.
- **`requirements.txt`**: The Python dependencies required for the backend (`fastapi`, `uvicorn`, `chromadb`, `sentence-transformers`, `sqlalchemy`, etc.).

## Frontend (`/frontend`)
- **`templates/base.html`**: The unified layout structure, updated to use FastAPI's static path formatting.
- **`templates/chat.html`**: The main chat interface, modified to send JSON payloads to the FastAPI backend.
- **`templates/index.html`**: The landing page.
- **`static/style.css` & `static/index.js`**: Core styling and visual behaviors, served directly by FastAPI.

## Data Directories
- **`/data`**: Stores the SQLite database (`pdr.db`).
- **`/vector_store`**: Stores the persistent ChromaDB embedding files.

## Project Root
- **`package.json`**: NPM and project metadata, updated specifically to add new `start` and `dev` scripts which launch the FastAPI server via Uvicorn.





## Sage Orb Redesign Files (Modified by Claude Opus 4.6)

### Backend (`/backend`)
- **`main.py`**: Updated the LLM configuration to use `llama3`. Rewrote the `SYSTEM_PROMPT` for the Sage companion persona. Adjusted the `/chat` endpoint by removing the `verify_single_user` dependency and implemented a redirect from the root `/` to `/chat`. Added inference tuning parameters to Ollama requests.

### Frontend (`/frontend`)
- **`templates/chat.html`**: Completely rewritten to replace the standard chat log with the central animated Orb UI. Contains the JavaScript logic for the Web Speech API (continuous listening, state machine) and Speech Synthesis (text-to-speech).
- **`static/style.css`**: Completely redesigned for a modern dark theme. Contains layout and advanced CSS animations for the four Orb states (idle, listening, thinking, speaking) and glassmorphism styling for text inputs.
- **`templates/base.html`**: Updated meta tags, added `theme-color` for dark mode, and set viewport to `user-scalable=no` for mobile optimization.
- **`templates/index.html`**: Updated to immediately redirect users to the new `/chat` interface.
