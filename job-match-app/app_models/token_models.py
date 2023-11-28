from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class ActivationData(BaseModel):
    id: int
    email: str
    username: str
    group: str
    purpose: str