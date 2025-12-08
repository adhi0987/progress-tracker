import os
import shutil
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from server.database.database import engine, get_db, Base
import server.models.models as models
import server.schemas.schemas as schemas
import server.auth.auth as auth

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Dependencies ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except auth.JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
