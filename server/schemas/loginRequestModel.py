from pydantic  import BaseModel, ConfigDict
class LoginRequestModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str 