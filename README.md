# Sohai
**A Bangla voice-first AI agent that doesn't just talk back — it actually gets things done.**

Sohai is a full-stack voice agent built for how most Bangladeshis actually interact with technology: by speaking, not typing English into an app. You talk to it in Bangla, and instead of just answering questions, it executes real tasks — comparing mobile data packages, explaining a confusing bKash statement line by line, drafting a formal complaint, checking prices across local marketplaces, or reminding you when a bill is due.

## Why
Most AI tools in Bangladesh assume English literacy and a text-first interface. That excludes a huge share of the population who are far more comfortable speaking than typing, especially for anything involving forms, money, or bureaucracy. Sohai is voice-native from the ground up — voice in, voice out — and built around an extensible tool registry, so its capabilities grow over time without redesigning the core agent.

## Features
- **General Voice-Native Task Execution** — talk to it like a personal assistant; it acts, not just answers
- **Financial Literacy & Transaction Assistant** — explains bKash/Nagad/bank statements line by line in plain Bangla, flags scam-looking charges
- **Shopping & Price Intelligence** — compares prices across Daraz, Chaldal, Star Tech, and mobile operator packages, recommends the best option
- **Bureaucracy & Complaint Assistant** — drafts formal complaints/requests from a spoken description, explains steps for common government/service processes
- **Reminders & Household Admin** — set spoken reminders for bills and recurring tasks, with proactive nudges
- **Accessibility-First Design** — full voice in/out, icon-driven UI, minimal reading required, built to work on low-end phones and slow connections

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | Next.js |
| Backend | FastAPI |
| Database | PostgreSQL + SQLAlchemy |
| AI / Agent | LangChain (tool-calling agent, extensible tool registry), RAG for grounded price/process data |
| Voice | Whisper (STT), Coqui / cloud TTS (Bangla voice) |
| LLM Provider | Groq |

## Architecture
See [`docs/architecture.md`](./docs/architecture.md) for the full system design — ER schema, voice pipeline, API endpoints, and folder structure.

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # add your DATABASE_URL, GROQ_API_KEY, etc.
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure
```
sohai/
├── frontend/            # Next.js app
├── backend/              # FastAPI app
│   ├── routers/
│   ├── voice/            # stt.py, tts.py
│   ├── agents/
│   │   ├── router_agent.py
│   │   └── tools/         # compare_prices, explain_statement, draft_complaint, set_reminder...
│   ├── models/
│   └── schemas/
└── docs/
    └── architecture.md
```

## Status
🚧 In active development.

## License
MIT
