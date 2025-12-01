import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base



app = fastapi.FastAPI("Progress Tracker API")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload_pdf")
def upload_pdf(file: fastapi.UploadFile = fastapi.File(...)):
    return {"filename": file.filename}