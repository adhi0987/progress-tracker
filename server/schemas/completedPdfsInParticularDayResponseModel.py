from pydantic import BaseModel

class CompletedPdfsInParticularDayResponseModel(BaseModel):
    NumberofCompletedPdfs: int
    access_token: str
    token_type: str