# Progress Tracker

Progress Tracker is a small study/productivity web app that helps users upload and manage study PDFs, mark tasks completed, track progress, and use a focused practice timer.

This document gives a clear summary of the project, how it works, how to run it locally, and the API surface your frontend uses.

**Quick test credentials**
- Username: `test`
- Password: `test`

**One‑line architecture**
- Backend: FastAPI + SQLAlchemy (JWT auth, file uploads served from `uploads/`).
- Frontend: React + TypeScript (Vite) using Axios to call the backend.

Contents
- Project overview
- Features
- Files of interest
- API (endpoints + usage)
- Run locally (PowerShell commands)
- Troubleshooting & notes

Project overview
- Users sign up / log in; JWT tokens authenticate API calls.
- Users upload PDFs which are stored in `uploads/` and listed per user.
- Users can mark PDFs completed, delete PDFs, and view overall progress.
- A practice countdown timer helps focused study sessions.

Features
- Authentication: `/signup`, `/login` (JWT issued on success).
- PDF management: upload, list, view (served from `uploads/`), toggle completion, delete.
- Progress endpoint: aggregated stats (total, completed, percentage).
- Frontend components: login/signup forms, `PDFManager`, `ProgressStats`, `ClockTimer`, `Navbar`.

Files of interest (quick)
- `server/app.py` — main FastAPI application with all routes.
- `server/auth.py` — password hashing (`passlib`) and JWT creation/validation.
- `server/database.py` — SQLAlchemy engine and `get_db` dependency (requires `DATABASE_URL`).
- `server/models.py` — `User` and `PdfFile` ORM models.
- `server/requirements.txt` — backend dependencies.
- `client/src/api.ts` — Axios instance that adds `Authorization: Bearer <token>` automatically.
- `client/src/components/PDFManager.tsx` — upload/list/toggle/delete UI.
- `client/src/components/ProgressStats.tsx` — overall progress and daily chart.

API — concise reference
Base URL: default `http://localhost:8000` (change by running server on another port).

- POST /signup
  - Body: JSON { name, email, username, password }
  - Returns: { access_token, token_type }

- POST /login
  - Body: JSON { username, password }
  - Returns: { access_token, token_type }

- POST /upload_pdf (auth required)
  - Form-data: `file` (PDF)
  - Returns: uploaded `PdfFile` object

- GET /pdfs (auth required)
  - Returns: list of `PdfFile` objects for current user

- PUT /pdfs/{pdf_id}/toggle (auth required)
  - Toggles `completed` and sets/unsets `completed_at`
  - Returns: updated `PdfFile`

- DELETE /pdfs/{pdf_id} (auth required)
  - Deletes DB record and removes file from `uploads/`

- GET /progress (auth required)
  - Returns: { total_pdfs, completed_pdfs, progress_percentage }

- GET /completed_pdfs_in_particular_day/{YYYY-MM-DD} (auth required)
  - Returns: PDFs completed on that date

Authentication
- Tokens: JWT HS256 created in `server/auth.py`, expire after 30 minutes by default.
- Send header: `Authorization: Bearer <token>` (the frontend stores token in `localStorage` key `token`).

Run locally (PowerShell)
Prereqs: Python 3.9+, Node.js (16+), and a database (or SQLite file).

Backend (server)
```powershell
cd .\server
py -3 -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Example quick local database (SQLite):
$env:DATABASE_URL = "sqlite:///./progress_tracker.db"
$env:SECRET_KEY = "supersecretkey"

uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Frontend (client)
```powershell
cd ..\client
npm install
$env:VITE_BASE_URL = "http://localhost:8000"
npm run dev
```

Open the Vite dev URL (usually `http://localhost:5173`) and use the test credentials or sign up.

Troubleshooting & notes
- `server/database.py` requires `DATABASE_URL`. Set it or create `server/.env` with a `DATABASE_URL` entry.
- `uploads/` is created at runtime; ensure the backend process has write permissions to the repository folder.
- If the frontend cannot reach the API, confirm `VITE_BASE_URL` matches backend host/port and add CORS origin in `server/app.py` if needed.
- Do not use the sample `SECRET_KEY` or `test` credentials in production.

Next suggested small improvements
- Add a `server/.env.example` and a script to seed the `test` user for convenience.
- Add backend tests for API endpoints and a small README section describing expected DB schema for production.

If you want, I can add the `server/.env.example` and a seeding script now. 

---

Updated: 2025-12-18
