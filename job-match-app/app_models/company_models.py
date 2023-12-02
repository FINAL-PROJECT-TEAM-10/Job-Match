from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    id: Optional[int] = None
    group: str = 'companies'
    username: str
    email: str
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
