from pydantic import BaseModel, ConfigDict

class SignupRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str
    name: str
    password: str