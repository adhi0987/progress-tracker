from pydantic import BaseModel

class togglePdfResponseModel(BaseModel):
    id: int
    filename: str
    completed: bool
    access_token: str
    token_type: str