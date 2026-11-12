# EnvyLead

Voice-first lead capture for Indian real estate, built on **Gnani Prisma** speech-to-text and
**Gnani Timbre** text-to-speech.

EnvyLead turns a short customer enquiry into a structured lead that a human reviews and approves.
Approved leads are stored in SQLite and managed from a dashboard with search, filters, editing,
status tracking, and a recommended next action.

## Run locally

Backend (port 8001):
```
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env   # set GNANI_API_KEY
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Frontend (port 5173):
```
cd frontend
npm install
npm run dev
```

## Tests
```
cd backend && .venv\Scripts\python -m pytest -q
cd frontend && npm test && npm run build
```

## Environment
See `backend/.env.example`. Never commit `.env`. API keys stay on the backend.