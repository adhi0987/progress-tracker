from pydantic import BaseModel, ConfigDict

class SignupResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str