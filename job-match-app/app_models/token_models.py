from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class AccessDataModel(BaseModel):
    id: int
    group: str
    username: str
    email: str


class ActivationDataModel(BaseModel):
    id: int
    email: str
    username: str
    group: str
    purpose: str
