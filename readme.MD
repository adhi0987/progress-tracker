# Progress Tracker

Progress Tracker is a small study/productivity web app that helps users upload and manage study PDFs, mark tasks completed, track progress, and use a focused practice timer.

This document gives a clear summary of the project, how it works, how to run it locally, and the API surface used by the frontend. The repository also contains a dedicated backend technical README at [server/readme.md](server/readme.md) with an in-depth reference — this file consolidates the most important usage and technical points so you don't miss anything.

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
- Backend technical reference (summary)
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
- `server/app.py` — main FastAPI application, CORS and static file mount.
- `server/routers/userRouters.py` — API endpoints registered under `/api`.
- `server/services/UserServices.py` and `server/services/PdfService.py` — core business logic.
- `server/models/models.py` — SQLAlchemy models for `User` and `PdfFile`.
- `server/database/database.py` — engine and `get_db` session dependency.
- `server/auth` — JWT helpers, password hashing, and permit/permission config.
- `server/schemas` — pydantic request/response models.
- `client/src/api.ts` — Axios instance that attaches the JWT bearer token.

API — concise reference (base URL: `http://localhost:8000`)

All backend endpoints are mounted under the `/api` prefix (see `app.include_router(...)`). Authentication uses Bearer JWT tokens returned on signup/login.

- POST `/api/signup`
  - Body: JSON `{ name, email, username, password }`
  - Returns: `{ access_token, token_type }` (see `server/schemas/signupResponseModel.py`)

- POST `/api/login`
  - Body: JSON `{ username, password }`
  - Returns: `{ access_token, token_type }`

- POST `/api/upload_pdf` (auth required)
  - Form-data: `file` (PDF)
  - Stores file to `uploads/<filename>` and creates DB entry.

- GET `/api/pdfs` (auth required)
  - Returns: list of PDFs for the current user.

- PUT `/api/pdfs/{pdf_id}/toggle` (auth required)
  - Toggles `completed` and sets/unsets `completed_at` timestamp.

- DELETE `/api/pdfs/{pdf_id}` (auth required)
  - Deletes DB record and removes file from `uploads/` if present.

- GET `/api/progress` (auth required)
  - Returns: `{ total_pdfs, completed_pdfs, progress_percentage }`.

- GET `/api/completed_pdfs_in_particular_day/{completed_at}` (auth required)
  - Path param: `completed_at` (ISO date / datetime). Returns number completed that day.

Authentication & permissions
- Tokens: JWT HS256 created in `server/auth/auth.py` (expires by default; adjust in auth config).
- Send header: `Authorization: Bearer <token>`.
- Permission checks: endpoints and services use `permit.check(...)` (configured in `server/auth/permitConfig.py`) and may return `403` for unauthorized actions. New users are synced and assigned roles via `UserServices.create_user`.

Backend technical reference (summary)
- Entrypoint: [server/app.py](server/app.py) — mounts `/uploads`, configures CORS, and includes routers.
- PDF storage: `PdfService.save_pdf` writes files to `uploads/` and creates `PdfFile` rows.
- Progress logic: `PdfService.get_progress` computes counts and percentage.
- User flows: `UserService.create_user` (creates DB user, hashes password, syncs with permit service); `UserService.authenticate_user` verifies credentials.
- DB auto-migration: `Base.metadata.create_all(bind=engine)` runs on startup to create missing tables.

Testing
- Tests live in `server/tests/` — run with:

```bash
pytest -q
```

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

uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
```

Frontend (client)
```powershell
cd .\client
npm install
$env:VITE_BASE_URL = "http://localhost:8000"
npm run dev
```

Open the Vite dev URL (usually `http://localhost:5173`) and use the test credentials or sign up.

Deployment notes
- Ensure environment variables are set in production: `DATABASE_URL`, `SECRET_KEY`, and permit/permission configuration keys (see `server/auth/permitConfig.py`).
- If you use a remote file store for PDFs, modify `PdfService.save_pdf` and the static files mount accordingly.

Troubleshooting
- If uploads fail, confirm `uploads/` exists and the backend has write permission.
- If JWT validation fails, verify `SECRET_KEY` is consistent and tokens haven't expired.
- Permission-related `403` responses usually point to permit config, role assignments, or missing user sync.

Next suggested improvements
- Add `server/.env.example` and an automated seeding script for the `test` user.
- Add pagination/filtering for `/api/pdfs` and stricter filename sanitization.
- Add integration tests for permission and upload flows.

Where to read more
- Full backend technical documentation is available at [server/readme.md](server/readme.md) (contains detailed schema and file map).

---
Updated: 2025-12-19
