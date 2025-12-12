from sqlalchemy.orm import Session
from fastapi import HTTPException,status, UploadFile
import os
import shutil
from datetime import datetime

import server.models.models as models
import server.schemas.schemas as schemas
import  server.auth.auth  as auth 


class UserService:
    @staticmethod
    def create_user(db:Session, user:schemas.SignupRequestModel):
        #check if user already exists
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        hashed_password = auth.get_password_hash(user.password)
        new_user = models.User(
            username=user.username,
            email=user.email,
            name=user.name,
            password_hash=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    @staticmethod
    def authenticate_user(db:Session,user:schemas.LoginRequestModel):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if not db_user or not auth.verify_password(user.password, db_user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        return db_user
    @staticmethod
    def get_user_by_username(db:Session,username:str):
        return db.query(models.User).filter(models.User.username == username).first()