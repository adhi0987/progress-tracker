from pydantic import BaseModel 
from datetime import datetime

class uploadPdfResponseModel(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    completed: bool
    access_token: str
    token_type: str  