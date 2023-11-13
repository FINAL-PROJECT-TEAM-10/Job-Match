from datetime import date,datetime
from pydantic import BaseModel

class Job_ad(BaseModel):
    description: str
    min_salary: int
    max_salary: int
    status: str
    date_posted: datetime

    @classmethod
    def from_query_result(cls, description, min_salary,max_salary, staus,date_posted):
        return cls(
            description= description,
            min_salary=min_salary,
            max_salary = max_salary,
            staus= staus,
            date_posted=date_posted,
            )