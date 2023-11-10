from datetime import date
from pydantic import BaseModel

class Job_ad(BaseModel):
    description: str
    min_salary: int
    max_salary: int
    status: str
    date_posted: date
    name_of_company: str

    @classmethod
    def from_query_result(cls, description, min_salary,max_salary, staus,date_posted,name_of_company):
        return cls(
            description= description,
            min_salary=min_salary,
            max_salary = max_salary,
            staus= staus,
            date_posted=date_posted,
            name_of_company = name_of_company)