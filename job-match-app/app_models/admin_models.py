from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Admin(BaseModel):
    id: Optional[int] = None
    group: str = 'admins'
    username: str
    first_name: str
    last_name: str
    summary: Optional[str] = None
    picture: Optional[str] = None

    email: str
    address: Optional[str] = None
    phone: Optional[str] = None

    city: str
    country: str

    @classmethod
    def from_query_results(cls, id, username, first_name, last_name, picture,
                           email, address, telephone,
                           city, country):
        return cls(
            id=id, group='admins',
            username=username, first_name=first_name, last_name=last_name,
            picture=picture,
            email=email, address=address, phone=telephone,
            city=city, country=country
        )

