from pydantic  import BaseModel
class LoginRequestModel(BaseModel):
    username: str
    password: str  