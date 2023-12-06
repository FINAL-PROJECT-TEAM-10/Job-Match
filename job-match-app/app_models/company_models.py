from typing import Optional
from pydantic import BaseModel, EmailStr

from app_models.validation_models import ALLOWED_USERNAME

class Company(BaseModel):
    id: Optional[int] = None
    group: str = 'companies'
    username: ALLOWED_USERNAME
    email: EmailStr
    work_address: str
    telephone: str
    country: str
    city: str
    blocked: Optional[bool] = 0
    approved: Optional[bool] = 1

    @classmethod
    def from_query_result(cls, id, username, email,
                            work_address, telephone, country, city, blocked):
        return cls(id=id,
                   username=username,
                   email=email,
                   work_address=work_address,
                   telephone=telephone,
                   country=country,
                   city=city,
                   blocked=blocked,
                   group='companies')
