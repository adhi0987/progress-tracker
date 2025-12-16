from pydantic import BaseModel
from datetime import datetime

class PdfItemModel(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    completed: bool

    class Config:
        from_attributes = True