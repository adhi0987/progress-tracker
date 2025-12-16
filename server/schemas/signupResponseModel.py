from pydantic import BaseModel

class SignupResponseModel(BaseModel):
    access_token: str
    token_type: str