import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from server.database.database import engine,Base
from server.routers import userRouters
# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Progress Tracker API")

# CORS
origins = ["http://localhost:5173","https://progress-tracker-user-interface.onrender.com"] # Vite default port
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount 'uploads' folder to serve PDFs
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"),name="uploads")


# Include Routers
app.include_router(userRouters.router, prefix="/api")