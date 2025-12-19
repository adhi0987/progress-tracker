
# Progress Tracker — Backend README

**Overview**
- **Project:** Progress Tracker backend (FastAPI).
- **Purpose:** Provides user auth, PDF upload/management, progress tracking, and permission checks.
- **Main app:** [server/app.py](server/app.py)

**Quick Start**
- **Create venv & install:**

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

- **Run locally:**

```bash
uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
```

**Environment / Config**
- See `requirements.txt` for Python deps.
- Environment variables expected (common):
	- `DATABASE_URL` — SQLAlchemy DB connection string (e.g. sqlite or postgres).
	- `SECRET_KEY` — JWT signing secret used in `server/auth/auth.py`.
	- `PERMIT_API_KEY` / Permit config — used by permission sync in `UserServices` (see `server/auth/permitConfig.py`).

**Architecture & Components**
- **Framework:** FastAPI — entrypoint: [server/app.py](server/app.py).
- **Routers:** [server/routers/userRouters.py](server/routers/userRouters.py) — exposes API under `/api` prefix.
- **Services:** Business logic lives in:
	- [server/services/UserServices.py](server/services/UserServices.py) — user creation, auth helper calls, permission sync.
	- [server/services/PdfService.py](server/services/PdfService.py) — save/delete/toggle PDFs and compute progress.
- **Auth & Permissions:**
	- JWT helpers and password hashing live in [server/auth/auth.py](server/auth/auth.py).
	- Permission integration via `permit` in [server/auth/permitConfig.py](server/auth/permitConfig.py) and used by services and routers.
- **Database:** SQLAlchemy models in [server/models/models.py](server/models/models.py) and DB utilities in [server/database/database.py](server/database/database.py).
- **Dependencies:** Auth dependency `get_current_user` in [server/dependencies/dependencies.py](server/dependencies/dependencies.py).

**API Reference (summary)**
All endpoints are registered under the `/api` prefix (see `app.include_router(...)`). Authentication uses Bearer JWT tokens returned on signup/login.

- **POST /api/signup**
	- Request: `SignupRequestModel`
	- Response: JWT token (`SignupResponseModel`)
	- Implementation: `UserService.create_user` syncs user to permission service.

- **POST /api/login**
	- Request: `LoginRequestModel`
	- Response: JWT token (`LoginResponseModel`)
	- Implementation: `UserService.authenticate_user` verifies credentials.

- **POST /api/upload_pdf**
	- Auth: required (dependency `get_current_user`).
	- Input: multipart file (`UploadFile`).
	- Response: `uploadPdfResponseModel` with created PDF metadata and refreshed token.
	- Implementation: `PdfService.save_pdf` stores file to `uploads/` and records DB entry.

- **GET /api/pdfs**
	- Auth: required.
	- Response: `pdfResponseModel` — list of PDFs for the current user.
	- Implementation: `PdfService.get_all_pdfs`.

- **PUT /api/pdfs/{pdf_id}/toggle**
	- Auth: required.
	- Response: `togglePdfResponseModel` — toggled completed flag.
	- Implementation: `PdfService.mark_pdf_completed` (flips `completed` and timestamps `completed_at`).

- **DELETE /api/pdfs/{pdf_id}**
	- Auth: required.
	- Response: 204 No Content on success.
	- Implementation: `PdfService.delete_pdf` (also removes file from filesystem if present).

- **GET /api/progress**
	- Auth: required.
	- Response: `ProgressResponseModel` with `total_pdfs`, `completed_pdfs`, `progress_percentage`.
	- Implementation: `PdfService.get_progress`.

- **GET /api/completed_pdfs_in_particular_day/{completed_at}**
	- Auth: required.
	- Path param: `completed_at` (datetime).
	- Response: `CompletedPdfsInParticularDayResponseModel` — count for the day.

**Models / Schemas**
- Schemas live in [server/schemas/](server/schemas) and define request/response shapes, e.g. `signupRequestModel.py`, `loginResponseModel.py`, `pdfResponseModel.py`.

**Database**
- Models: [server/models/models.py](server/models/models.py).
- DB engine & session helpers: [server/database/database.py](server/database/database.py).
- On startup the app calls `Base.metadata.create_all(bind=engine)` (see [server/app.py](server/app.py)) to create tables automatically.

**Uploads / Static Files**
- The uploads directory is created at runtime and mounted at `/uploads` (see [server/app.py](server/app.py)). Uploaded PDF files are saved to `uploads/<filename>` by `PdfService.save_pdf`.

**Testing**
- Tests are present in [server/tests/](server/tests). Run them with:

```bash
pytest -q
```

**Error handling & permission checks**
- Many endpoints call `permit.check(...)` (see `server/auth/permitConfig.py`) and will raise `HTTPException(status_code=403)` if the action is not allowed.
- Service methods raise `HTTPException` with appropriate status codes for not-found and auth errors.

**File Map (important files)**
- [server/app.py](server/app.py) — FastAPI app, CORS, static files, router inclusion.
- [server/routers/userRouters.py](server/routers/userRouters.py) — API endpoints.
- [server/services/UserServices.py](server/services/UserServices.py) — user create/auth and permission sync.
- [server/services/PdfService.py](server/services/PdfService.py) — PDF persistence and progress logic.
- [server/models/models.py](server/models/models.py) — SQLAlchemy models.
- [server/database/database.py](server/database/database.py) — DB engine & session.
- [server/auth](server/auth) — auth helpers and permit config.
- [server/schemas](server/schemas) — pydantic models for requests/responses.
- [server/dependencies/dependencies.py](server/dependencies/dependencies.py) — `get_current_user` dependency.

**Deployment notes**
- Ensure environment variables (`DATABASE_URL`, `SECRET_KEY`, permit config) are set in the target environment.
- If using a cloud file store or different filesystem layout, adapt `PdfService.save_pdf` and the static files mount.

**Troubleshooting**
- If uploads fail, check that the `uploads` directory exists and the process has write permissions.
- If JWT auth fails, verify `SECRET_KEY` matches between token creation and verification.
- Permission-related 403s indicate permit.io configuration or role assignments (see `UserServices.create_user`).

**Next steps / Suggestions**
- Add pagination and filtering for `/api/pdfs`.
- Add rate limiting and stricter filename sanitization for uploads.
- Add integration tests for permission flows.

---
Last updated: generated by documentation tooling.
