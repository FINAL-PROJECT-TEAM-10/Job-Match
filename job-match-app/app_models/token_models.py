from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

#TODO: Finish Token Data by Type
class TokenDataAdmin(BaseModel):
    pass

class TokenDataUser(BaseModel):
    pass

class TokenDataCompany(BaseModel):
    pass