from pydantic import BaseModel
class PasswordUpdater(BaseModel):
    old_password: str
    new_password: str