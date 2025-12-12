from sqlalchemy.orm import Session
from fastapi import HTTPException,status, UploadFile
import os
import shutil
from datetime import datetime
import server.models.models as models
import  server.auth.auth  as auth



class PdfService:
    @staticmethod
    def save_pdf(db:Session,file:UploadFile,user_id:int):
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        new_pdf = models.PdfFile(
            filename=file.filename,
            filepath=file_location,
            user_id=user_id
        )
        db.add(new_pdf)
        db.commit()
        db.refresh(new_pdf)
        return new_pdf
    @staticmethod
    def get_all_pdfs(db:Session,user_id:int):
        return db.query(models.PdfFile).filter(models.PdfFile.user_id == user_id).all()
    @staticmethod
    def mark_pdf_completed(db:Session,pdf_id:int,user_id:int):
        pdf = db.query(models.PdfFile).filter(models.PdfFile.id == pdf_id,models.PdfFile.user_id == user_id).first()
        if not pdf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF not found")
        pdf.completed = not pdf.completed
        if pdf.completed:
            pdf.completed_at = auth.datetime.utcnow()
        else:
            pdf.completed_at = None
        db.commit()
        db.refresh(pdf)
        return pdf
    @staticmethod
    def delete_pdf(db:Session,pdf_id:int,user_id:int):
        pdf = db.query(models.PdfFile).filter(models.PdfFile.id == pdf_id,models.PdfFile.user_id == user_id).first()
        if not pdf:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF not found")
        db.delete(pdf)
        db.commit()
        # Optionally, delete the file from the filesystem
        if os.path.exists(pdf.filepath):
            os.remove(pdf.filepath)
        return
    @staticmethod
    def get_progress(db:Session,user_id:int):
        total_pdfs = db.query(models.PdfFile).filter(models.PdfFile.user_id == user_id).count()
        completed_pdfs = db.query(models.PdfFile).filter(models.PdfFile.user_id == user_id, models.PdfFile.completed == True).count()
        progress_percentage = (completed_pdfs / total_pdfs * 100) if total_pdfs > 0 else 0.0
        return total_pdfs, completed_pdfs, progress_percentage
    @staticmethod
    def get_completed_pdfs_in_particular_day(db:Session,user_id:int,day:datetime):
        start_of_day = datetime(day.year, day.month, day.day)
        end_of_day = datetime(day.year, day.month, day.day, 23, 59, 59)
        count = db.query(models.PdfFile).filter(
            models.PdfFile.user_id == user_id,
            models.PdfFile.completed == True,
            models.PdfFile.completed_at >= start_of_day,
            models.PdfFile.completed_at <= end_of_day
        ).count()
        return count