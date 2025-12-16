from pydantic import BaseModel

class ProgressResponseModel(BaseModel):
    total_pdfs: int
    completed_pdfs: int
    progress_percentage: float
    access_token: str
    token_type: str