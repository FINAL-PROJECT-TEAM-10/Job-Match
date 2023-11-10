from pydantic import BaseModel

class Company(BaseModel):
    company_name: str
    email: str
    work_adress: str
    telephone: int
    country: str
    city: str

    @classmethod
    def from_company_result(cls,company_name,email,work_adress,telephone,country,city):
        return cls(
            company_name = company_name,
            email = email,
            work_adress = work_adress,
            telephone = telephone,
            country = country,
            city = city
        )