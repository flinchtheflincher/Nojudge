# Nojudge (Voice-First Single-User PDR)

Working prototype for a local-first AI companion with:
- Single-user access lock
- Voice input (speech-to-text in browser)
- Voice output (AI reply spoken back)
- RAG over local ingested documents
- Local conversation memory (SQLite)

## Quick Start

1. Create/activate Python env and install backend deps:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

2. Set env vars for single-user mode + free API test:
```bash
export NOJUDGE_SINGLE_USER_KEY="choose-a-private-key"
export NOJUDGE_LLM_PROVIDER="gemini"
export GEMINI_API_KEY="your-free-gemini-api-key"
```

3. Run server:
```bash
npm run dev
```

4. Open:
```text
http://127.0.0.1:8000/chat
```

On first load, enter your owner key in the prompt.  
Use the mic button to speak; Nojudge transcribes, replies, and speaks back.

## Optional Local LLM Mode (No API Key)

If you want local-only inference:
```bash
export NOJUDGE_LLM_PROVIDER="ollama"
ollama pull qwen2.5-coder:14b
ollama serve
```

## Single-User Behavior

- `/chat` and `/ingest` require `X-Nojudge-Key`.
- The browser stores your key locally in `localStorage`.
- Without matching key, API calls are rejected (`401`).
