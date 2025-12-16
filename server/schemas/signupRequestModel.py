from pydantic import BaseModel

class SignupRequestModel(BaseModel):
    username: str
    email: str
    name: str
    password: str