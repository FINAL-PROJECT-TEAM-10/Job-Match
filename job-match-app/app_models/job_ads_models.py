from datetime import date
from pydantic import BaseModel

class Job_ad(BaseModel):
    description: str
    min_salary: int
    max_salary: int
    staus: str
    date_posted: date

    @classmethod
    def from_query_result(cls, description, min_salary,max_salary, staus,date_posted):
        return cls(
            description= description,
            min_salary=min_salary,
            max_salary = max_salary,
            staus= staus,
            date_posted=date_posted)