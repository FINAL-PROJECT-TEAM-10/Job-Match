from typing import Optional

from pydantic import BaseModel, EmailStr

from app_models.validation_models import ALLOWED_USERNAME


class Admin(BaseModel):
    id: Optional[int] = None
    group: str = 'admins'
    username: ALLOWED_USERNAME
    first_name: str
    last_name: str
    summary: Optional[str] = None
    picture: Optional[str] = None

    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None

    city: str
    country: str

    @classmethod
    def from_query_results(cls, id, username, first_name, last_name, email, address, telephone,
                           city, country):
        return cls(
            id=id, group='admins',
            username=username, first_name=first_name, last_name=last_name,
            email=email, address=address, phone=telephone,
            city=city, country=country
        )

