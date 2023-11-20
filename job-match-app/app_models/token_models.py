from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class ActivationData(BaseModel):
    id: int
    email: str
    group: str
    purpose: str