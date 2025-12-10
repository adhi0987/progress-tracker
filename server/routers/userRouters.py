from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,status
from sqlalchemy.orm import Session
from typing import List
import shutil
import os

from server.database.database import get_db
from server.models import models
from server.schemas import schemas
from server.auth import auth
from server.dependencies.dependencies import get_current_user
from server.services.services import UserService ,PdfService

#create Router
router = APIRouter()


@router.post("/signup", response_model=schemas.SignupResponseModel)
def signup(user: schemas.SignupRequestModel, db: Session = Depends(get_db)):
    new_user = UserService.create_user(db, user)
    access_token = auth.create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.LoginResponseModel)
def login(userLoginData: schemas.LoginRequestModel, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, userLoginData)
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload_pdf", response_model=schemas.uploadPdfResponseModel)
async def upload_pdf(
    file: UploadFile = File(...), 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_pdf = PdfService.save_pdf(db, file, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return {
        "id": new_pdf.id,
        "filename": new_pdf.filename,
        "upload_time": new_pdf.upload_time,
        "completed": False,
        "access_token": access_token,
        "token_type": "bearer"
    }

    # file_location = f"uploads/{file.filename}"
    # with open(file_location, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
        
    # new_pdf = models.PdfFile(
    #     filename=file.filename,
    #     filepath=file_location,
    #     user_id=current_user.id
    # )
    # db.add(new_pdf)
    # db.commit()
    # db.refresh(new_pdf)
    # return new_pdf

@router.get("/pdfs", response_model=schemas.pdfResponseModel)
def get_pdfs(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # return db.query(models.PdfFile).filter(models.PdfFile.user_id == current_user.id).all()
    pdfs = PdfService.get_all_pdfs(db, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return {
        "PdfList": pdfs,
        "acess_token": access_token,
        "token_type": "bearer"
    }


@router.put("/pdfs/{pdf_id}/toggle", response_model=schemas.togglePdfResponseModel)
def toggle_pdf_completion(
    pdf_id: int, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # pdf = db.query(models.PdfFile).filter(models.PdfFile.id == pdf_id, models.PdfFile.user_id == current_user.id).first()
    # if not pdf:
    #     raise HTTPException(status_code=404, detail="PDF not found")
    
    # pdf.completed = not pdf.completed
    # if pdf.completed:
    #     pdf.completed_at = auth.datetime.utcnow()
    # else:
    #     pdf.completed_at = None
        
    # db.commit()
    # db.refresh(pdf)
    # return pdf
    pdf = PdfService.mark_pdf_completed(db, pdf_id, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return {
        "id": pdf.id,
        "filename": pdf.filename,
        "completed": pdf.completed,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.delete("/pdfs/{pdf_id}", status_code=204)
def delete_pdf(
    pdf_id: int, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # pdf = db.query(models.PdfFile).filter(models.PdfFile.id == pdf_id, models.PdfFile.user_id == current_user.id).first()
    # if not pdf:
    #     raise HTTPException(status_code=404, detail="PDF not found")
    
    # # Delete the file from the filesystem
    # if os.path.exists(pdf.filepath):
    #     os.remove(pdf.filepath)
    
    # db.delete(pdf)
    # db.commit()
    # return  
    PdfService.delete_pdf(db, pdf_id, current_user.id)    
    return

@router.get("/progress", response_model=schemas.ProgressResponseModel) 
def get_progress(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # total_pdfs = db.query(models.PdfFile).filter(models.PdfFile.user_id == current_user.id).count()
    # completed_pdfs = db.query(models.PdfFile).filter(models.PdfFile.user_id == current_user.id, models.PdfFile.completed == True).count()
    
    # # progress_percentage = (completed_pdfs / total_pdfs * 100) if total_pdfs > 0 else 0.0
    
    # return schemas.ProgressResponse(
    #     total_pdfs=total_pdfs,
    #     completed_pdfs=completed_pdfs,
    #     progress_percentage=progress_percentage
    # ) 
    progress_data = PdfService.get_progress(db, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return {
        "total_pdfs": progress_data["total_pdfs"],
        "completed_pdfs": progress_data["completed_pdfs"],
        "progress_percentage": progress_data["progress_percentage"],
        "acess_token": access_token,
        "token_type": "bearer"
    }  


@router.get("/completed_pdfs_in_particular_day/{completed_at}", response_model=schemas.pdfResponseModel)
def get_completed_pdfs_in_particular_day(
    completed_at: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        date_obj = auth.datetime.strptime(completed_at, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    start_datetime = auth.datetime.combine(date_obj, auth.datetime.min.time())
    end_datetime = auth.datetime.combine(date_obj, auth.datetime.max.time())
    
    completed_pdfs = db.query(models.PdfFile).filter(
        models.PdfFile.user_id == current_user.id,
        models.PdfFile.completed == True,
        models.PdfFile.completed_at >= start_datetime,
        models.PdfFile.completed_at <= end_datetime
    ).all()
    
    return completed_pdfs   