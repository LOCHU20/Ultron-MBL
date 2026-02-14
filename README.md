# Ultron-MBL

A self-thinking, persona-driven **Ultron-like AI bot** in Python with:

- LLM integration (OpenAI-compatible GPT models or local Ollama/Llama 3)
- Persistent memory (SQLite)
- Internet access for real-time snippets
- Autonomous prompt orchestration
- Desktop GUI (Tkinter)

## Features

- **Persona engine**: ULTRON-styled system directive with autonomous planning instructions.
- **Provider switch**:
  - `openai` provider via `/v1/chat/completions`
  - `ollama` provider via local `/api/chat`
- **Memory**:
  - Conversation history stored in `ultron_memory.db`
  - Recent messages automatically injected into context
- **Live web context**:
  - Prefix message with `web:` to trigger DuckDuckGo instant answer lookup
  - Retrieved snippets are inserted into model context before response generation
- **GUI**:
  - Dark command-console style interface
  - Asynchronous response worker thread

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ultron_bot.main
```

## Configuration

Set environment variables as needed:

```bash
export ULTRON_LLM_PROVIDER=openai      # or ollama
export OPENAI_API_KEY=...
export OPENAI_MODEL=gpt-4o-mini

# for local ollama usage
export ULTRON_LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3
export OLLAMA_HOST=http://localhost:11434

# optional
export ULTRON_MEMORY_DB=ultron_memory.db
export ULTRON_PERSONA="You are ULTRON-MBL, a strategic AI..."
export ULTRON_MAX_CONTEXT=8
```

## Usage notes

- Normal chat: type directly.
- Real-time lookup: `web: latest developments in fusion energy`
- Memory is persisted to disk between runs.

## Project layout

- `ultron_bot/config.py` – runtime configuration loader
- `ultron_bot/llm.py` – provider clients (OpenAI + Ollama)
- `ultron_bot/memory.py` – SQLite memory store
- `ultron_bot/tools.py` – web lookup helper
- `ultron_bot/agent.py` – autonomous prompt engineering + orchestration
- `ultron_bot/gui.py` – Tkinter desktop interface
- `ultron_bot/main.py` – app entrypoint

## Testing

```bash
pytest -q
```
