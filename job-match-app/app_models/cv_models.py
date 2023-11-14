#COMPANY ADS - CVS
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CvCreation(BaseModel):
    description: str
    min_salary: int
    max_salary: int
    status: str
    date_posted: datetime


    def from_query_result(cls, description, min_salary,max_salary, status,date_posted):
        return cls(description = description,
                   min_salary = min_salary,
                   max_salary = max_salary,
                   status = status,
                   date_posted = date_posted
            )