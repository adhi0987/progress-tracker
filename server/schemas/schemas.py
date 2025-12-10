from pydantic import BaseModel
from datetime import datetime

#Schemas for Signup 
class SignupRequestModel(BaseModel):
    username: str
    email: str
    name: str
    password: str

class SignupResponseModel(BaseModel):
    access_token: str
    token_type: str

class LoginRequestModel(BaseModel):
    username: str
    password: str   

class LoginResponseModel(BaseModel):
    access_token: str
    token_type: str

class uploadPdfResponseModel(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    completed: bool
    access_token: str
    token_type: str  

class pdfResponseModel(BaseModel):
    PdfList : list
    acess_token: str
    token_type: str

class togglePdfResponseModel(BaseModel):
    id: int
    filename: str
    completed: bool
    access_token: str
    token_type: str

class ProgressResponseModel(BaseModel):
    total_pdfs: int
    completed_pdfs: int
    progress_percentage: float
    acess_token: str
    token_type: str
# #
# class UserBase(BaseModel):
#     username: str
#     email: str
#     name: str

# class UserCreate(UserBase):
#     password: str

# class UserLogin(BaseModel):
#     username: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class PdfFileBase(BaseModel):
#     id: int
#     filename: str
#     completed: bool
#     upload_time: datetime

#     class Config:
#         from_attributes = True

# class ProgressResponse(BaseModel):
#     total_pdfs: int
#     completed_pdfs: int
#     progress_percentage: float