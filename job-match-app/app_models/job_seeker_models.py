from typing import Optional

from pydantic import BaseModel


# TODO: Consider constraints for strings
# TODO: Look into BLOBs for picture
class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    first_name: str
    last_name: str
    summary: Optional[str] = None
    picture: Optional[str] = None
    busy: bool
    blocked: bool
    approved: bool

    email = str
    address = Optional[str] = None
    phone = Optional[str] = None
    post_code = Optional[str] = None

    location = str