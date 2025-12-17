from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,status
from sqlalchemy.orm import Session
from datetime import datetime
from server.database.database import get_db
from server.models import models
from server.auth import auth
from server.dependencies.dependencies import get_current_user
from server.services.UserServices import UserService 
from server.services.PdfService import PdfService
from server.schemas.completedPdfsInParticularDayResponseModel import CompletedPdfsInParticularDayResponseModel
from server.schemas.uploadPdfResponseModel import uploadPdfResponseModel
from server.schemas.pdfResponseModel import pdfResponseModel
from server.schemas.togglePdfResponseModel import togglePdfResponseModel
from server.schemas.progressResponseModel import ProgressResponseModel
from server.schemas.loginRequestModel import LoginRequestModel
from server.schemas.loginResponseModel import LoginResponseModel
from server.schemas.signupRequestModel import SignupRequestModel
from server.schemas.signupResponseModel import SignupResponseModel
from server.auth.permitConfig import permit 
#create Router
router = APIRouter()


@router.post("/signup", response_model=SignupResponseModel)
async def signup(user: SignupRequestModel, db: Session = Depends(get_db)):
    new_user = await UserService.create_user(db, user)
    access_token = auth.create_access_token(data={"sub": new_user.username})
    return SignupResponseModel(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/login", response_model=LoginResponseModel)
def login(userLoginData: LoginRequestModel, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, userLoginData)
    access_token = auth.create_access_token(data={"sub": user.username})
    return LoginResponseModel(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/upload_pdf", response_model=uploadPdfResponseModel)
async def upload_pdf(
    file: UploadFile = File(...), 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    permitted = await permit.check(current_user.username, "create", "pdf_document")
    if not permitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to upload PDF")
    


    new_pdf = PdfService.save_pdf(db, file, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return uploadPdfResponseModel(
        id=new_pdf.id,
        filename=new_pdf.filename,
        upload_time=new_pdf.upload_time,
        completed=False,
        access_token=access_token,
        token_type="bearer"
    )

@router.get("/pdfs", response_model=pdfResponseModel)
async def get_pdfs(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # return db.query(models.PdfFile).filter(models.PdfFile.user_id == current_user.id).all()

    permitted =  await permit.check(current_user.username,"read","pdf_document")
    if not permitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view PDFs")
    
    pdfs = PdfService.get_all_pdfs(db, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return pdfResponseModel(
        PdfList=pdfs,
        access_token=access_token,
        token_type="bearer"
    )


@router.put("/pdfs/{pdf_id}/toggle", response_model=togglePdfResponseModel)
async def toggle_pdf_completion(
    pdf_id: int, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    permitted = await permit.check(
        user = current_user.username,
        action = "update",
        resource = "pdf_document"
    )
    if not permitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update PDF status")
    

    pdf = PdfService.mark_pdf_completed(db, pdf_id, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return togglePdfResponseModel(
        id=pdf.id,
        filename=pdf.filename,
        completed=pdf.completed,
        access_token=access_token,
        token_type="bearer"
    )

@router.delete("/pdfs/{pdf_id}", status_code=204)
async def delete_pdf(
    pdf_id: int, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
): 
    permitted =  await permit.check(
        user = current_user.username,
        action = "delete",
        resource = "pdf_document"
    )
    if not permitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete PDF")
    PdfService.delete_pdf(db, pdf_id, current_user.id)    
    return

@router.get("/progress", response_model=ProgressResponseModel) 
async def get_progress(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_pdfs,completed_pdfs,progress_percentage = PdfService.get_progress(db, current_user.id)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return ProgressResponseModel(
        total_pdfs=total_pdfs,
        completed_pdfs=completed_pdfs,
        progress_percentage=progress_percentage,
        access_token=access_token,
        token_type="bearer"
    ) 


@router.get("/completed_pdfs_in_particular_day/{completed_at}", response_model=CompletedPdfsInParticularDayResponseModel)
def get_completed_pdfs_in_particular_day(
    completed_at: datetime,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    number_of_completed_pdfs = PdfService.get_completed_pdfs_in_particular_day(db, current_user.id, completed_at)
    access_token = auth.create_access_token(data={"sub": current_user.username})
    return CompletedPdfsInParticularDayResponseModel(
        NumberofCompletedPdfs=number_of_completed_pdfs,
        access_token=access_token,
        token_type="bearer"
    )
       